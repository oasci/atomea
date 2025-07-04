from typing import TYPE_CHECKING

from atomea.containers import AtomeaContainer
from atomea.containers.atomistic import Microstates, Topology

if TYPE_CHECKING:
    from atomea.containers import Project


class Ensemble(AtomeaContainer):
    """
    The `Ensemble` class represents a collection of molecular structures,
    each referred to as a microstate. This class is used to
    manage and validate an ensemble of molecular data, facilitating the handling of
    multiple molecular configurations, such as those produced during atomistic
    calculations.

    Only data that could reasonably change shape or dimensions between ensembles
    (due to different numbering or ordering of atoms) should be stored here. All other
    data should be stored in a [`Project`][schemas.Project].
    """

    def __init__(self, ensemble_id: str, parent: "Project") -> None:
        self.id: str = ensemble_id
        self._parent = parent

        # Initialize components with parent reference
        self.microstates = Microstates(self)

        self.topology = Topology(self)

    def __repr__(self) -> str:
        return f"<Ensemble id={self.id!r}>"
