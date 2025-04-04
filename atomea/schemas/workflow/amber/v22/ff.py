from typing import Literal

from pydantic import Field

from atomea.schemas.workflow import ForcefieldSchemaBase


class Amber22Forcefield(ForcefieldSchemaBase):
    protein: (
        Literal[
            "ff19SB",
            "ff14SB",
            "ff99SB",
            "ff15ipq",
            "fb15",
            "ff03ua",
        ]
        | None
    ) = Field(default=None)
    r"""Options for protein force fields.

    -   [ff19SB](https://md.crumblearn.org/mm/examples/protein/sb/19/)
    -   [ff14SB](https://md.crumblearn.org/mm/examples/protein/sb/14/)
    -   [ff99SB](https://md.crumblearn.org/mm/examples/protein/sb/99/)
    -   [ff15ipq](https://md.crumblearn.org/mm/examples/protein/ipq/15/)
    -   [fb15](https://md.crumblearn.org/mm/examples/protein/fb/15/)
    -   ff03ua
    """

    water: (
        Literal[
            "tip4p",
            "tip4pew",
            "tip5p",
            "spce",
            "spceb",
            "opc",
            "opc3",
            "opc3pol",
            "pol3",
            "tip3pfb",
            "tip4pfb",
        ]
        | None
    ) = Field(default=None)
    r"""Options for water force fields."""
