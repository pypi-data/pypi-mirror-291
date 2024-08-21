#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from textwrap import dedent
from typing import Union

from conformer.systems import Atom, System

DEFAULT_SYSTEM = """\
    {name}: n_atoms={n_atoms}; {info}

    {charge} {mult}
    {geometry}
"""
DEFAULT_ATOM = " {symbol}    {x} {y} {z}"
DEFAULT_GHOST_ATOM = "@{symbol}    {x} {y} {z}"


class SystemTemplate(object):
    def __init__(
        self,
        template=None,
        atom=None,
        ghost_atom=None,
    ) -> None:
        self.template = dedent(template) if template else None
        self.atom = atom
        self.ghost_atom = ghost_atom

    def override(self, **kwargs):
        for k, v in kwargs.items():
            if v is None:
                continue
            setattr(self, k, v)

    def system_to_string(self, sys: System, **kwargs) -> str:
        atom_strs = [self.atom_to_string(a) for a in sys]
        geometry = "\n".join(atom_s for atom_s in atom_strs if atom_s is not None)

        name = kwargs.pop("name", sys.name)
        info = kwargs.pop("info", "")

        cpus = kwargs.pop("cpus", 1)
        total_memory = kwargs.pop("total_memory", 8000)
        memory_per_cpu = kwargs.pop("memory_per_cpu", None)
        if not memory_per_cpu:
            memory_per_cpu = int(total_memory / cpus)

        # TODO: add additional fields to the template
        fragment_str = self.template.format(
            name=name,
            info=info,
            n_atoms=sys.size,
            charge=sys.charge,
            mult=sys.multiplicity,
            geometry=geometry,
            cpus=cpus,
            total_memory=total_memory,
            memory_per_cpu=memory_per_cpu,
            **kwargs,
        )
        return fragment_str

    def atom_to_string(self, a: Atom) -> Union[str, None]:
        if not a.is_physical:
            template = self.ghost_atom
        else:
            template = self.atom

        if not template:
            return None

        return template.format(symbol=a.t, x=a.r[0], y=a.r[1], z=a.r[2])


def get_default_template():
    return SystemTemplate(
        template=DEFAULT_SYSTEM,
        atom=DEFAULT_ATOM,
        ghost_atom=DEFAULT_GHOST_ATOM,
    )
