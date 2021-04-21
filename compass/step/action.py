from .base import Step

import pandas as pd


class Action(Step):
    def run(self, input: pd.DataFrame):
        raise NotImplementedError()
