#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import enum
import subprocess
from copy import copy
from datetime import datetime
from os import environ
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional, Tuple, cast

import numpy as np
import numpy.typing as npt
from conformer.elements import ANGSTROM_TO_BOHR, BOHR_TO_ANGSTROM
from conformer_core.properties.extraction import calc_property
from conformer_core.records import RecordStatus
from pydantic import Field, model_validator

from atomdriver.abstract_driver import (
    Driver,
    DriverOptions,
    RunContext,
)
from atomdriver.properties import NuclearGradient
from atomdriver.templating import SystemTemplate


class CP2KEnvironment:
    id: int
    cp2k_proc: "CP2KProc"
    natom: int
    active: bool

    # For ENV reuse
    atom_counts: Dict[str, int]

    def __init__(self, cp2k_proc: "CP2KProc", env_id: int) -> None:
        self.id = env_id
        self.cp2k_proc = cp2k_proc
        self.natom = int(self.put(f"NATOM {self.id}"))
        self.active = True

    def __del__(self):
        # Only destroy if the process is running
        if self.cp2k_proc.proc is None:
            return
        self.destroy()

    def put(self, *input: str, flush=True) -> bytes:
        return self.cp2k_proc.put(*input, flush=flush)

    def get(self) -> str:
        return self.cp2k_proc.get()

    def flush(self) -> None:
        self.cp2k_proc.flush()

    def destroy(self) -> None:
        """
        destroys the given environment (last and default env
        might become invalid)
        """
        if self.active and self.cp2k_proc.is_running():
            self.cp2k_proc.DESTROY(self.id)
        self.active = False

    def get_natom(self) -> int:
        """returns the number of atoms in the environment env_id"""
        return int(self.put(f"NATOM {self.id}"))

    @property
    def positions(self) -> npt.NDArray[np.float64]:
        """
        gets the positions of the atoms, returns
        natom*3 (on a line) and then all the positions then "* END"
        (alone on a line)
        """
        result = self.put(f"GET_POS {self.id}")
        pos = np.zeros((self.natom, 3), np.float64)
        # [1:-1] trims out 3*natom and * END
        for l, r in zip(result.split("\n")[1:-1], pos):
            r[:] = [float(_l) for _l in l.split()]
        pos *= BOHR_TO_ANGSTROM
        return pos

    @positions.setter
    def positions(self, pos: npt.NDArray[np.float64]) -> None:
        """
        sets the positions of the atoms, should be followed
        by natom*3 (on a line) and then all the positions. Returns the max
        change of the coordinates (useful to avoid extra calculations).
        """
        self.put(f"SET_POS {self.id}", flush=False)
        self.put(str(self.natom * 3), flush=False)
        for r in pos * ANGSTROM_TO_BOHR:
            self.put(*r, flush=False)
        self.put("*END", flush=True)  # "* END" gives an error

    @property
    def cell(self) -> npt.NDArray[np.float64]:
        res_str = self.put(f"GET_CELL {self.id}", flush=True)
        cell = np.fromiter(
            (float(i) for i in res_str.split()), np.float64, count=9
        ).reshape((3, 3), order="F")
        cell *= BOHR_TO_ANGSTROM
        return cell

    @cell.setter
    def cell(self, cell: npt.NDArray[np.float64]) -> None:
        self.put(f"SET_CELL {self.id}", flush=False)
        for r in cell * ANGSTROM_TO_BOHR:
            self.put(" ".join((str(i) for i in r)), flush=False)
        self.get()

    def get_stress(self) -> npt.NDArray[np.float64]:
        """gets the stress tensor of the last calculation on env_id"""
        raise NotImplementedError("`get_stress` is not implemented")

    def get_energy(self) -> float:
        """gets the energy of the last calculation on env_id"""
        return float(self.put(f"GET_E {self.id}"))

    def get_forces(self) -> npt.NDArray[np.float64]:
        """
        gets the forces on the atoms of the last calculation on
        env_id, if only the energy was calculated the content is undefined. Returns
        natom*3 (on a line) and then all the forces then "* END" (alone on
        a line)
        """
        res_str = self.put(f"GET_F {self.id}")
        lines = res_str.split("\n")
        gradient = np.zeros((self.natom, 3), np.float64)
        for l, r in zip(lines[1:-1], gradient):
            r[:] = np.fromiter((float(_l) for _l in l.split()), np.float64, 3)
        return gradient

    def calc_energy(self) -> float:
        """calculate the energy and returns it"""
        return float(self.put(f"CALC_E {self.id}"))

    def calc_force_energy(self) -> Tuple[float, npt.NDArray[np.float64]]:
        """
        calculate energy and forces and returns them,
        first the energy on a line, then the natom*3 (on a line)
        and finally all the values and "* END" (alone on a line)
        """
        res_str = self.put(f"CALC_EF {self.id}")
        lines = res_str.split("\n")
        energy = float(lines[0])
        gradient = np.zeros((self.natom, 3), np.float64)
        for l, r in zip(lines[2:-1], gradient):
            r[:] = np.fromiter((float(_l) for _l in l.split()), np.float64, 3)
        return energy, gradient


