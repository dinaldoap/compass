from .base import Step

import pandas as pd


class Quantity(Step):
    def run(self, input: pd.DataFrame):
        raise NotImplementedError()
