from .base import Step

import pandas as pd


class Actual(Step):
    def run(self, data: pd.DataFrame):
        actual = pd.read_excel('data/actual.xlsx')
        actual = actual[['Ticker', 'Actual']]
        result = data.join(actual.set_index('Ticker'), how='inner')
        return result