class CP2KDirectives(enum.Enum):
    READY: str = "* READY\n"
    END: str = "* END\n"
    ERROR: str = "* ERROR"


DIRECTIVES_LIST = [i.value for i in CP2KDirectives]


class ProcessCompletedError(Exception):
    ...


class CP2KProc:
    args: List[str]
    harsh_on_error: bool
    proc: Optional[Popen]
    environ: Dict[str, str]
    environments: Dict[int, CP2KEnvironment]

    def __init__(self, args, path=None, stop_on_error=False, environ=None) -> None:
        if "--shell" not in args:
            raise ValueError("`args` must contain '--shell' option.")
        self.args = args

        # Runtime
        self.path = path
        if environ is None:
            self.environ = environ
        else:
            self.environ = environ
        self.stop_on_error = stop_on_error

        # State vars
        self.environments = {}
        self.proc = None

    def is_running(self):
        if self.proc is None:
            return False
        else:
            return self.proc.poll() is None

    def startup(self):
        # Clear out previous calculations
        if self.proc is not None:
            self.shutdown()

        # Start new process
        self.proc = Popen(
            self.args,
            stdin=PIPE,
            stdout=PIPE,
            # start_new_session=True,
            # stderr=STDOUT,
            cwd=self.path,
            text=True,
            env=self.environ,
        )

        # Read initial startup
        self.get()

        # Set permissive mode. Default is permissive
        if self.stop_on_error:
            self.HARSH()
        else:
            self.PERMISSIVE()

    def shutdown(self):
        # Deactivate all environments
        for env in self.environments.values():
            env.destroy()

        if self.proc is None:
            return

        # Allocate to list so we don't change sizes during itr
        # for env in list(self.environments.items()):
        #     self.destroy_env(env)

        if self.is_running():
            self.EXIT()

        # Clean up the IO for the process
        if not self.proc.stdin.closed:
            try:
                self.proc.stdin.close()
            except BrokenPipeError:
                pass

        if not self.proc.stdout.closed:
            try:
                self.proc.stdout.close()
            except BrokenPipeError:
                pass

        self.proc = None

    def __del__(self):
        self.shutdown()

    def get(self):
        self.flush()
        result = ""
        l = ""
        while l != CP2KDirectives.READY.value:
            result += l
            l = self.proc.stdout.readline()
            # DEBUGGING
            # if l.strip():
            #     print("<<", repr(l), l == CP2KDirectives.READY.value)
            if l.startswith(CP2KDirectives.ERROR.value):
                print("CP2K DRIVER: THERE WAS AN ERROR IN THE CP2K SHELL")
                print(l)
            if not l and not self.is_running():
                raise ProcessCompletedError("CP2K process is no longer running")
        return result

    def put(self, *input: str, flush=True) -> bytes:
        # (Re)start the server if it's shut down
        if not self.is_running():
            self.startup()
        # DEBUGGING
        # print(">>", input)
        print(*input, file=self.proc.stdin)

        # Return result
        if flush:
            return self.get()

    def flush(self):
        self.proc.stdin.flush()

    def load_file(self, input_file: str, output_file: str) -> CP2KEnvironment:
        env = CP2KEnvironment(self, self.LOAD(input_file, output_file))
        self.environments[env.id] = env
        return env

    def destroy_env(self, env: CP2KEnvironment) -> None:
        env.destroy()
        del self.environments[env.id]

    def run_file(self, input_file: str, output_file: Optional[str] = None) -> None:
        return self.RUN(input_file, output_file)

    # COMMANDS
    def INFO(self):
        """INFO: returns some information about cp2k."""
        return self.put("INFO")

    def VERSION(self):
        """returns shell version. (queried by ASE to assert features & bugfixes)"""
        return self.put("VERSION").strip()

    def HARSH(self) -> None:
        """stops on any error"""
        self.put("HARSH")

    def PERMISSIVE(self) -> str:
        """stops only on serious errors"""
        self.put("PERMISSIVE")

    def UNITS(self) -> str:
        """returns the units used for energy and position"""
        return self.put("UNITS").strip()

    def UNITS_EV_A(self) -> None:
        """sets the units to electron volt (energy)  and Angstrom (positions)"""
        self.put("UNITS_EV_A")

    def UNITS_AU(self) -> None:
        """sets the units atomic units"""
        self.put("UNITS_AU")

    def CD(self, dir: str) -> None:
        """change working directory"""
        self.put(f"CD {dir}")

    def PWD(self) -> str:
        """print working directory"""
        return self.put("PWD").strip()

    def EXIT(self) -> None:
        """
        Quit the shell

        Passes the exit command + EOF
        """
        try:
            std, err = self.proc.communicate("EXIT\n", 3)  # Shudown with 3 s timeout
            assert std == "* EXIT\n"
            assert err is None
        except TimeoutExpired:
            self.proc.kill()

    def LOAD(self, input_file: str, output_file: Optional[None] = None) -> int:
        """
        loads the filename, returns the env_id, or -1 in case of error
        out-filename is optional and defaults to <inp-filename>.out
        use "__STD_OUT__" for printing to the screen
        """
        if output_file is None:
            output_file = "__STD_OUT__"
        return int(self.put(f"LOAD {input_file} {output_file}"))

    def RUN(self, input_file: str, output_file: Optional[str] = None) -> None:
        """run the given input file"""
        if output_file is None:
            output_file = "__STD_OUT__"
        self.put(f"RUN {input_file} {output_file}")

    def LAST_ENV_ID(self) -> CP2KEnvironment:
        """returns the env_id of the last environment loaded"""
        return int(self.put("LAST_ENV_ID"))

    def DESTROY(self, env_id: int) -> None:
        """destroys the given environment (last and default env might become invalid)"""
        try:
            self.put(f"DESTROY {env_id}")
        except ProcessCompletedError:
            pass


