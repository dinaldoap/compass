from .base import Step

import pandas as pd


class Quantity(Step):
    def run(self, data: pd.DataFrame):
        raise NotImplementedError()
