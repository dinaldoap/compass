from .base import Step

import pandas as pd


class Change(Step):
    def run(self, input: pd.DataFrame):
        output = input.copy()
        output['Change'] = 0
        return output
