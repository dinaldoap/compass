import pandas as pd
from pandas.testing import assert_frame_equal

from compass import source


def test_StandardPortfolio():
    output = source.file.StandardPortfolio("tests/data/portfolio.xlsx").read()
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
    assert_frame_equal(expected, output)
