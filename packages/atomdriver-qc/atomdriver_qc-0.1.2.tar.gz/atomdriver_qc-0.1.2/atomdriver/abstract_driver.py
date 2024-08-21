#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import inspect
import logging
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from typing import Any, ClassVar, Dict, List, Optional, TextIO, Tuple

from conformer.records import Property, SystemRecord
from conformer.systems import System
from conformer_core.properties.core import add_property
from conformer_core.properties.extraction import PropertyExtractorMixin, calc_property
from conformer_core.records import RecordStatus
from conformer_core.stages import Stage, StageOptions

import atomdriver.properties as ad_properties  # import to initilize all properties
from atomdriver.context import Machine, ResourceAllocation
from atomdriver.exceptions import (
    BackendRunException,
    ConfigurationError,
    NoOutputFile,
    ProcessFailed,
)
from atomdriver.templating import SystemTemplate

# Adds all properties to the MASTER_PROPERTY_LIST. 
# TODO: Replace this with registry code
for name, val in inspect.getmembers(ad_properties):
    if isinstance(val, Property):
        add_property(val)

log = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class RunContext:
    """Transient information needed to handle a claculation including files and
    scratch data
    """

    working_system: System  # The working copy of the system
    record: SystemRecord
    workpath: Optional[Path] = None
    scratch: Dict[Any, Any] = field(
        default_factory=dict
    )  # Scratch space for running the calc
    files: Dict[str, Path] = field(default_factory=dict)
    _open_files: Dict[str, TextIO] = field(default_factory=dict)

    def open_file(self, tag: str, mode="r") -> TextIO:
        if tag in self._open_files:
            return self._open_files[tag]
        self._open_files[tag] = self.files[tag].open(mode)
        return self._open_files[tag]

    def close_file(self, tag: str) -> None:
        f = self._open_files.get(tag, None)
        if f is None:
            return
        f.close()
        del self._open_files[tag]

    def close_files(self) -> None:
        for f in self._open_files.values():
            f.close()
        self._open_files = dict()

    def sanitize(self) -> None:
        self.scratch = {}
        self.close_files()


class DriverOptions(StageOptions):
    cpus: int = 1  # Max number of CPUs
    memory: Optional[int] = None  # Max memory in MB
    remove_files: bool = True
    batch_size: int = 5  # How many calculations to run cuncurrently

    # Options for use with DriverAccessors
    use_database: bool = True
    use_cache: bool = True
    run_calculations: bool = True


