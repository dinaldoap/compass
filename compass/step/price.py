from .base import Step

import pandas as pd


class Price(Step):
    def run(self, data: pd.DataFrame):
        raise NotImplementedError()
