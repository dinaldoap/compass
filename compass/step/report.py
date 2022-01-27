from .base import Step
from compass.model import Calculator
from compass.number import format_currency
import pandas as pd
import numpy as np


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


class ChangeHistoryReport(Step):
    def __init__(self, expense_ratio: float, tax_rate: float):
        self.expense_ratio = expense_ratio
        self.tax_rate = tax_rate

    def run(self, input: pd.DataFrame):
        output = (
            input.groupby("Ticker")
            .apply(lambda df_group: df_group.assign(AvgPrice=_avg_price))
            .assign(Expense=lambda df: df["Price"] * self.expense_ratio)
            .assign(
                CapitalGain=lambda df: np.abs(np.minimum(df["Change"], 0))
                * (df["Price"] - df["AvgPrice"])
            )
            .assign(Tax=lambda df: df["CapitalGain"] * self.tax_rate)
            .sort_values("Date")
            .reset_index(drop=True)
        )
        return output


def _avg_price(input: pd.DataFrame):
    count = 0
    value = 0
    avg_prices = []
    for _, row in input.iterrows():
        count += row["Change"]
        value += row["Change"] * (row["Price"] if row["Change"] >= 0 else avg_price)
        avg_price = value / count
        avg_prices.append(avg_price)
    return avg_prices
