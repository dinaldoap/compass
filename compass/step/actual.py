from .base import Step
from compass.source import Source

import pandas as pd


class Actual(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame) -> pd.DataFrame:
        output = self.source.read()
        output = output[['Ticker', 'Actual']]
        output = input.join(output.set_index('Ticker'),
                            on='Ticker', how='left')
        output['Actual'] = output['Actual'].fillna(0).astype(int)
        assert len(input) == len(output), 'output\'s length ({}) is expected to be the same as input\'s ({}).'.format(
            len(output), len(input))
        return output


class ActualAddedChange(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame) -> pd.DataFrame:
        actual = input.copy()
        actual = actual.drop('Change', axis='columns', errors='ignore')
        change = self.source.read()
        change = change[['Ticker', 'Change']]
        output = change.join(actual.set_index('Ticker'), on='Ticker')
        output['Actual'] = output['Actual'].fillna(0).astype(int)
        output['Actual'] += output['Change']
        output = output[actual.columns]
        return output
