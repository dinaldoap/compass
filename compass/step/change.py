from .base import Step

import pandas as pd


class Change(Step):
    def run(self, input: pd.DataFrame):
        raise NotImplementedError()
