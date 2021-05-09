from .base import Source

import pandas as pd
from pathlib import Path

_CEI_COLUMNS = ['Cód. de Negociação', 'Qtde.']


class StandardTarget(Source):
    '''
    Excel sheet with Name, Ticker and Target columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = path
        _check_layout(self.path, ['Name', 'Ticker', 'Target'])

    def read(self):
        return pd.read_excel(self.path)


class StandardActual(Source):
    '''
    Excel sheet with Ticker and Actual columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = path
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
        self.path = path
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
    HTML file with data from Home Page -> Carteira de ativos -> Fundos of Canal Eletrônico do Investidor (https://cei.b3.com.br/CEI_Responsivo/ConsultarMovimentoCustodia.aspx?TP_VISUALIZACAO=5).
    The columns Cód. de Negociação and Qtde. are, respectivelly, renamed to Ticker and Actual. 

    ...
    '''

    def __init__(self, path: Path):
        self.path = path
        _check_layout(path, _CEI_COLUMNS)

    def read(self) -> pd.DataFrame:
        data = _read_html(self.path)
        data = data.rename({
            'Cód. de Negociação': 'Ticker',
            'Qtde.': 'Actual',

        }, axis='columns')
        return data


class StandardPrice(Source):
    '''
    Excel sheet with Ticker and Price columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = path
        _check_layout(self.path, ['Ticker', 'Price'])

    def read(self, tickers=None):
        return pd.read_excel(self.path)


class LayoutError(Exception):
    pass


def _read_html(path: Path) -> pd.DataFrame:
    data = pd.read_html(path, thousands='.', decimal=',')
    data = filter(lambda df: set(
        _CEI_COLUMNS).issubset(set(df.columns)), data)
    data = pd.concat(data)
    data = data.dropna()
    data = data.reset_index(drop=True)
    data['Qtde.'] = data['Qtde.'].astype(int)
    print(data)
    return data


def _check_layout(path: Path, columns: list) -> None:
    try:
        data = pd.read_excel(path)
    except:
        data = _read_html(path)
    if not set(columns).issubset(set(data.columns)):
        raise LayoutError(
            'Columns {} are expected in file {}.'.format(columns, path))
