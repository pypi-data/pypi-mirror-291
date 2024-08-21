#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import subprocess
from typing import List, Tuple

import qcelemental as qcel
from conformer_core.properties.extraction import calc_property

from atomdriver.abstract_driver import RunContext, ShellCommandDriver


class MOPAC(ShellCommandDriver):
    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
            PM7 XYZ PRECISE NOSYM NOREOR GEO-OK


            {geometry}
        """,
        "atom": "{symbol}    {x} {y} {z}",
        "ghost_atom": None,
    }
    FILE_MANIFEST = {"input": ".mop", "output": ".out"}
    RUN_CMD = "MOPAC2016.exe"

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
                == 0
            )
        except FileNotFoundError:
            return False

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.RUN_CMD, [ctx.files["input"]]

    @calc_property(source="re_file", patterns=[r"TOTAL ENERGY\s+=\s+(-?\d+\.\d+)\sEV"])
    def prop_total_energy(self, ctx, m, _):
        return float(m[1]) / qcel.constants.hartree2ev

    @calc_property(
        source="re_file", patterns=[r"COMPUTATION TIME\s+=\s+(-?\d+\.\d+)\sSECONDS"]
    )
    def prop_cpu_time(self, ctx, m, _):
        return float(m[1])
