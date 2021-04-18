from .base import Step

import pandas as pd


class Target(Step):
    def run(self, data: pd.DataFrame):
        return pd.read_excel('data/target.xlsx')
