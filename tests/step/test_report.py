import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from compass.step.report import _to_percentage


@pytest.mark.parametrize(
    "data,         percentages",
    [
        ([0, 0], [0.0, 0.0]),  # Replace NaN with 0
        ([1, 0], [1.0, 0.0]),  #
        ([1, 1], [0.5, 0.5]),  #
    ],
)
def test_to_percentage(data, percentages):
    output = _to_percentage(pd.Series(data))
    assert_series_equal(pd.Series(percentages), output)
