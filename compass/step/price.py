from .base import Step

import pandas as pd


class Price(Step):
    def run(self, data: pd.DataFrame):
        output = pd.read_excel('data/price.xlsx')
        output = output[['Ticker', 'Price']]
        output = data.join(output.set_index('Ticker'),
                           on='Ticker', how='inner')
        assert len(data) == len(output), 'output\'s length ({}) is expected to be the same as input\'s ({}).'.format(
            len(output), len(data))
        return output
