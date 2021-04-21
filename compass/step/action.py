from .base import Step

import pandas as pd


class Action(Step):
    def run(self, input: pd.DataFrame):
        input.to_excel('data/action.xlsx', index=False)
        return input
