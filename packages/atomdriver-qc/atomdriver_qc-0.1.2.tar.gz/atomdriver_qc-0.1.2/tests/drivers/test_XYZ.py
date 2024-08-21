#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from atomdriver.drivers.xyz import XYZ
from tests._util import TempDirTestCase, make_system


class XYZTestCases(TempDirTestCase):
    def setUp(self) -> None:
        self.backend = XYZ()
        self.backend.configure()
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()

    def test_atom(self):
        atom = self.sys[0]
        self.assertEqual(self.backend.template.atom_to_string(atom), "H    0.0 0.0 0.0")

    def test_ghost_atom(self):
        atom = self.sys[2]
        self.assertIsNone(self.backend.template.atom_to_string(atom))

    def test_template(self):
        self.assertEqual(
            self.backend.template.system_to_string(self.sys, name="fragment_1"),
            "4\nFragment fragment_1; Charge=0; Multiplicity=1\nH    0.0 0.0 0.0\nH    1.0 1.0 1.0\n",
        )
