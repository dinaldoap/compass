from .base import Source

import pandas as pd
from pathlib import Path


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
        _check_layout(self.path, ['Cód. de Negociação', 'Qtde.'])

    def read(self) -> pd.DataFrame:
        data = pd.read_excel(self.path)
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


def _check_layout(path, columns):
    data = pd.read_excel(path)
    if not set(columns).issubset(set(data.columns)):
        raise LayoutError(
            'Columns {} are expected in file {}.'.format(columns, path))

# TODO move to factory.py


def create_target(config: dict) -> Source:
    path = Path(config['directory'], 'target.xlsx')
    return StandardTarget(path=path)


def create_actual(config: dict) -> Source:
    path = Path(config['directory'], 'actual.xlsx')
    try:
        return StandardActual(path=path)
    except LayoutError:
        return CeiActual(path=path)
