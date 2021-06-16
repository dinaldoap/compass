from .base import Step
from compass.target import Target
from compass.model import Calculator
from babel.numbers import format_currency

import pandas as pd


class Action(Step):

    def __init__(self, target: Target, calculator: Calculator):
        self.target = target
        self.calculator = calculator

    def run(self, input: pd.DataFrame):
        output = input.copy()
        output['Before'] = output['Actual'] * output['Price']
        output['Before'] = _to_percentage(output['Before'])
        output['After'] = (output['Actual'] +
                           output['Change']) * output['Price']
        output['After'] = _to_percentage(output['After'])
        print(output)
        self.calculator.transaction = (
            output['Change'] * output['Price']).abs().sum().round(2)
        print('========== Estimates =============')
        print('      Gross:',  to_currency(self.calculator.gross))
        print('        Fee:',  to_currency(self.calculator.estimated_fee))
        print('        Net:',  to_currency(self.calculator.net))
        print('============ Final ===============')
        print('Transaction:',  to_currency(self.calculator.transaction))
        print('        Fee:',  to_currency(self.calculator.actual_fee))
        print('  Remainder:',  to_currency(self.calculator.remainder))
        self.target.write(output)
        return output


def to_currency(value: float):
    return format_currency(value, currency='BRL')


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)
