import pandas as pd
from pandas.testing import assert_frame_equal
from pandera.errors import SchemaErrors

from compass import step
from compass.exception import CompassException


def test_validate_convert():
    expected = pd.DataFrame(
        {
            "Name": [
                "1.0",
                "2.0",
            ],
            "Ticker": ["1", "2"],
            "Target": [0.2, 0.8],
            "Actual": [1, 2],
            "Price": [1.0, 2.0],
            "Group": ["1.0", None],
        }
    )
    # Change column types as a possible wrong type inference done by the input spreadsheet
    input_ = expected.astype(
        {
            "Name": float,
            "Ticker": int,
            "Target": str,
            "Actual": float,
            "Price": int,
            "Group": float,
        }
    )
    output = step.Validate().run(input_)
    # Check if step convert types back to the original ones
    assert_frame_equal(expected, output)


def test_validate_error():
    # Set many cells with invalid values
    input_ = pd.DataFrame(
        {
            "Name": [None, "1.0", "2.0"],  # None is invalid
            "Ticker": [None, "1", "2"],  # None is invalid
            "Target": [
                None,
                -0.2,
                1.8,
            ],  # None is invalid, negative is invalid, greater than 1 is invalid
            "Actual": [None, -1, 2.5],  # None is invalid, negative is invalid
            "Price": [None, -1.0, 2.0],  # None is invalid, negative is invalid
            "Group": [None, "1.0", None],
        }
    )
    # Expected failure cases
    expected = pd.DataFrame(
        {
            "column": [
                "Actual",
                "Name",
                "Ticker",
                "Target",
                "Target",
                "Target",
                "Target",
                "Actual",
                "Actual",
                "Actual",
                "Actual",
                "Price",
                "Price",
            ],
            "check": [
                "coerce_dtype('int64')",  # Actual
                "not_nullable",  # Name
                "not_nullable",  # Ticker
                "not_nullable",  # Target
                "greater_than_or_equal_to(0)",  # Target
                "less_than_or_equal_to(1)",  # Target
                "sum_one",  # Target
                "not_nullable",  # Actual
                "dtype('int64')",  # Actual
                "greater_than_or_equal_to(0)",  # Actual
                "not_fractionable",  # Actual
                "not_nullable",  # Price
                "greater_than_or_equal_to(0)",  # Price
            ],
        }
    )
    try:
        step.Validate().run(input_)
        assert False, "SchemaErrors are expected."
    except CompassException as ex:
        assert SchemaErrors == type(ex.__cause__)
        assert 13 == len(ex.__cause__.failure_cases)
        assert_frame_equal(expected, ex.__cause__.failure_cases[["column", "check"]])
