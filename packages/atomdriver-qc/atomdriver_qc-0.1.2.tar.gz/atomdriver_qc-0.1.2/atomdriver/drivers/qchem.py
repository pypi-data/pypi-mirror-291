#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import re
from datetime import datetime
from os import environ, path
from typing import List, TextIO, Tuple

import numpy as np
from conformer_core.properties.extraction import calc_property
from conformer_core.records import RecordStatus

from atomdriver.abstract_driver import RunContext, ShellCommandDriver
from atomdriver.properties import NuclearGradient

ENERGY_SEARCH_RE = r"^\s*method[ \t]*=?[ \t]*([^\s]*)"  # Connot pre-compile
ENERGY_EXPRESSIONS = {
    "mp2": re.compile(r"MP2[ \t]+[tT]otal [eE]nergy =[ \t]+(-?\d+.\d+)"),
    "rimp2": re.compile(r"RIMP2[ \t]+[tT]otal [eE]nergy =[ \t]+(-?\d+.\d+)"),
    "ccsd": re.compile(r"CCSD [tT]otal [eE]nergy[ \t]+=[ \t]+(-?\d+.\d+)"),
    "ccsd(t)": re.compile(r"CCSD\(T\) [tT]otal [eE]nergy[ \t]+=[ \t]+(-?\d+.\d+)"),
    "default": re.compile(
        r"Total energy (?:in the final basis set )?=[ \t]+(-?\d+.\d+)"
    ),
}
CORRELATION_EXPRESSION = {
    "mp2": re.compile(r"MP2[ \t]+correlation energy =[ \t]+(-?\d+.\d+)"),
    "rimp2": re.compile(r"RIMP2[ \t]+correlation energy =[ \t]+(-?\d+.\d+)"),
    "ccsd": re.compile(r"CCSD correlation energy[ \t]+=[ \t]+(-?\d+.\d+)"),
    "ccsd(t)": re.compile(r"CCSD\(T\) correlation energy[ \t]+=[ \t]+(-?\d+.\d+)"),
}
DEFAULT_ENERGY_EXPRESSION = ENERGY_EXPRESSIONS["default"]
ZERO = 1e-9

# JONAH - Regex for pinning rem variables
HARM_OPT_SEARCH_RE = r"^\s*harm_opt[ \t=]+(true|1)"
FRZN_OPT_SEARCH_RE = r"^\s*frzn_opt[ \t=]+(true|1)"


