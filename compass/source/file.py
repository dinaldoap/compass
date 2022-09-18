from .base import Source
from compass.number import parse_decimal

from datetime import date, datetime
import pandas as pd
from pathlib import Path
import re

_CEI_COLUMNS = ["Cód. de Negociação", "Qtde."]
_RICO_RENAME = {
    "Código": "Ticker",
    "Quantidade": "Actual",
    "Preço": "Price",
}
_RICO_COLUMNS = _RICO_RENAME.keys()
_ALI_TYPES = {
    "Código de Negociação": str,
    "Quantidade": int,
}
_ALI_RENAME = {
    "Código de Negociação": "Ticker",
    "Quantidade": "Actual",
}
_ALI_COLUMNS = _ALI_RENAME.keys()
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
_WARREN_PATTERN = r"https://warren.com.br/app/#[\/\w]*/trade"


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


class AliActual(Source):
    """
    Excel sheet with data downloaded from Área Logada do Investidor (https://https://www.investidor.b3.com.br/).
    The columns Código de Negociação and Quantidade are, respectivelly, renamed to Ticker and Actual.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, _ALI_COLUMNS)

    def read(self) -> pd.DataFrame:
        data = _read_excel(self.path)
        data = data.rename(_ALI_RENAME, axis="columns")
        data = data.groupby(by="Ticker", as_index=False, sort=False).agg(
            {"Actual": "sum"}
        )
        return data


class CeiHtmlActual(Source):
    """
    HTML file with data from Home Page -> Investimentos -> Carteira de ativos -> Consultar of Canal Eletrônico do Investidor (https://cei.b3.com.br/CEI_Responsivo/ConsultarCarteiraAtivos.aspx).
    The columns Cód. de Negociação and Qtde. are, respectivelly, renamed to Ticker and Actual.

    ...
    """

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        _check_extension(self.path, "html")
        _check_pattern_layout(
            self.path,
            "https://cei.b3.com.br/CEI_Responsivo/ConsultarCarteiraAtivos.aspx",
        )
        _check_layout(self.path, _CEI_COLUMNS)
        _check_last_update(self.path, date)

    def read(self) -> pd.DataFrame:
        data = _read_html(self.path, _CEI_COLUMNS)
        data = data.rename(
            {
                "Cód. de Negociação": "Ticker",
                "Qtde.": "Actual",
            },
            axis="columns",
        )
        data["Actual"] = data["Actual"].astype(int)
        return data


class RicoHtmlActualPrice(Source):
    """
    HTML file with data from Home Page -> Ações e FIIs (https://www.rico.com.vc/arealogada/acoes).
    The columns Código, Quantidade and Price are, respectivelly, renamed to Ticker, Actual and Price.

    ...
    """

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        _check_extension(self.path, "html")
        _check_pattern_layout(self.path, "https://www.rico.com.vc/arealogada/acoes")
        _check_layout(self.path, _RICO_COLUMNS)
        _check_last_update(self.path, date)

    def read(self) -> pd.DataFrame:
        data = _read_html(self.path, _RICO_COLUMNS)
        data = data.rename(_RICO_RENAME, axis="columns")
        data = _convert_actual(data)
        data = _convert_price(data)
        return data


class WarrenHtmlActual(Source):
    """
    HTML file with data from Home Page -> Trade -> Meus ativos -> QUANTIDADE of Warren (https://warren.com.br/app/#/v3/trade).
    The columns are named as Ticker and Actual.

    ...
    """

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        self.selection_pattern = r'class="selected">\s*QUANTIDADE'
        self.table_pattern = r"QUANTIDADE(.+)Favoritos"
        self.ticker_pattern = r"(?:%| )(\w+) (\d+) "
        _check_extension(self.path, "html")
        _check_pattern_layout(self.path, _WARREN_PATTERN, self.selection_pattern)
        _check_last_update(self.path, date)

    def read(self) -> pd.DataFrame:
        data = _parse_html(self.path, self.table_pattern, self.ticker_pattern, "Actual")
        data["Actual"] = data["Actual"].astype(int)
        return data


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


class WarrenHtmlPrice(Source):
    """
    HTML file with data from Home Page -> Trade -> Meus ativos -> PREÇO ATUAL of Warren (https://warren.com.br/app/#/v3/trade).
    The columns are named as Ticker and Price.

    ...
    """

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        self.selection_pattern = r"class=\"selected\">\s*PREÇO ATUAL"
        self.table_pattern = r"PREÇO ATUAL(.+)Favoritos"
        self.ticker_pattern = r"([A-Z\d]+) R\$ ([\d\.,]+) "
        _check_extension(self.path, "html")
        _check_pattern_layout(self.path, _WARREN_PATTERN, self.selection_pattern)
        _check_last_update(self.path, date)

    def read(self) -> pd.DataFrame:
        data = _parse_html(self.path, self.table_pattern, self.ticker_pattern, "Price")
        data["Price"] = data["Price"].apply(parse_decimal, locale="pt_BR")
        return data


class StandardOutput(Source):
    """
    Excel sheet outputted by Transaction pipeline, which includes Ticker, Actual and Change columns.

    ...
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, ["Ticker", "Actual", "Change"])

    def read(self):
        return pd.read_excel(self.path)


class Change(Source):
    """
    Excel sheet with data downloaded from Área Logada do Investidor (https://www.investidor.b3.com.br/).
    The columns Data do Negociação, Código de Negociação, Quantidade and Preço are, respectivelly, renamed to Date, Ticker, Change and Price.

    ...
    """

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        _check_extension(self.path, "xlsx")
        _check_layout(self.path, _CHANGE_COLUMNS)

    def read(self) -> pd.DataFrame:
        data = (
            pd.read_excel(
                self.path,
                parse_dates=["Data do Negócio"],
                date_parser=lambda txt: datetime.strptime(txt, "%d/%m/%Y"),
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


class LayoutError(Exception):
    pass


class LastUpdateError(Exception):
    pass


def _read_excel(path: Path) -> pd.DataFrame:
    data = pd.read_excel(path, sheet_name=None)
    data = data.values()
    data = filter(lambda df: set(_ALI_COLUMNS).issubset(set(df.columns)), data)
    data = pd.concat(data)
    data = data.dropna(subset=_ALI_COLUMNS)
    data = data.reset_index(drop=True)
    data = data.astype(_ALI_TYPES)
    return data


def _read_html(path: Path, columns: list) -> pd.DataFrame:
    data = pd.read_html(path, thousands=".", decimal=",")
    data = filter(lambda df: set(columns).issubset(set(df.columns)), data)
    data = pd.concat(data)
    data = data.dropna(subset=columns)
    data = data.reset_index(drop=True)
    return data


def _convert_actual(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["Actual"] = pd.to_numeric(data["Actual"], errors="coerce", downcast="float")
    data = data.dropna(subset=["Actual"])
    data["Actual"] = data["Actual"].astype(int)
    return data


def _convert_price(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["Price"] = data["Price"].apply(parse_decimal, locale="pt_BR")
    data = data.dropna(subset=["Price"])
    return data


def _check_extension(path, extension: str):
    if not path.suffix.endswith(extension):
        raise LayoutError(
            "Extension {} is expected in file {}.".format(extension, path)
        )


def _check_layout(path: Path, columns: list) -> None:
    if path.suffix.endswith("xlsx"):
        data = pd.read_excel(path)
    elif path.suffix.endswith("html"):
        data = _read_html(path, columns)
    else:
        assert "File extension not supported: {}.".format(path)
    if not set(columns).issubset(set(data.columns)):
        raise LayoutError("Columns {} are expected in file {}.".format(columns, path))


def _check_last_update(path: Path, expected_date: date) -> None:
    if expected_date is None:
        return
    last_update = date.fromtimestamp(path.stat().st_mtime)
    if last_update < expected_date:
        raise LastUpdateError(
            "{} is out of date. Last update is expected to be at {} or later.".format(
                path, expected_date
            )
        )


def _parse_html(path: Path, table_pattern, ticker_pattern, value_column):
    text = _clean_html(_read_content(path))
    match = re.search(table_pattern, text)
    assert (
        match is not None
    ), "It is expected one table with values embraced by the pattern {} in the cleaned html {}.".format(
        table_pattern, text
    )
    table = match.group(0)
    data = []
    for row in re.findall(ticker_pattern, table):
        data.append(row)
    data = pd.DataFrame(data, columns=["Ticker", value_column])
    return data


def _clean_html(html):
    text = re.sub(r"<.*?>", "", html, flags=re.DOTALL)
    text = re.sub(r"\s\s+", " ", text)
    return text


def _check_pattern_layout(path: Path, *patterns):
    content = _read_content(path)
    for pattern in patterns:
        match = re.search(pattern, content, flags=re.DOTALL)
        if match is None:
            raise LayoutError(
                "Pattern {} is expected in file {}.".format(pattern, path)
            )


def _read_content(path: Path):
    with open(path, "r") as file:
        return file.read()
