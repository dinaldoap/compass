from .base import Step

import pandas as pd


class Actual(Step):
    def run(self, input: pd.DataFrame):
        output = pd.read_excel('data/actual.xlsx')
        output = output[['Ticker', 'Actual']]
        output = input.join(output.set_index('Ticker'),
                            on='Ticker', how='inner')
        assert len(input) == len(output), 'output\'s length ({}) is expected to be the same as input\'s ({}).'.format(
            len(output), len(input))
        return output
