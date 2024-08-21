#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import subprocess
from typing import List, Tuple

from conformer_core.properties.extraction import calc_property

from atomdriver.abstract_driver import RunContext, ShellCommandDriver


class NWChem(ShellCommandDriver):
    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
            start {name}
            title "{name}"
            charge {charge}
            geometry
            {geometry}
            end
            basis
                * library 6-31G
            end
            task scf
        """,
        "atom": "{symbol}    {x} {y} {z}",
        "ghost_atom": "bq{symbol}    {x} {y} {z}",
    }
    FILE_MANIFEST = {"input": ".nw", "output": ".out"}
    STDOUT_FILE = "output"
    RUN_CMD = "nwchem"

    @classmethod
    def is_available(cls):
        try:
            return (
                subprocess.run(
                    cls.RUN_CMD,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    input=b"\n",
                ).returncode
                == 255
            )
        except FileNotFoundError:
            return False

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.RUN_CMD, [ctx.files["input"]]

    @calc_property(
        source="re_file", patterns=[r"Total\s+SCF\s+energy\s=\s+(-\d+\.\d+)"]
    )
    def prop_total_energy(self, ctx, m, _):
        return float(m[1])

    @calc_property(source="re_file", patterns=[r"Total\s+times\s+cpu:\s+(\d+\.\d+)s"])
    def prop_cpu_time(self, ctx, m, _):
        return float(m[1])
