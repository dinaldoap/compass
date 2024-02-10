"""File sources."""

from pathlib import Path

import pandas as pd

from compass.exception import CompassException

from .base import Source

_EXTENSION = "xlsx"


class StandardPortfolio(Source):
    """
    Excel sheet with Name, Ticker, Target, Actual, Price and Group columns.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path)
        _check_layout(
            self.path, ["Name", "Ticker", "Target", "Actual", "Price", "Group"]
        )

    def read(self):
        return pd.read_excel(self.path)


def _check_extension(path):
    if not path.suffix.endswith(_EXTENSION):
        raise CompassException(f"Extension {_EXTENSION} is expected in file {path}.")


def _check_layout(path: Path, columns: list):
    if not path.suffix.endswith(_EXTENSION):
        raise ValueError(f"File extension {path} not supported.")
    data = pd.read_excel(path)
    if not set(columns).issubset(set(data.columns)):
        raise CompassException(f"Columns {columns} are expected in file {path}.")
