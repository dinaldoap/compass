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
        self.calculator.actual_buy = df_calc[df_calc['Change'] > 0]['Transaction'].sum(
        )
        self.calculator.actual_sell = df_calc[df_calc['Change'] < 0]['Transaction'].sum(
        )
        print('========== Input =============')
        print('    Value:',  to_currency(self.calculator.value))
        print('      Fee: {}%'.format(self.calculator.fee * 100))
        print('========== Estimate =============')
        print('    Value:',  to_currency(self.calculator.estimated_value))
        print('      Fee:',  to_currency(self.calculator.estimated_fee))
        print('============ Final ===============')
        print('      Buy:',  to_currency(self.calculator.actual_buy))
        print('     Sell:',  to_currency(self.calculator.actual_sell))
        print('      Fee:',  to_currency(self.calculator.actual_fee))
        print('Remainder:',  to_currency(self.calculator.actual_remainder))
        self.target.write(output)
        return output


def to_currency(value: float):
    return format_currency(value, currency='BRL')


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)
