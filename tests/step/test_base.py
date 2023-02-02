import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from compass import source, step, target


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