class Driver(Stage, PropertyExtractorMixin):
    Options = DriverOptions

    opts: DriverOptions
    allocation: ResourceAllocation
    machine: Machine

    # Class variables
    FILELESS: ClassVar[bool] = True  # Potentially fileless
    EXTRACTABLE_FILES: ClassVar[Tuple[str, ...]] = tuple()
    FILE_MANIFEST: ClassVar[Dict[str, str]] = dict()
    is_configured: bool = False
    is_provisioned: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allocation = None
        self.machine = None

    @classmethod
    def is_available(cls) -> bool:
        """
        Returns true if this backend be used pending system configuration
        """
        return True

    @property
    def is_fileless(self):
        """
        Returns `true` if QM backend does not need access to the filesystem

        .. note:: Some backends which do not use input/output files such
            as PySCF require filesystem access for scratch files
        """
        if self.FILE_MANIFEST:
            return False
        return self.FILELESS

    def configure(self) -> None:
        """Configures backend to work the the amount of cores and memeory provided by `worker`"""
        if not self.is_provisioned:
            self.provision()  # Do default provisioning
        self.is_configured = True

    def provision(
        self,
        allocation: ResourceAllocation = None,
        cpus: Optional[int] = None,
        memory: Optional[int] = None,
        basepath: Optional[Path] = None,
        machine: Optional[Machine] = None,
        force=False,
    ):
        """Set resource useage for the driver"""
        if self.allocation and not force:
            return
        self.machine = machine if machine else Machine()
        self.is_provisioned = True
        # We are given an allocation
        if allocation is not None and any([cpus, memory]):
            raise ValueError("Cannot specify both `allocation` and `cpus`/`memory`")
        else:  # We are told what the allocation should be
            if cpus is None:
                cpus = self.opts.cpus
            if memory is None:
                memory = self.opts.memory
            allocation = ResourceAllocation(cpus=cpus, memory=memory, basepath=basepath)
        self.allocation = allocation

    def cleanup(self):
        if self.is_provisioned:
            self.allocation.cleanup()
        self.is_configured = False

    def __del__(self):
        self.cleanup()

    def __call__(self, system: System):
        """Something something something"""
        if not self.is_configured:
            self.configure()
        rec = self.mk_record(system)
        return self.run_record(rec)

    def mk_record(self, system: System) -> SystemRecord:
        return SystemRecord(system=system, stage=self)

    def mk_context(self, record: SystemRecord) -> RunContext:
        return RunContext(
            working_system=record.system.canonize(),
            record=record,
            workpath=self.allocation.basepath / str(record.id),
        )

    def system_context(self, system: System):
        """Returns a context object for the system"""
        if not self.is_configured:
            self.configure()
        rec = self.mk_record(system)
        return self.mk_context(rec)

    def run_record(self, record: SystemRecord) -> SystemRecord:
        """
        Run calculation given a run context
        """
        ctx = self.mk_context(record)

        try:
            self.setup_calc(ctx)
            self.run_calc(ctx)
            self.gather_results(ctx)
        except Exception as e:
            # Is this the best option? this will be funneled into the DB...
            # Let's let this fail. This is Fragment issue, not a backend subprocess issue
            record.status = RecordStatus.FAILED
            record.meta["error"] = str(e)
            raise e
        finally:
            self.cleanup_calc(ctx)
        return ctx.record

    def create_workpath(self, ctx: RunContext):
        # NOTE: It's possible to have an empty FILE_MANIFEST and still be
        #       FILELESS due to non-saved scratch files
        if not self.is_fileless:
            if ctx.workpath is None:
                raise ConfigurationError(f"Driver {self.__class__} needs a workpath")
            if not ctx.workpath.is_absolute():
                raise ConfigurationError(
                    "Context has a relative workpath: " + str(ctx.workpath)
                )

            ctx.scratch["old_path"] = os.getcwd()
            ctx.workpath.mkdir(parents=True, exist_ok=True)
            os.chdir(ctx.workpath)

            # Create files and add the to the file manifext
            for k, ext in self.FILE_MANIFEST.items():
                ctx.files[k] = ctx.workpath / f"{k}{ext}"

    def setup_calc(self, ctx: RunContext):
        """
        Ensure that the environment is setup to run the calculation
        """
        self.create_workpath(ctx)

    def run_calc(self, ctx: RunContext):
        """Execute the QM backend"""
        raise NotImplementedError(
            f"Please implement `{self.__class__.__name__}.run_calc`"
        )

    def determine_success(self, ctx: RunContext):
        for file in ctx.files.values():
            if not file.exists():
                raise NoOutputFile(f"Process did not create an output file {file}")

    @calc_property(source="context")
    def prop_wall_time(self, ctx: RunContext):
        if ctx is None:  # Testing does this. I dislike it.
            return
        if ctx.record.start_time is None or ctx.record.end_time is None:
            return None
        return (ctx.record.end_time - ctx.record.start_time).total_seconds()

    def sources_from_ctx(self, ctx: RunContext) -> List[Any]:
        sources = []

        # Handle files inside RunContexts
        ctx.close_files()  # Start from a clean slate

        # Open the run context and add it's file to list of sources
        for tag in self.EXTRACTABLE_FILES:
            if ctx.files[tag].exists():
                sources.append(ctx.open_file(tag))
        return sources

    def gather_results(self, ctx: RunContext) -> RunContext:
        try:
            self.determine_success(ctx)
        except BackendRunException:
            ctx.record.status = RecordStatus.FAILED
        else:
            ctx.record.status = RecordStatus.COMPLETED

        try:
            ctx.record.properties = self.get_properties(ctx, self.sources_from_ctx(ctx))
            return ctx
        finally:
            ctx.close_files()

    def cleanup_calc(self, ctx: RunContext):
        ctx.close_files()

        if ctx.scratch.get("old_path", None):
            os.chdir(ctx.scratch["old_path"])

        if not self.is_fileless:
            if self.opts.remove_files:
                rmtree(ctx.workpath)
            else:
                ctx.record.meta["work_path"] = str(ctx.workpath.absolute())


