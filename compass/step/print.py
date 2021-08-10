from .base import Step

import pandas as pd


class Print(Step):

    def run(self, input: pd.DataFrame):
        print(input)
        return input
