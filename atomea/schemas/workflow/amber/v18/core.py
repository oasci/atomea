from pydantic import Field

from atomea.schemas.workflow.amber import AmberSchemaBase
from atomea.schemas.workflow.amber.v18 import (
    Amber18CLI,
    Amber18Forcefield,
    Amber18Inputs,
)


class Amber18Schema(AmberSchemaBase):
    r"""Amber 18 schema for simulation contexts."""

    inputs: Amber18Inputs = Field(default_factory=Amber18Inputs)

    cli: Amber18CLI = Field(default_factory=Amber18CLI)

    ff: Amber18Forcefield = Field(default_factory=Amber18Forcefield)
