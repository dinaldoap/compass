from .base import Source

import pandas as pd
from pathlib import Path


class Standard(Source):
    '''
    Excel worksheet with \'Ticker\' and \'Actual\' columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = path
        _check_layout(self.path, ['Ticker', 'Actual'])

    def read(self):
        return pd.read_excel(self.path)


class CEI(Source):
    '''
    Excel worksheet with data copied from \'Carteira de ativos\' of \'Canal Eletrônico do Investidor\' (https://cei.b3.com.br/).
    The columns 'Cód. de Negociação' and 'Qtde.' are, respectivelly, renamed to \'Ticker\' and \'Actual\'. 

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


def _check_layout(path, columns):
    data = pd.read_excel(path)
    if not set(columns).issubset(set(data.columns)):
        raise RuntimeError(
            'Columns {} are expected in file {}.'.format(columns, path))


def create_source(config: dict) -> Source:
    actual_path = Path(config['directory'], 'actual.xlsx')
    try:
        return CEI(path=actual_path)
    except RuntimeError as err:
        return Standard(path=actual_path)
