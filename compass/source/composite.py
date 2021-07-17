from .base import Source

import pandas as pd


class CompositeActual(Source):
    def __init__(self, actuals: list):
        self.actuals = actuals

    def read(self):
        data = []
        for actual in self.actuals:
            data.append(actual.read())
        data = pd.concat(data)
        data = data.groupby(by='Ticker', as_index=False,
                            sort=False).agg({'Actual': 'sum'})
        return data
