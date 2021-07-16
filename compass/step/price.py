from .base import Step
from compass.source import Source

import pandas as pd


class Price(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame):
        output = self.source.read()
        output = output[['Ticker', 'Price']]
        output = input.join(output.set_index('Ticker'),
                            on='Ticker', how='inner')
        assert len(input) == len(output), 'output\'s length ({}) is expected to be the same as input\'s ({}).'.format(
            len(output), len(input))
        return output
