from .base import Step
from compass.target import Target
from compass.model import Calculator
from babel.numbers import format_currency, format_percent, format_decimal

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
        df_calc = output.copy()
        df_calc['Transaction'] = output['Change'] * output['Price']
        self.calculator.actual_deposit = df_calc[df_calc['Change'] > 0]['Transaction'].sum(
        )
        self.calculator.actual_withdraw = df_calc[df_calc['Change'] < 0]['Transaction'].sum(
        )
        print('=========== Input ===============')
        print('        Value:',  to_currency(self.calculator.value))
        print('Expense Ratio: {}%'.format(self.calculator.expense_ratio * 100))
        print('========== Estimate =============')
        print('        Value:',  to_currency(self.calculator.estimated_value))
        print('      Expense:',  to_currency(
            self.calculator.estimated_expense))
        print('=========== Final ===============')
        print('      Deposit:',  to_currency(self.calculator.actual_deposit))
        print('     Withdraw:',  to_currency(self.calculator.actual_withdraw))
        print('      Expense:',  to_currency(self.calculator.actual_expense))
        print('    Remainder:',  to_currency(self.calculator.actual_remainder))
        self.target.write(output)
        return output


def to_currency(value: float):
    return format_currency(value, currency='BRL')


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)
