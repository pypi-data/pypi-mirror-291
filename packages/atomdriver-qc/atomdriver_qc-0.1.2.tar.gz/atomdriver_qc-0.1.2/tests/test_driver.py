#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
"""Test the generic driver packages"""

from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import List, Tuple
from uuid import UUID

from conformer.systems import System
from conformer_core.records import RecordStatus

from atomdriver.abstract_driver import Driver, RunContext, ShellCommandDriver
from tests import AtomDriverTestCase

H2O_STR = """
H    0.0000000    0.5383516   -0.7830366
O   -0.0000000   -0.0184041    0.0000000
H   -0.0000000    0.5383516    0.7830366
"""


class TestDriver(Driver):
    """
    Create a driver that actually runs code. It's easier to test
    """

    def run_calc(self, ctx: RunContext):
        ctx.record.start_time = datetime.now()
        ctx.record.end_time = datetime.now()


class TestShellCommandDriver(ShellCommandDriver):
    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
            {charge} {mult} 
            {geometry}
        """,
        "atom": "{symbol}    {x: .2f} {y: .2f} {z: .2f}",
        "ghost_atom": "@{symbol}    {x: .2f} {y: .2f} {z: .2f}",
    }
    RUN_CMD = "touch"

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.RUN_CMD, [str(ctx.files["output"])]


class DriverTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.H2O = System.from_string(H2O_STR)

    def test_configure(self) -> None:
        driver = TestDriver.from_options()
        self.assertFalse(driver.is_configured)
        self.assertFalse(driver.is_provisioned)
        driver.configure()
        self.assertTrue(driver.is_configured)
        self.assertTrue(driver.is_provisioned)

    def test_run_ctx(self) -> None:
        driver = TestDriver.from_options()
        res = driver(self.H2O)
        self.assertIsInstance(res.start_time, datetime)
        self.assertIsInstance(res.end_time, datetime)
        self.assertTrue("wall_time" in res.properties)


class ShellCommandDriverTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.H2O = System.from_string(H2O_STR)

    def test_run_ctx(self) -> None:
        # Keep the files for examination
        driver = TestShellCommandDriver.from_options(
            remove_files=False, name="Test Driver"
        )
        rec = driver(self.H2O)

        self.assertEqual(rec.status, RecordStatus.COMPLETED)

        # Test that all the files were created
        workpath = Path(rec.meta["work_path"])
        for file, ext in driver.FILE_MANIFEST.items():
            p = workpath / (file + ext)
            self.assertTrue(p.exists())
            if ext == ".inp":
                input = p

        with input.open() as f:
            self.assertEqual(
                f.read(),
                dedent(
                    """\
                0 1 
                O    -0.00 -0.02  0.00
                H     0.00  0.54 -0.78
                H    -0.00  0.54  0.78
            """
                ),
            )

        self.assertIsInstance(rec.start_time, datetime)
        self.assertIsInstance(rec.end_time, datetime)
        self.assertTrue("wall_time" in rec.properties)
        self.assertTrue("work_path" in rec.meta)

        # Clean variable data
        rec.id = UUID(int=0)
        rec.start_time = datetime(2020, 1, 1)
        rec.properties["wall_time"] = 0.0
        rec.meta["work_path"] = "/"
        fixture = dedent(
            """\
        System Record 00000000-0000-0000-0000-000000000000: 
          Driver: Test Driver
          Created: 2020-01-01T00:00
          System: System(formula="H2O", name="sys-66e36aa0")
          Status: COMPLETED
          Meta:
            work_path: /
          Properties:
            Wall Time:  0.000000 s
        """
        )
        self.assertEqual(fixture, rec.summarize())
