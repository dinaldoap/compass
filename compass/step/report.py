from .base import Step
from compass.model import Calculator
from compass.number import format_currency
import pandas as pd


class Report(Step):
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def run(self, input: pd.DataFrame):
        df_calc = input.copy()
        df_calc["Transaction"] = df_calc["Change"] * df_calc["Price"]
        self.calculator.actual_deposit = df_calc[df_calc["Change"] > 0][
            "Transaction"
        ].sum()
        self.calculator.actual_withdraw = df_calc[df_calc["Change"] < 0][
            "Transaction"
        ].sum()
        print("=========== Input ===============")
        print("        Value:", format_currency(self.calculator.value))
        print("Expense Ratio: {}%".format(self.calculator.expense_ratio * 100))
        print(" Spread Ratio: {}%".format(self.calculator.spread_ratio * 100))
        print("========== Estimate =============")
        print("        Value:", format_currency(self.calculator.estimated_value))
        print("      Expense:", format_currency(self.calculator.estimated_expense))
        print("       Spread:", format_currency(self.calculator.estimated_spread))
        print("=========== Final ===============")
        print("      Deposit:", format_currency(self.calculator.actual_deposit))
        print("     Withdraw:", format_currency(self.calculator.actual_withdraw))
        print("      Expense:", format_currency(self.calculator.actual_expense))
        print("       Spread:", format_currency(self.calculator.actual_spread))
        print("    Remainder:", format_currency(self.calculator.actual_remainder))
        return input
