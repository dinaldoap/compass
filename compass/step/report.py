"""Report step."""

import pandas as pd

from compass.model import Calculator
from compass.number import format_currency

from .base import Step


class AllocationReport(Step):
    """Step which calculates actual values before and after the changes."""

    def run(self, input_: pd.DataFrame):
        output = input_.copy()
        output["Before"] = output["Actual"] * output["Price"]
        output["Before"] = _to_percentage(output["Before"])
        output["After"] = (output["Actual"] + output["Change"]) * output["Price"]
        output["After"] = _to_percentage(output["After"])
        return output


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.fillna(0).round(2)


class TransactionPrint(Step):
    """Step which prints transaction values: total value of the change,
    expenses, deposit and withdraw values."""

    def __init__(self, rebalance: bool, calculator: Calculator):
        self.rebalance = rebalance
        self.calculator = calculator

    def run(self, input_: pd.DataFrame):
        self.calculator.calculate(input_)
        print("=========== Input ===============")
        print("        Value:", format_currency(self.calculator.value))
        print(f"    Rebalance: {self.rebalance}")
        print(f"Expense Ratio: {self.calculator.expense_ratio * 100}%")
        print("======== Transaction ============")
        print("      Deposit:", format_currency(self.calculator.deposit))
        print("     Withdraw:", format_currency(self.calculator.withdraw))
        print("      Expense:", format_currency(self.calculator.expense))
        print("=================================")
        return input_
