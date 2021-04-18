from .base import Step

import pandas as pd


class Plan(Step):
    def run(self, data: pd.DataFrame):
        raise NotImplementedError()
