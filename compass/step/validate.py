"""Validate step."""

import math
from typing import cast

import pandas as pd
import pandera as pa
from pandera.errors import SchemaErrors
from pandera.typing import DataFrame, Series

from compass.exception import CompassException

from .base import Step


class Validate(Step):
    """Step which validates the portfolio data."""

    def __init__(self):
        pass

    def run(self, input_: pd.DataFrame):
        """Validate the portfolio data.

        Parameters
        ----------
        input : pandas.DataFrame
            DataFrame with the following columns:
                Name : str
                    Description of the ticker.
                Ticker : str
                    Ticker name.
                Target : float
                    Fraction of the wealth that must be allocated in the asset.
                Actual : int
                    Number of asset's units currently owned.
                Price : float
                    Curent price of the asset.
                Group : str
                    Group of the ticker.

        Returns
        -------
        pandas.DataFrame
            DataFrame with the same columns of ``input_``. The columns which does not match the expected types are converted.

        Raises:
            RuntimeError: When the input schema is not as expected, and it is not possible to convert it to the expected one.
        """
        try:
            return _transform(input_)
        except SchemaErrors as ex:
            raise CompassException(
                f"Input data with invalid schema. Please review the columns and errors showed below. Fix the first check/error of each column and try again.\n{ex.failure_cases}"
            ) from ex


class PortfolioSchema(pa.DataFrameModel):
    """Portfolio's data schema."""

    Name: Series[str] = pa.Field(coerce=True)
    Ticker: Series[str] = pa.Field(coerce=True)
    Target: Series[float] = pa.Field(ge=0, le=1, coerce=True)
    Actual: Series[int] = pa.Field(ge=0, coerce=True)
    Price: Series[float] = pa.Field(ge=0, coerce=True)
    Group: Series[str] = pa.Field(coerce=True, nullable=True)

    @pa.check("Target", name="sum_one")
    def _sum_one(self, column: Series[float]) -> Series[bool]:
        return cast(Series[bool], math.isclose(column.sum(), 1))

    @pa.check("Actual", name="not_fractionable")
    def _not_fractionable(self, column: Series[float]) -> Series[bool]:
        return cast(Series[bool], column % 1 == 0)


@pa.check_types(lazy=True)
def _transform(input_: DataFrame[PortfolioSchema]) -> DataFrame[PortfolioSchema]:
    return input_
