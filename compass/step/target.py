from .base import Step
from compass.source import Source

import pandas as pd


class Target(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame):
        output = self.source.read()
        return output[['Name', 'Ticker', 'Target']]
