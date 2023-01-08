import pandas as pd
from pandas.testing import assert_frame_equal

from compass import source, target


def test_Standard(tmp_path):
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
    output = target.file.Standard(filename).write(expected)
    assert None == output
    output = source.file.StandardPortfolio(filename).read()
    assert_frame_equal(expected, output)
