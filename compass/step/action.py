from .base import Step
from .target import Target
from babel.numbers import format_decimal

import pandas as pd


class Action(Step):

    def __init__(self, target: Target):
        self.target = target

    def run(self, input: pd.DataFrame):
        output = input.copy()
        output['Before'] = output['Actual'] * output['Price']
        output['Before'] = _to_percentage(output['Before'])
        output['After'] = (output['Actual'] +
                           output['Change']) * output['Price']
        output['After'] = _to_percentage(output['After'])
        print(output)
        value = (output['Change'] * output['Price']).sum().round(2)
        print('Value: ',  format_decimal(value))
        self.target.write(output)
        return output


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)
