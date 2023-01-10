"""Init step."""

import pandas as pd

from .base import Step


class Init(Step):
    """Step which generates the default portfolio."""

    def run(self, input_: pd.DataFrame):
        """Initilize files.

        Returns
        -------
        pandas.DataFrame
            DataFrame corresponding to the default portfolio. See @__main__ for details about the porfolio spreadsheet.
        """
        output = pd.DataFrame(
            {
                "Name": [
                    "Stocks",
                    "Bonds",
                ],
                "Ticker": ["STCK", "BOND"],
                "Target": [0.6, 0.4],
                "Actual": [0, 0],
                "Price": [1, 1],
                "Group": [None, None],
            }
        )
        return output
