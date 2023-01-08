"""File sources."""
from pathlib import Path

import pandas as pd

from .base import Source


class StandardPortfolio(Source):
    """
    Excel sheet with Name, Ticker, Target, Actual, Price and Group columns.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(
            self.path, ["Name", "Ticker", "Target", "Actual", "Price", "Group"]
        )

    def read(self):
        return pd.read_excel(self.path)


class LayoutError(Exception):
    """Exception raised when the file does not have the expected columns."""


class LastUpdateError(Exception):
    """Exception raised when the file is not up to date."""


def _check_extension(path, extension: str):
    if not path.suffix.endswith(extension):
        raise LayoutError(f"Extension {extension} is expected in file {path}.")


def _check_layout(path: Path, columns: list) -> None:
    if path.suffix.endswith("xlsx"):
        data = pd.read_excel(path)
    else:
        raise RuntimeError(f"File extension not supported: {path}.")
    if not set(columns).issubset(set(data.columns)):
        raise LayoutError(f"Columns {columns} are expected in file {path}.")
