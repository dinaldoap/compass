from .base import Step
from compass.source import CEI

import pandas as pd


class Actual(Step):
    def __init__(self):
        super().__init__()
        self.source = CEI('data/actual.xlsx')

    def run(self, input: pd.DataFrame):
        output = self.source.read()
        output = output[['Ticker', 'Actual']]
        output = input.join(output.set_index('Ticker'),
                            on='Ticker', how='left')
        output['Actual'] = output['Actual'].fillna(0).astype(int)
        assert len(input) == len(output), 'output\'s length ({}) is expected to be the same as input\'s ({}).'.format(
            len(output), len(input))
        return output
