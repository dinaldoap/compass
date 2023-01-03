"""File sources."""
from pathlib import Path

import pandas as pd

from .base import Source

_CHANGE_RENAME = {
    "Data do Negócio": "Date",
    "Tipo de Movimentação": "Transaction",  # Compra == Deposit and Venda == Withdraw
    "Código de Negociação": "Ticker",
    "Quantidade": "Change",
    "Preço": "Price",
}
_CHANGE_COLUMNS = _CHANGE_RENAME.keys()
_CHANGE_TYPES = {
    "Change": int,
    "Price": float,
}


class StandardTarget(Source):
    """
    Excel sheet with Name, Ticker and Target columns.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, ["Name", "Ticker", "Target", "Group"])

    def read(self):
        return pd.read_excel(self.path)


class StandardActual(Source):
    """
    Excel sheet with Ticker and Actual columns.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, ["Ticker", "Actual"])

    def read(self):
        return pd.read_excel(self.path)


class StandardPrice(Source):
    """
    Excel sheet with Ticker and Price columns.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, ["Ticker", "Price"])

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
