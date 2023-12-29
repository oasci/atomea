try:
    import MDAnalysis as mda

    HAS_MDANALYSIS = True
except ImportError:
    HAS_MDANALYSIS = False
from typing import Any, Generator

from collections import defaultdict
from collections.abc import Collection

import numpy as np
import numpy.typing as npt

from ..schema import Atomea
from .digester import Digester


def accumate_things(*args, **kwargs):
    return list(*args)


class MDAnalysisDigester(Digester):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def checks():
        if not HAS_MDANALYSIS:
            raise ImportError("MDAnalysis is not installed")

    @classmethod
    def digest(
        cls, atomea: Atomea, *args: Any, **kwargs: Collection[Any]
    ) -> dict[str, Any]:
        """Digest simulations supported by [MDAnalysis](https://www.mdanalysis.org/)."""
        data_all: dict[str, Any] = defaultdict(list)
        for data in cls.digestStep(atomea, *args, **kwargs):
            for k, v in data.items():
                data_all[k].append(v)
        return data_all

    @classmethod
    def digestStep(
        cls, atomea: Atomea, *args: Any, **kwargs: Collection[Any]
    ) -> Generator[dict[str, Any], None, None]:
        cls.checks()
        u: mda.Universe = mda.Universe(*args, **kwargs)
        schema = atomea.get()
        for _ in u.trajectory:
            data: dict[str, Any] = {}
            for k in schema.keys():
                try:
                    data[k] = getattr(cls, k)(u)
                except AttributeError as e:
                    raise NotImplementedError(f"{k} not implemented") from e
            yield data

    @staticmethod
    def coordinates(u: mda.Universe) -> npt.NDArray[np.float64]:
        """Return the coordinates of the atoms in the universe."""
        v = u.atoms.positions
        if isinstance(v, np.ndarray):
            return v
        raise TypeError(f"{type(v)} is not a numpy array")

    @staticmethod
    def ff_atom_type(u: mda.Universe) -> list[str]:
        """Return the coordinates of the atoms in the universe."""
        atom_types: list[str] = u.atoms.accumulate("types", function=accumate_things)
        return atom_types