class CP2K(Driver):
    class Options(DriverOptions):
        exec: str = Field(default_factory=lambda: environ.get("CP2K_EXEC", "cp2k"))
        mpi_procs: Optional[int] = None
        omp_threads: Optional[int] = None

        calc_gradient: bool = False

        # TODO: Add custom Pydantic validators for these either-or options
        template: str = Field(default_factory=str)
        template_file: Optional[str] = None
        static_files: List[str] | Dict[str, str] = Field(default_factory=dict)
        environment: Dict["str", "str"] = Field(default_factory=dict)

        # RUNTIME OPTIONS
        batch_size: int = 50

        @model_validator(mode="after")
        def validate_templates(self):
            if self.template_file is not None and self.template:
                raise ValueError(
                    "Both 'template_file' and 'template' are mutually exclusive."
                )

        ##### SLURM EXAMPLE #####
        # cpus = 32
        # run_command: List[str] = [
        #     'srun',
        #     '-n8',
        #     '-N1',
        #     '--cpu_bind', 'core',
        #     '--cpus-per-task=4',
        #     'cp2k.psmp',
        #     '--shell'
        # ]
        # environment = {
        #     'OMP_NUM_THREADS': '4',
        #     'OMP_PROC_BIND': 'close',
        #     'OMP_PLACES': 'cores'
        # }

    opts: Options

    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
        {n_atoms}
        {name}: n_atoms={n_atoms};
        {geometry}
        """,
        "atom": "{symbol}    {x} {y} {z}",
    }
    FILE_MANIFEST = {
        "input": ".inp",
        "geometry": ".xyz",
        "output": ".out",
        "log": ".log",
    }
    EXTRACTABLE_FILES = tuple()

    # CP2K tends to have multiple names for the exec. so we will configure this at runtime
    RUN_CMD = environ.get("CP2K_EXEC", "cp2k")

    proc: Optional[CP2KProc] = None
    STATIC_PATH: Optional[TemporaryDirectory] = None

    def __init_stage__(self):
        opts = self.opts

        # Read the template file
        if opts.template_file is not None:
            with open(opts.template_file, "r") as f:
                opts.template = f.read()
            opts.template_file = None

        # Read static files
        if isinstance(opts.static_files, List):
            static_files = {}
            for fp in opts.static_files:
                fp = Path(fp)
                with fp.open("r") as f:
                    static_files[fp.name] = f.read()
            opts.static_files = static_files

    @classmethod
    def is_available(cls):
        try:
            return (
                subprocess.run(
                    cls.RUN_CMD, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                ).returncode
                == 0
            )
        except FileNotFoundError:
            return False

    def make_template(self) -> None:
        # Set defaults
        self.template = SystemTemplate(**self.DEFAULT_TEMPLATE_PARAMS)

    def configure(self) -> None:
        super().configure()

        # Make static files!
        static_files = cast(Dict[str, str], self.opts.static_files)
        self.STATIC_PATH = TemporaryDirectory()
        SP = Path(self.STATIC_PATH.name)
        for fname, fdata in static_files.items():
            with (SP / fname).open("w") as f:
                f.write(fdata)

        # Make the template!
        self.make_template()

        basepath = self.allocation.basepath
        basepath.mkdir(exist_ok=True, parents=True)
        run_cmd, env = self.get_run_cmd()
        env.update(self.opts.environment)
        self.proc = CP2KProc(run_cmd, path=basepath, stop_on_error=False, environ=env)
        self.proc.startup()

    def get_run_cmd(self) -> Tuple[str, Dict[str, str]]:
        cmd = environ.get("CP2K_EXEC", self.opts.exec)
        cmd_path = Path(cmd)

        if cmd_path.suffix in (".psmp", ".popt"):
            use_MPI = True
        else:  # Assume its a non-MPI build
            use_MPI = False

        # Handle single-core process
        if not use_MPI:
            env = copy(environ)
            env.update(
                OMP_NUM_THREADS=str(self.allocation.cpus),
                OMP_PROC_BIND="false",
                OMP_PLACES="cores",
            )
            return [cmd, "--shell"], env

        # Handle MPI (mulit-core) process
        hostname = environ.get("SLURMD_NODENAME", self.machine.hostname)
        env = copy(environ)

        if self.opts.mpi_procs is None:
            nprocs = self.allocation.cpus
        else:
            nprocs = self.opts.mpi_procs

        if self.opts.omp_threads:
            env.update(
                OMP_NUM_THREADS=str(self.opts.omp_threads),
                OMP_PROC_BIND="false",
                OMP_PLACES="cores",
            )
        elif self.allocation.cpus % nprocs != 0:
            raise ValueError(
                f"`mpi_procs` {nprocs} must be a factor of `cpus` ({self.allocation.cpus})"
            )
        else:
            nthreads = self.allocation.cpus // nprocs
            env.update(
                OMP_NUM_THREADS=str(nthreads), OMP_PROC_BIND="false", OMP_PLACES="cores"
            )

        # fmt: off
        run_cmd = [
            "mpirun",
            "-n", str(nprocs), 
            "--host", hostname, 
            "--oversubscribe",
            cmd,
            "--shell",
        ]
        # fmt: on
        return run_cmd, env

    def cleanup(self):
        if self.proc:
            self.proc.shutdown()
            del self.proc
            self.proc = None
        if self.STATIC_PATH:
            self.STATIC_PATH.cleanup()
        super().cleanup()

    def setup_calc(self, ctx: RunContext):
        super().setup_calc(ctx)

        # TODO: Make this more customizable
        # Write the input file
        # Fails if there isn't this file so make a dummy
        assert ctx.workpath.exists()

        with ctx.files["geometry"].open("w") as f:
            sys = ctx.working_system
            f.write(
                self.template.system_to_string(
                    sys,
                    num_atoms=sys.size,
                    name=ctx.working_system.name,
                    time=datetime.now().isoformat(),
                    system_id=ctx.record.id,
                )
            )

        with ctx.files["input"].open("w") as f:
            kwargs = {
                "name": ctx.working_system.name,
                "charge": ctx.record.system.charge,
                "multiplicity": ctx.record.system.multiplicity,
                "num_atoms": ctx.record.system.size,
                "geometry_file": ctx.files["geometry"],
                "static_path": self.STATIC_PATH.name,
                "cpus": self.allocation.cpus,
                "total_memory": self.allocation.memory,
                "memory_per_cpu": int(self.allocation.memory / self.allocation.cpus),
            }
            if ctx.working_system.unit_cell is not None:
                kwargs["cell"] = "{} {} {}".format(*sys.unit_cell)
            f.write(self.opts.template.format(**kwargs))

    def run_calc(self, ctx: RunContext) -> None:
        ctx.record.start_time = datetime.now()
        self.proc.CD(ctx.workpath)
        assert ctx.files["input"].exists()

        try:
            env = self.proc.load_file(ctx.files["input"], ctx.files["output"])
            ctx.scratch["env"] = env

            # Calculate properties
            if self.opts.calc_gradient:
                (
                    ctx.scratch["total_energy"],
                    ctx.scratch["forces"],
                ) = env.calc_force_energy()
            else:
                ctx.scratch["total_energy"] = env.calc_energy()
        except ProcessCompletedError:
            with ctx.files["output"].open("r") as f:
                ctx.record.meta["error"] = "".join(f.readlines()[-50:])
            ctx.record.status = RecordStatus.FAILED
        finally:
            ctx.record.end_time = datetime.now()

    def determine_success(self, ctx: RunContext):
        """What other checks to make sure it returned correctly?"""
        return

    def cleanup_calc(self, ctx: RunContext):
        env = ctx.scratch.get("env")
        if env:
            env.destroy()
        return super().cleanup_calc(ctx)

    @calc_property(source="context")
    def prop_total_energy(self, ctx: RunContext):
        energy = ctx.scratch.get("total_energy", None)
        if energy is None:
            ctx.record.status = RecordStatus.FAILED
        return energy

    @calc_property(source="context")
    def prop_nuclear_gradient(self, ctx: RunContext):
        if not self.opts.calc_gradient:
            return None
        grad = ctx.scratch.get("forces", None)
        if grad is None:
            return None
        atom_map = []
        atom_type_map = []
        for i, a in enumerate(ctx.record.system):
            if a.is_physical:
                atom_map.append(i)
                if a.is_proxy:
                    atom_type_map.append(1)  # Proxies will take back seat
                else:
                    atom_type_map.append(0)  # Real atom
        return NuclearGradient(atom_map, atom_type_map, -grad)  # Return gradient
