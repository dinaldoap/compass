"""File source step."""
import datetime as dt
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


class Change(Source):
    """
    Excel sheet with data downloaded from Área Logada do Investidor (https://www.investidor.b3.com.br/).
    The columns Data do Negociação, Código de Negociação, Quantidade and Preço are, respectivelly, renamed to Date, Ticker, Change and Price.

    ...
    """

    def __init__(self, path: Path, date=dt.date.today()):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, _CHANGE_COLUMNS)

    def read(self) -> pd.DataFrame:
        data = (
            pd.read_excel(
                self.path,
                parse_dates=["Data do Negócio"],
                date_parser=lambda txt: dt.datetime.strptime(txt, "%d/%m/%Y"),
            )
            .pipe(lambda df: df[_CHANGE_COLUMNS])
            .rename(_CHANGE_RENAME, axis="columns")
            .astype(_CHANGE_TYPES)
            .assign(
                Change=lambda df: (
                    (df["Transaction"] == "Compra")
                    + (df["Transaction"] == "Venda") * -1
                )
                * df["Change"]
            )
            .pipe(lambda df: df[["Date", "Ticker", "Change", "Price"]])
            .set_index("Date")
        )
        return data


class DirectoryChange(Source):
    """
    Directory with multiples change files.
    See @Change class.

    ...
    """

    def __init__(self, path: Path, date=dt.date.today()):
        self.path = Path(path)
        self.date = date
        _check_directory(self.path)

    def read(self) -> pd.DataFrame:
        data = [Change(file, self.date) for file in self.path.iterdir()]
        data = [change.read() for change in data]
        data = pd.concat(data)
        return data


class LayoutError(Exception):
    pass


class LastUpdateError(Exception):
    pass


def _check_extension(path, extension: str):
    if not path.suffix.endswith(extension):
        raise LayoutError(
            "Extension {} is expected in file {}.".format(extension, path)
        )


def _check_directory(path: Path):
    if not path.exists():
        raise LayoutError("{} does not exists.".format(path))
    if not path.is_dir():
        raise LayoutError("{} is expected to be a directory.".format(path))
    if not list(path.iterdir()):
        raise LayoutError("{} is expected to have xlsx files.".format(path))


def _check_layout(path: Path, columns: list) -> None:
    if path.suffix.endswith("xlsx"):
        data = pd.read_excel(path)
    else:
        raise RuntimeError("File extension not supported: {}.".format(path))
    if not set(columns).issubset(set(data.columns)):
        raise LayoutError("Columns {} are expected in file {}.".format(columns, path))


def _check_last_update(path: Path, expected_date: dt.date) -> None:
    if expected_date is None:
        return
    last_update = dt.date.fromtimestamp(path.stat().st_mtime)
    if last_update < expected_date:
        raise LastUpdateError(
            "{} is out of date. Last update is expected to be at {} or later.".format(
                path, expected_date
            )
        )
