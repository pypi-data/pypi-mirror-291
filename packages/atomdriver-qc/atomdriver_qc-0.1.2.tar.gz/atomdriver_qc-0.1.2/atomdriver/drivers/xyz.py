#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from datetime import datetime
from typing import List, Tuple

from conformer_core.records import RecordStatus

from atomdriver.abstract_driver import (
    RunContext,
    ShellCommandDriver,
    ShellCommandDriverOptions,
)


class XYZ(ShellCommandDriver):
    class Options(ShellCommandDriverOptions):
        remove_files: bool = False

    RUN_CMD = ":"  # no-op
    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
            {n_atoms}
            Fragment {name}; Charge={charge}; Multiplicity={mult}
            {geometry}
        """,
        "atom": "{symbol}    {x} {y} {z}",
        "ghost_atom": None,
    }
    FILE_MANIFEST = {
        "input": ".xyz",
    }
    EXTRACTABLE_FILES = tuple()

    @classmethod
    def is_available(cls):
        return True

    def run_calc(self, ctx: RunContext):
        ctx.status = RecordStatus.COMPLETED
        ctx.start_time = datetime.now()
        ctx.end_time = datetime.now()
        return ctx

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return "", []

    def determine_success(self, ctx: RunContext) -> None:
        return
