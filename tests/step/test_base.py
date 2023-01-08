import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from compass import source, step, target
from compass.source import Source
from compass.step import Join, LengthChangedError


class SourceMock(Source):
    def read(self):
        # BIEF39 is missing value
        return pd.DataFrame({"Ticker": ["BITO39"], "Actual": [1]})


def test_join():
    input = pd.DataFrame(
        {
            "Ticker": ["BITO39", "BIEF39"],
            "Target": [0.2, 0.8],
        }
    )
    expected = pd.DataFrame(
        {"Ticker": ["BITO39", "BIEF39"], "Target": [0.2, 0.8], "Actual": [1, 2]}
    )
    # Left join requires filling BIEF39's actual
    output = Join(source=SourceMock(), on="Ticker", fillna={"Actual": 2}).run(input)
    assert_frame_equal(expected, output)
    # Inner join only outputs BITO39
    output = Join(source=SourceMock(), on="Ticker", how="inner").run(input)
    assert_frame_equal(expected.query("Ticker == 'BITO39'"), output)
    # Stricted inner join raises exception
    with pytest.raises(LengthChangedError):
        output = Join(source=SourceMock(), on="Ticker", how="inner", strict=True).run(
            input
        )
    # Filter input by input.Ticker in source.Tickers
    output = Join(source=SourceMock(), on="Ticker", add=[], how="inner").run(input)
    assert_frame_equal(
        expected.query("Ticker == 'BITO39'").pipe(lambda df: df[input.columns]), output
    )


def test_read_source():
    expected = pd.DataFrame(
        {
            "Name": [
                "iShares Core S&P Total US Stock Market ETF",
                "iShares Core MSCI EAFE ETF",
            ],
            "Ticker": ["BITO39", "BIEF39"],
            "Target": [0.2, 0.8],
            "Actual": [1, 2],
            "Price": [1, 2],
            "Group": ["A", None],
        }
    )
    output = step.ReadSource(
        source=source.StandardPortfolio(path="tests/data/portfolio.xlsx")
    ).run(None)
    assert_frame_equal(expected, output)


def test_write_target(tmp_path):
    expected = pd.DataFrame(
        {
            "Name": [
                "iShares Core S&P Total US Stock Market ETF",
                "iShares Core MSCI EAFE ETF",
            ],
            "Ticker": ["BITO39", "BIEF39"],
            "Target": [0.2, 0.8],
            "Actual": [1, 2],
            "Price": [1, 2],
            "Group": ["A", None],
        }
    )
    filename = tmp_path.joinpath("output.xlsx")
    output = step.WriteTarget(target=target.file.Standard(path=filename)).run(expected)
    assert_frame_equal(expected, output)
    output = step.ReadSource(source=source.StandardPortfolio(filename)).run(None)
    assert_frame_equal(expected, output)
