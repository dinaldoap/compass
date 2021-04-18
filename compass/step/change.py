from .base import Step

import pandas as pd


class Change(Step):
    def run(self, data: pd.DataFrame):
        raise NotImplementedError()
