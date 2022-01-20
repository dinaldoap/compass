from .base import Step
from compass.model import Calculator
from compass.number import format_currency
import pandas as pd


class Report(Step):
    def __init__(self, rebalance: bool, calculator: Calculator):
        self.rebalance = rebalance
        self.calculator = calculator

    def run(self, input: pd.DataFrame):
        self.calculator.calculate(input)
        print("=========== Input ===============")
        print("        Value:", format_currency(self.calculator.value))
        print("    Rebalance: {}".format(self.rebalance))
        print("Expense Ratio: {}%".format(self.calculator.expense_ratio * 100))
        print("======== Transaction ============")
        print("      Deposit:", format_currency(self.calculator.deposit))
        print("     Withdraw:", format_currency(self.calculator.withdraw))
        print("      Expense:", format_currency(self.calculator.expense))
        print("=================================")
        return input