class ShellCommandDriverOptions(DriverOptions):
    template: Optional[str] = None


class ShellCommandDriver(Driver):
    Options = ShellCommandDriverOptions

    DEFAULT_TEMPLATE_PARAMS: Dict[str, Any] = {}
    FILELESS = False
    FILE_MANIFEST = {"input": ".inp", "output": ".out", "log": ".log"}
    EXTRACTABLE_FILES = ("output",)
    STDOUT_FILE: str = "log"
    STDERR_FILE: str = "log"
    RUN_CMD: ClassVar[str]
    AVAILABLE_RETURN_CODE: ClassVar[int] = 0

    def configure(self) -> None:
        super().configure()
        # Pass along arguments and make them saveable
        self.make_template()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if "log" not in cls.FILE_MANIFEST:
            if cls.STDOUT_FILE == "log" or cls.STDERR_FILE == "log":
                cls.FILE_MANIFEST["log"] = ".log"

        for f in cls.EXTRACTABLE_FILES:
            if f not in cls.FILE_MANIFEST:
                raise ConfigurationError(
                    f"The extractible file {f} is not in the FILE_MANIFEST"
                )

    def make_template(self) -> None:
        # Set defaults
        self.template = SystemTemplate(**self.DEFAULT_TEMPLATE_PARAMS)
        # Overwrite with user-supplied values
        if self.opts.template:
            self.template.override(template=self.opts.template)

    @classmethod
    def is_available(cls):
        result = subprocess.run(["which", cls.RUN_CMD], text=True, capture_output=True)
        return result.returncode == cls.AVAILABLE_RETURN_CODE

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        """Returns the command-line program required to run an external
        QM application

        .. note:: This function assumes the QM process will be run on a single
            node with multiple CPUs

        Argumens:
            input_path (str): The path to an existing input file
            output_path (str): The path to the not-yet-written output file
            cores(int): Number of threads/CPUs to run the application

        Returns:
            str: QM Command
            List[str]: Arguments
        """
        raise NotImplementedError("The backend should implement this function")

    def run_calc(self, ctx: RunContext):
        cmd = ctx.scratch["run_cmd"]
        args = ctx.scratch["run_args"]

        ctx.record.start_time = datetime.now()
        proc = subprocess.Popen(
            [cmd] + args,
            stdout=ctx.open_file(self.STDOUT_FILE, "w"),
            stderr=ctx.open_file(self.STDERR_FILE, "w"),
        )
        ctx.scratch["proc"] = proc
        proc.wait()
        ctx.record.end_time = datetime.now()
        ctx.close_files()

    def determine_success(self, ctx: RunContext):
        """Raise exception if the QM Job failed

        Args:
            output_path (int): Expected output path of the QM process
            returncode (int): Shell return code
            stdout (str): String of the STDOUT content
            stderror (str): String of STDERR content

        Raises:
            ProcessFailed: Raised if non-zero return code
            NoOutputFile: Raise if no output file was created
        """
        try:
            proc: subprocess.Popen = ctx.scratch["proc"]
        except KeyError:
            raise BackendRunException("The executable was never called.")
        if proc.returncode is None:
            raise BackendRunException("Calculation is still running")
        if proc.returncode != 0:
            raise ProcessFailed("Process returned a non-zero exit code")
        super().determine_success(ctx)

    def setup_calc(self, ctx: RunContext):
        super().setup_calc(ctx)

        # Get the run command
        ctx.scratch["run_cmd"], ctx.scratch["run_args"] = self.get_run_cmd(ctx)

        if ctx.files["input"].exists():
            return
        with ctx.files["input"].open("w") as f:
            f.write(
                self.template.system_to_string(
                    ctx.working_system,
                    num_atoms=ctx.working_system.size,
                    name=ctx.working_system.name,
                    time=datetime.now().isoformat(),
                    backend=self.name,
                    cpus=self.allocation.cpus,
                    total_memory=self.allocation.memory,
                    memory_per_cpu=int(self.allocation.memory / self.allocation.cpus),
                )
            )

    # def file_manifest(self, filename_stub: str, workpath: Path) -> Dict[str, Path]:
    #     if not "log" in self.FILE_MANIFEST:
    #         self.FILE_MANIFEST["log"] = ".log"
    #     return super().file_manifest(filename_stub, workpath)
