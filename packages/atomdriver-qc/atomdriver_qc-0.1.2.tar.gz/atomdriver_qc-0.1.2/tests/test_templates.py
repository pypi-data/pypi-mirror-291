#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from atomdriver.templating import get_default_template
from tests._util import TempDirTestCase, make_system


class TemplatingTestCases(TempDirTestCase):
    def setUp(self) -> None:
        self.sys = make_system(
            atoms=3,
            ghost_atoms=2,
        )
        self.atom = self.sys[0]
        self.ghost_atom = self.sys[3]
        self.template = get_default_template()

    def test_Atom(self):
        atom_str = self.template.atom_to_string(self.atom)
        self.assertEqual(atom_str, " H    0.0 0.0 0.0")

    def test_GhostAtom(self):
        ghost_atom_str = self.template.atom_to_string(self.ghost_atom)
        self.assertEqual(ghost_atom_str, "@H    0.0 0.0 0.0")

    def test_System(self):
        frag_str = self.template.system_to_string(self.sys, name="fragment_1")
        self.assertEqual(
            "fragment_1: n_atoms=5; \n\n0 2\n H    0.0 0.0 0.0\n H    1.0 1.0 1.0\n H    2.0 2.0 2.0\n@H    0.0 0.0 0.0\n@H    1.0 1.0 1.0\n",
            frag_str,
        )
