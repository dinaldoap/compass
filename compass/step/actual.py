from .base import Step

import pandas as pd


class Actual(Step):
    def run(self, data: pd.DataFrame):
        raise NotImplementedError()
