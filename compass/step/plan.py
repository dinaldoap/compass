from .base import Step

import pandas as pd


class Plan(Step):
    def run(self, data: pd.DataFrame):
        return pd.read_excel('data/plan.xlsx')
