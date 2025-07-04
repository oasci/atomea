from typing import TypeAlias

import numpy as np
import numpy.typing as npt
import polars as pl

PassableData: TypeAlias = npt.NDArray[np.generic] | pl.DataFrame
"""Core data types that we stick to passing around functions. All functions working
with data should accept and/or return data of this type.

All stores should return one of these types.
"""
OptionalPassableData: TypeAlias = npt.NDArray[np.generic] | pl.DataFrame | None
