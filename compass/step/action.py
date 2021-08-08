from .base import Step
from compass.target import Target
from compass.model import Calculator
from compass.number import format_currency
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
        print('        Value:',  format_currency(self.calculator.value))
        print('Expense Ratio: {}%'.format(self.calculator.expense_ratio * 100))
        print(' Spread Ratio: {}%'.format(self.calculator.spread_ratio * 100))
        print('========== Estimate =============')
        print('        Value:',  format_currency(
            self.calculator.estimated_value))
        print('      Expense:',  format_currency(
            self.calculator.estimated_expense))
        print('       Spread:',  format_currency(
            self.calculator.estimated_spread))
        print('=========== Final ===============')
        print('      Deposit:',  format_currency(
            self.calculator.actual_deposit))
        print('     Withdraw:',  format_currency(
            self.calculator.actual_withdraw))
        print('      Expense:',  format_currency(
            self.calculator.actual_expense))
        print('       Spread:',  format_currency(
            self.calculator.actual_spread))
        print('    Remainder:',  format_currency(
            self.calculator.actual_remainder))
        self.target.write(output)
        return output


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)
