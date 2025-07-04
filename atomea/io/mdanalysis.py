import inspect

import numpy as np
from loguru import logger

try:
    import MDAnalysis as mda
    from MDAnalysis.guesser.tables import SYMB2Z

    HAS_MDANALYSIS = True
except ImportError:
    HAS_MDANALYSIS = False

from typing import Any

from atomea.containers import Project
from atomea.io import Reader


class MDAnalysisReader(Reader):
    """
    Read data via MDAnalysis.
    """

    @classmethod
    def checks(cls) -> None:
        if not HAS_MDANALYSIS:
            raise ImportError("MDAnalysis is required for MDAnalysisReader")

    @classmethod
    def prepare(
        cls, topology: str, trajectory: str, *args: Any, **kwargs: Any
    ) -> dict[str, Any]:
        """Load a single Universe."""
        u = mda.Universe(topology, trajectory, *args, **kwargs)
        return {"u": u}

    @classmethod
    def extract(cls, prj: Project, id_ens: str, id_run, ctx: dict[str, Any]) -> Project:
        """Extract and parse all possible information given the context.
        This method is responsible for calling all other methods.
        """
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not name.startswith("parse_"):
                continue
            logger.debug(f"[{id_ens}] running parser `{name}`")
            try:
                prj = method(prj, id_ens, ctx)
            except Exception:
                logger.exception(f"[{id_ens}] error in parser `{name}`")
        return prj

    @staticmethod
    def parse_ensemble_metadata(
        prj: Project, ens_id: str, ctx: dict[str, Any]
    ) -> Project:
        """Store per‐ensemble atom symbols & ff types once."""
        u = ctx["u"]
        syms = np.array(u.atoms.elements, dtype=np.dtype(np.str_))
        prj.ensembles[ens_id].microstates.atom_symbol = syms
        types = np.array(u.atoms.types, dtype=np.dtype(np.str_))
        prj.ensembles[ens_id].topology.ff_atom_type = types
        ids_component = np.array(u.atoms.resids, dtype=np.dtype(np.uint32))
        prj.ensembles[ens_id].topology.ids_component = ids_component
        labels_component = np.array(u.atoms.resnames, dtype=np.dtype(np.str_))
        prj.ensembles[ens_id].topology.labels_component = labels_component
        return prj

    @staticmethod
    def parse_coordinates(prj: Project, ens_id: str, ctx: dict[str, Any]) -> Project:
        """Stack all frames into a (n_frames,n_atoms,3) array."""
        u = ctx["u"]
        coords = [ts.positions.copy() for ts in u.trajectory]
        arr = np.stack(coords, axis=0)
        # this writes a 3D microstate array
        prj.ensembles[ens_id].microstates.coordinates = arr
        return prj

    @staticmethod
    def parse_atom_z(prj: Project, ens_id: str, ctx: dict[str, Any]) -> Project:
        """Store the atomic numbers as an ensemble‐level array."""
        u = ctx["u"]
        zs = np.array([SYMB2Z.get(sym, 0) for sym in u.atoms.elements])
        prj.ensembles[ens_id].microstates.atom_z = zs
        return prj
