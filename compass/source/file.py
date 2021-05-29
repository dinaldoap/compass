from .base import Source

from datetime import date
import pandas as pd
from pathlib import Path
import re

_CEI_COLUMNS = ['Cód. de Negociação', 'Qtde.']


class StandardTarget(Source):
    '''
    Excel sheet with Name, Ticker and Target columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_layout(self.path, ['Name', 'Ticker', 'Target'])

    def read(self):
        return pd.read_excel(self.path)


class StandardActual(Source):
    '''
    Excel sheet with Ticker and Actual columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_layout(self.path, ['Ticker', 'Actual'])

    def read(self):
        return pd.read_excel(self.path)


class CeiActual(Source):
    '''
    Excel sheet with data copied from Carteira de ativos of Canal Eletrônico do Investidor (https://cei.b3.com.br/).
    The columns Cód. de Negociação and Qtde. are, respectivelly, renamed to Ticker and Actual. 

    ...
    '''

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_layout(self.path, _CEI_COLUMNS)

    def read(self) -> pd.DataFrame:
        data = pd.read_excel(self.path)
        data = data.rename({
            'Cód. de Negociação': 'Ticker',
            'Qtde.': 'Actual',

        }, axis='columns')
        return data


class CeiHtmlActual(Source):
    '''
    HTML file with data from Home Page -> Investimentos -> Carteira de ativos -> Consultar of Canal Eletrônico do Investidor (https://cei.b3.com.br/CEI_Responsivo/ConsultarCarteiraAtivos.aspx).
    The columns Cód. de Negociação and Qtde. are, respectivelly, renamed to Ticker and Actual. 

    ...
    '''

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        _check_pattern_layout(
            self.path, 'https://cei.b3.com.br/CEI_Responsivo/ConsultarCarteiraAtivos.aspx')
        _check_layout(self.path, _CEI_COLUMNS)
        _check_last_update(self.path, date)

    def read(self) -> pd.DataFrame:
        data = _read_html(self.path)
        data = data.rename({
            'Cód. de Negociação': 'Ticker',
            'Qtde.': 'Actual',

        }, axis='columns')
        return data


class WarrenHtmlActual(Source):
    '''
    HTML file with data from Home Page -> Trade -> Meus ativos -> QUANTIDADE of Warren (https://warren.com.br/app/#/v3/trade).
    The columns Cód. de Negociação and Qtde. are, respectivelly, renamed to Ticker and Actual. 

    ...
    '''

    def __init__(self, path: Path, date=date.today()):
        self.path = Path(path)
        self.selection_pattern = r'class="selected">\s*QUANTIDADE'
        self.table_pattern = r'QUANTIDADE(.+)Favoritos'
        _check_pattern_layout(
            self.path, 'https://warren.com.br/app/#/v3/trade', self.selection_pattern)
        _check_last_update(self.path, date)

    def read(self) -> pd.DataFrame:
        data = _parse_html(self.path, self.table_pattern)
        return data


class StandardPrice(Source):
    '''
    Excel sheet with Ticker and Price columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = Path(path)
        _check_layout(self.path, ['Ticker', 'Price'])

    def read(self, tickers=None):
        return pd.read_excel(self.path)


class LayoutError(Exception):
    pass


class LastUpdateError(Exception):
    pass


def _read_html(path: Path) -> pd.DataFrame:
    data = pd.read_html(path, thousands='.', decimal=',')
    data = filter(lambda df: set(
        _CEI_COLUMNS).issubset(set(df.columns)), data)
    data = pd.concat(data)
    data = data.dropna()
    data = data.reset_index(drop=True)
    data['Qtde.'] = data['Qtde.'].astype(int)
    return data


def _check_layout(path: Path, columns: list) -> None:
    if path.suffix.endswith('xlsx'):
        data = pd.read_excel(path)
    elif path.suffix.endswith('html'):
        data = _read_html(path)
    else:
        assert 'File extension not supported: {}.'.format(path)
    if not set(columns).issubset(set(data.columns)):
        raise LayoutError(
            'Columns {} are expected in file {}.'.format(columns, path))


def _check_last_update(path: Path, expected_date: date) -> None:
    if expected_date is None:
        return
    last_update = date.fromtimestamp(path.stat().st_mtime)
    if last_update < expected_date:
        raise LastUpdateError(
            '{} is out of date. Last update is expected to be at {} or later.'.format(path, expected_date))


def _parse_html(path: Path, table_pattern):
    text = _clean_html(_read_content(path))
    match = re.search(table_pattern, text)
    assert len(match.groups()) == 1, 'It is expected only one table with quantities embraced by the pattern {} in the cleaned html {}.'.format(
        table_pattern, text)
    table = match.group(0)
    ticker_pattern = r'(\w+) (\d+)'
    data = []
    for row in re.findall(ticker_pattern, table):
        data.append(row)
    data = pd.DataFrame(data, columns=['Ticker', 'Actual'])
    data['Actual'] = data['Actual'].astype(int)
    return data


def _clean_html(html):
    text = re.sub(r'<.*?>', '', html, flags=re.DOTALL)
    text = re.sub(r'\s\s+', ' ', text)
    return text


def _check_pattern_layout(path: Path, *patterns):
    content = _read_content(path)
    for pattern in patterns:
        match = re.search(pattern, content, flags=re.DOTALL)
        if match is None:
            raise LayoutError(
                'Pattern {} is expected in file {}.'.format(pattern, path))


def _read_content(path: Path):
    with open(path, 'r') as file:
        return file.read()
