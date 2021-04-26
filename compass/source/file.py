from .base import Source

import pandas as pd


class Default(Source):
    '''
    Excel worksheet with \'Ticker\' and \'Actual\' columns.

    ...
    '''

    def __init__(self, path : str):
        self.path = path

    def read(self):
        return pd.read_excel(self.path)


class CEI(Source):
    '''
    Excel worksheet with data copied from \'Carteira de ativos\' of \'Canal Eletrônico do Investidor\' (https://cei.b3.com.br/).
    The columns 'Cód. de Negociação' and 'Qtde.' are, respectivelly, renamed to \'Ticker\' and \'Actual\'. 

    ...
    '''

    def __init__(self, path: str):
        self.path = path

    def read(self) -> pd.DataFrame:
        data = pd.read_excel(self.path)
        data = data.rename({
            'Empresa': 'Name',
            'Cód. de Negociação': 'Ticker',
            'Qtde.': 'Actual',

        }, axis='columns')
        return data


def create_source(config: dict) -> Source:
    source_type = config['source_type']
    source_path = config['source_path']
    if 'default' == source_type:
        return Default(path=source_path)
    if 'cei' == source_type:
        return CEI(path=source_path)
    assert False, 'Source type not expected: {}'.format(source_type)
