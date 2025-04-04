from pydantic import Field

from atomea.schemas.workflow.amber import AmberSchemaBase
from atomea.schemas.workflow.amber.v20 import (
    Amber20CLI,
    Amber20Forcefield,
    Amber20Inputs,
)


class Amber20Schema(AmberSchemaBase):
    r"""Amber 20 schema for simulation contexts."""

    inputs: Amber20Inputs = Field(default_factory=Amber20Inputs)

    cli: Amber20CLI = Field(default_factory=Amber20CLI)

    ff: Amber20Forcefield = Field(default_factory=Amber20Forcefield)
