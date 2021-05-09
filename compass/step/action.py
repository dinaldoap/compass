from .base import Step
from .target import Target

import pandas as pd


class Action(Step):

    def __init__(self, target: Target):
        self.target = target

    def run(self, input: pd.DataFrame):
        output = input.copy()
        output['After'] = (output['Actual'] +
                           output['Change']) * output['Price']
        output['After'] = output['After'] / output['After'].sum()
        output['After'] = output['After'].round(2)
        self.target.write(output)
        return output