class QChem(ShellCommandDriver):
    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
            ! Name: {name}
            $molecule
            {charge} {mult} 
            {geometry}
            $end

            $rem
                basis 6-31G
                method HF
                job_type sp
            $end
        """,
        "atom": "{symbol}    {x:.8f} {y:.8f} {z:.8f}",
        "ghost_atom": "@{symbol}    {x:.8f} {y:.8f} {z:.8f}",
    }
    RUN_CMD = "qchem"

    use_pinned_atoms: bool = False

    def configure(self):
        super().configure()

        # Configure the energy expression based on the template
        m = re.search(ENERGY_SEARCH_RE, self.template.template.lower(), re.MULTILINE)

        if m is None:
            self.prop_total_energy.patterns = [DEFAULT_ENERGY_EXPRESSION]
        else:
            self.prop_total_energy.patterns = [
                ENERGY_EXPRESSIONS.get(m[1], DEFAULT_ENERGY_EXPRESSION)
            ]
            if m[1] in CORRELATION_EXPRESSION:
                self.prop_total_correlation_energy.patterns = [
                    CORRELATION_EXPRESSION[m[1]]
                ]
        #JONAH - Search for the pinned atom rem variables
        harm_opt_search = re.search(HARM_OPT_SEARCH_RE, self.template.template.lower(), re.MULTILINE)
        frzn_opt_search = re.search(FRZN_OPT_SEARCH_RE, self.template.template.lower(), re.MULTILINE)
        if harm_opt_search is not None or frzn_opt_search is not None:
            self.use_pinned_atoms = True
    
    # JONAH - Scripts that output the rem variables, pinned atom indices, and
    # pinned atom coords for a system
    
    @staticmethod
    def pinned_num(sys) -> str:
        pinned_num = 0
        for a in sys:
            if a.role.is_pinned:
                pinned_num += 1
        return pinned_num
    
    @staticmethod
    def pinned_idxs(sys) -> str:
        pinned_idxs: str = ''
        for i, a in enumerate(sys, 1):
            if a.role.is_pinned:
                pinned_idxs += f'{i} '
        return pinned_idxs

    @staticmethod
    def pinned_coords(sys) -> str:
        pinned_coords: str = ''
        for i, a in enumerate(sys, 1):
            if a.role.is_pinned:
                pinned_coords += '{:n} {:.8f} {:.8f} {:.8f}\n'.format(i, *a.r)
        return pinned_coords

    def setup_calc(self, ctx: RunContext):
        self.create_workpath(ctx)

        # Get the run command
        ctx.scratch["run_cmd"], ctx.scratch["run_args"] = self.get_run_cmd(ctx)
        environ["QCSCRATCH"] = str(ctx.workpath)

        kwargs = dict(
            num_atoms=ctx.working_system.size,
            name=ctx.working_system.name,
            time=datetime.now().isoformat(),
            backend=self.name,
            cpus=self.allocation.cpus,
            total_memory=self.allocation.memory,
            static_memory=min([int(self.allocation.memory * 0.20), 2000]),
            memory_per_cpu=int(self.allocation.memory / self.allocation.cpus),
        )

        # Harmonic confiner stuff here

        if self.use_pinned_atoms:
            kwargs.update(
                pinned_atom_num = self.pinned_num(ctx.working_system),
                pinned_atom_idxs = self.pinned_idxs(ctx.working_system),
                pinned_atom_coords = self.pinned_coords(ctx.working_system),
            )

        with ctx.files["input"].open("w") as f:
            # JONAH - This was for making sure the templates were working out ok
            # print(self.template.system_to_string(ctx.working_system, **kwargs))
            f.write(self.template.system_to_string(ctx.working_system, **kwargs))

    @classmethod
    def is_available(cls):
        QC = environ.get("QC", None)
        QCAUX = environ.get("QCAUX", None)
        if not (QC and path.exists(QC)):
            return False
        if not (QCAUX and path.exists(QCAUX)):
            return False
        return True

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.RUN_CMD, [
            "-nt",
            str(self.allocation.cpus),
            ctx.files["input"],
            ctx.files["output"],
        ]

    @calc_property(source="re_file")  # Patterns configured at runtime
    def prop_total_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Total [eE]nthalpy\s*:\s+(-?\d+.\d+)\s*"]
    )
    def prop_total_enthalpy(self, ctx: RunContext, m, _):
        """
        Properties from frequency calcualtions
        Enthalphy reported in kcal/mol
        """
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"SCF +energy in the final basis set = +(-?\d+.\d+)"],
    )
    def prop_total_scf_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"DFT +Exchange +Energy = +(-?\d+.\d+)"],
    )
    def prop_dft_exchange(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[r"DFT +Correlation +Energy = +(-?\d+.\d+)"],
    )
    def prop_dft_correlation(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[r"Total +Coulomb +Energy = +(-?\d+.\d+)"],
    )
    def prop_total_coulomb_energy(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[
            r"HF +Exchange +Energy = +(-?\d+.\d+)",
            r"Alpha +Exchange +Energy = +(-?\d+.\d+)",
        ],
    )
    def prop_hf_exchange(self, ctx: RunContext, m, stream):
        if m[0].startswith("HF"):
            return float(m[1])
        if m[0].startswith("Alph"):
            alpha = float(m[1])
            beta_str = stream.readline()
            m2 = re.match(r" Beta +Exchange +Energy = +(-?\d+.\d+)", beta_str)
            if m2:
                return alpha + float(m2[1])

    @calc_property(source="re_file")
    def prop_total_correlation_energy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"Kinetic + Energy = +(-?\d+.\d+)"],
    )
    def prop_kinetic_energy(self, ctx: RunContext, m, _):
        res = float(m[1])
        if abs(res) > ZERO:
            return res

    @calc_property(
        source="re_file",
        patterns=[r"Nuclear Repulsion Energy = +(-?\d+.\d+)"],
    )
    def prop_nuclear_repulsion(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Nuclear Attr(actions|\.) + Energy = +(-?\d+.\d+)"]
    )
    def prop_nuclear_attraction(self, ctx: RunContext, m, _):
        res = float(m[2])
        if abs(res) > ZERO:
            return float(m[2])

    @calc_property(
        source="stream",
    )
    def prop_nuclear_gradient(self, ctx: RunContext, line: str, stream: TextIO):
        if line.strip() != "Gradient of SCF Energy":
            return

        # TODO: This will likely be spun off into it's own helper function
        atom_map = []
        atom_type_map = []
        for i, a in enumerate(ctx.record.system):
            if a.is_physical:
                atom_map.append(i)
                if a.is_proxy:
                    atom_type_map.append(1)  # Proxies will take back seat
                else:
                    atom_type_map.append(0)  # Real atom

        grad = np.zeros((len(atom_map), 3), dtype=NuclearGradient.type)

        # TODO: Do some math to pre-allocate our matrix
        uncollected = len(atom_map)
        while True:
            if uncollected <= 0:  # Break when we are done
                break
            idxs = [int(i) - 1 for i in stream.readline().split()]
            xs = [float(i) for i in stream.readline().split()[1:]]
            ys = [float(i) for i in stream.readline().split()[1:]]
            zs = [float(i) for i in stream.readline().split()[1:]]

            grad[idxs, 0] += xs
            grad[idxs, 1] += ys
            grad[idxs, 2] += zs

            uncollected -= len(idxs)

        return grad

    @calc_property(
        source="re_file",
        patterns=[r"One-Electron +Energy = +(-?\d+.\d+)"],
    )
    def prop_one_electron_int(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"Total [eE]ntropy\s*:\s+(-?\d+.\d+)\s*"]
    )
    def prop_total_entropy(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(source="re_file", patterns=[r"(\d+\.\d+)s\(cpu\)"])
    def prop_cpu_time(self, ctx: RunContext, m, _):
        return float(m[1])

    @calc_property(source="re_file", patterns=[r"Q-Chem fatal error occurred *"])
    def error(self, ctx: RunContext, m, stream):
        ctx.record.status = RecordStatus.FAILED
        # Back up. QChem is bad about printing full error
        stream.seek(stream.tell() - 300)
        ctx.record.meta["error"] = "..." + stream.read()

    @calc_property(source="re_file", patterns=[r"[Ww]arning:"])
    def warnings(self, ctx: RunContext, m, _):
        if ctx is None: # This really only happens in testing
            return None
        warning = m.string.strip()
        try:
            ctx.record.meta["warnings"].append(warning)
        except KeyError:
            ctx.record.meta["warnings"] = [warning]

    @calc_property(
            source="re_file", patterns=[r"This [mM]olecule [hH]as\s+(\d+)\s+[iI]maginary [fF]requencies"]
            )
    def prop_num_imaginary_freq(self, ctx: RunContext, m, _):
        return int(m[1])

    @calc_property(
            source="re_file", patterns=[r"Zero [pP]oint [vV]ibrational [eE]nergy\s*:\s+(-?\d+.\d+)\s*"]
            )
    def prop_zero_point_energy(self, ctx: RunContext, m, _):
        return float(m[1])