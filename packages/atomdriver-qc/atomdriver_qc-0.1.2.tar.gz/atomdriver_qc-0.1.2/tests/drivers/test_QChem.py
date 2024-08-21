#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from textwrap import dedent

from conformer.systems import System
from conformer_core.records import RecordStatus

from atomdriver.drivers.qchem import QChem
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.qchem_outfiles import (
    TEST_BAD_MULT,
    TEST_CCSD_OUT,
    TEST_CCSDT_OUT,
    TEST_GRAD_OUT,
    TEST_MP2_OUT,
    TEST_WB97XV_OUT,
    TEST_WB97XV_OUT_NO_SCFMAN,
)
from tests.drivers.util import H2


class QChemTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = QChem()
        self.backend.configure()  # Load template
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()
        return super().tearDown()

    def test_atom(self):
        atom = self.sys[0]
        self.assertEqual(
            self.backend.template.atom_to_string(atom),
            "H    0.00000000 0.00000000 0.00000000",
        )

    def test_ghost_atom(self):
        atom = self.sys[2]
        self.assertEqual(
            self.backend.template.atom_to_string(atom),
            "@H    0.00000000 0.00000000 0.00000000",
        )

    def test_template(self):
        out_templ = self.backend.template.system_to_string(self.sys, name="fragment_1")
        self.assertEqual(
            out_templ,
            dedent(
                """\
            ! Name: fragment_1
            $molecule
            0 1 
            H    0.00000000 0.00000000 0.00000000
            H    1.00000000 1.00000000 1.00000000
            @H    0.00000000 0.00000000 0.00000000
            @H    1.00000000 1.00000000 1.00000000
            $end

            $rem
                basis 6-31G
                method HF
                job_type sp
            $end
            """
            ),
        )

    def test_errors(self):
        backend = QChem.from_options()
        backend.configure()
        rec = backend.mk_record(System(atoms=[]))
        ctx = backend.mk_context(rec)
        with open(TEST_BAD_MULT, "r") as f:
            _ = backend.get_properties(ctx, [f])
        self.assertEqual(rec.status, RecordStatus.FAILED)
        self.assertIn(" Q-Chem fatal error", rec.meta["error"])

    def test_DFT_properties(self):
        rec = self.backend.mk_record(System(atoms=[]))
        ctx = self.backend.mk_context(rec)
        with open(TEST_WB97XV_OUT, "r") as f:
            props = self.backend.get_properties(ctx, [f])
        self.assertEqual(len(rec.meta["warnings"]), 1)
        self.assertEqual(
            rec.meta["warnings"][0],
            "Warning:  Energy on first SCF cycle will be non-variational",
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.30736459065521,
                "dft_exchange": -0.19132616115182,
                "dft_correlation": -0.03594325243512,
                "total_coulomb_energy": 0.96514412043875,
                "one_electron_int": -1.82894628401205,
                "total_scf_energy": -1.0496965291,
                "total_energy": -1.0496965291,
                "cpu_time": 11.87,
            },
        )

    def test_gradient(self):
        sys = System.from_tuples(
            [
                ("O", 0.0000000000, 0.0000000000, 0.0000000000),
                ("H", 0.0000000000, 0.0000000000, 0.9472690000),
                ("H", 0.9226720317, 0.0000000000, -0.2622325328),
                ("O", 2.6471478408, 0.3844315763, -0.9182749348),
                ("H", 3.1174655443, -0.2510444530, -1.4399583931),
                ("H", 2.4898165091, 1.1358441907, -1.4932568902),
                ("H", -0.7410073392, 1.4056351087, -1.0422511992),
                ("O", -0.8926504046, 2.1871551862, -1.5770641709),
                ("H", -1.3211437399, 2.8135423867, -1.0103863394),
                ("H", 0.8272292940, 2.5359868450, -2.2596898885),
                ("O", 1.7290565094, 2.4955238008, -2.5842220902),
                ("H", 1.6540997866, 2.3948478946, -3.5233223240),
            ]
        )
        with open(TEST_GRAD_OUT, "r") as f:
            ctx = self.backend.system_context(sys)
            props = self.backend.get_properties(ctx, [f])
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 138.50530341,
                "one_electron_int": -695.7229525654,
                "total_coulomb_energy": 288.9931360924,
                "hf_exchange": -35.8639156754,
                "nuclear_attraction": -999.104564156,
                "kinetic_energy": 303.3816115906,
                "total_scf_energy": -304.08842873,
                "total_energy": -304.08842873,
                "nuclear_gradient": {
                    "shape": (12, 3),
                    "dtype": "float64",
                    "data": [
                        2.54e-05,
                        7.36e-05,
                        -0.0001867,
                        -0.000114,
                        1.71e-05,
                        4.01e-05,
                        4e-05,
                        -5.5e-05,
                        0.0002675,
                        -2.42e-05,
                        2.12e-05,
                        -2.59e-05,
                        5.7e-05,
                        7.65e-05,
                        -6.99e-05,
                        5.93e-05,
                        -0.0001437,
                        -5.73e-05,
                        0.0001755,
                        7.9e-06,
                        -0.0002081,
                        -0.000121,
                        0.0001165,
                        0.0001042,
                        -3.35e-05,
                        -7.13e-05,
                        -1e-05,
                        -5.73e-05,
                        2.16e-05,
                        6.93e-05,
                        0.0001621,
                        4.6e-05,
                        7.28e-05,
                        -0.0001693,
                        -0.0001104,
                        3.9e-06,
                    ],
                },
                "cpu_time": 14.0,
            },  # fmt: skip
        )

    def test_no_scfman_properties(self):
        with open(TEST_WB97XV_OUT_NO_SCFMAN, "r") as f:
            props = self.backend.get_properties(None, [f])
            self.maxDiff = None
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.3073645906,
                "dft_exchange": -0.1913261612,
                "dft_correlation": -0.0359432524,
                "total_coulomb_energy": 0.9651441204,
                "one_electron_int": -1.828946284,
                "kinetic_energy": 0.7760006951,
                "nuclear_attraction": -2.6049469792,
                "total_scf_energy": -1.04969653,
                "total_energy": -1.04969653,
                "cpu_time": 12.18,
            },
        )

    def test_MP2_properties(self):
        # TEST MP2 template
        backend = QChem.from_options(
            template=dedent(
                """\
        ! Name: {name}
        $molecule
        0 1
        {geometry}
        $end
        $rem
            basis aug-cc-pVTZ
            method mp2
            job_type sp
        $end
        """
            ),
        )
        backend.configure()
        with open(TEST_MP2_OUT, "r") as f:
            props = backend.get_properties(None, [f])
        backend.cleanup()
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.55072907976639,
                "one_electron_int": -1.80515692871430,
                "total_correlation_energy": -0.04659996,
                "total_coulomb_energy": 1.10145815953278,
                "total_energy": -0.95228817,
                "total_scf_energy": -0.9056882102,
                "cpu_time": 3.54,
            },
        )

    def test_CCSD_properties(self):
        backend = QChem.from_options(
            template=dedent(
                """\
        ! Name: {name}
        $molecule
        0 1
        {geometry}
        $end
        $rem
            basis aug-cc-pVTZ
            method CCSD
            job_type sp
        $end
        """
            ),
        )
        backend.configure()
        with open(TEST_CCSD_OUT, "r") as f:
            props = backend.get_properties(None, [f])
        backend.cleanup()
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.47394666363846,
                "one_electron_int": -1.82166189958895,
                "total_correlation_energy": -0.06033663,
                "total_coulomb_energy": 0.94789332727691,
                "total_energy": -1.05931223,
                "total_scf_energy": -0.9989755972,
                "cpu_time": 10.14,
            },
        )

    def test_CCSD_T_properties(self):
        backend = QChem.from_options(
            template=dedent(
                """\
        ! Name: {name}
        $molecule
        0 1
        {geometry}
        $end
        $rem
            basis = aug-cc-pVTZ
            method = CCSD(T)
            job_type = sp
        $end
        """
            ),
        )
        backend.configure()
        with open(TEST_CCSDT_OUT, "r") as f:
            props = backend.get_properties(None, [f])
        backend.cleanup()
        self.assertDictEqual(
            props.to_dict(),
            {
                "nuclear_repulsion": 0.34873964,
                "hf_exchange": -0.55072907976639,
                "one_electron_int": -1.80515692871430,
                "total_correlation_energy": 0.00000000,
                "total_coulomb_energy": 1.10145815953278,
                "total_energy": -0.99540333,
                "total_scf_energy": -0.9056882102,
                "cpu_time": 9.04,
            },
        )
    
    def test_pinned_info(self):
        # JONAH - Tests the pinned_atoms and pinned_coords scripts on a system
        pinned_sys = make_system(atoms=2, pinned_atoms=2)
        self.assertEqual(
            QChem.pinned_idxs(pinned_sys),
            '''3 4 '''
        )
        self.assertEqual(
            QChem.pinned_coords(pinned_sys),
            '''3 0.00000000 0.00000000 0.00000000\n4 1.00000000 1.00000000 1.00000000\n'''
        )

    @unittest.skipIf(not QChem.is_available(), "Could not find QChem exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.10859, 5)
