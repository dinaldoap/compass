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
            input.assign(Expense=lambda df: (df["Price"] * self.expense_ratio).round(2))
            .assign(
                Value=lambda df: df["Price"]
                + ((df["Change"] >= 0).astype(int) - (df["Change"] < 0).astype(int))
                * df["Expense"]
            )
            .groupby("Ticker")
            .apply(
                lambda df_group: df_group.assign(
                    CumSumChange=lambda df: df["Change"].cumsum()
                )
                .assign(CumAvgExpense=lambda df: _cum_avg(df, "Expense"))
                .assign(
                    CumSumExpense=lambda df: df["CumSumChange"] * df["CumAvgExpense"]
                )
                .assign(CumAvgValue=lambda df: _cum_avg(df, "Value"))
                .assign(CumSumValue=lambda df: df["CumSumChange"] * df["CumAvgValue"])
            )
            .assign(
                CapitalGain=lambda df: np.abs(np.minimum(df["Change"], 0))
                * np.maximum(df["Value"] - df["CumAvgValue"], 0.0)
            )
            .assign(Tax=lambda df: (df["CapitalGain"] * self.tax_rate).round(2))
            .sort_values("Date")
            .reset_index(drop=True)
        )
        return output


def _cum_avg(input: pd.DataFrame, column):
    count = 0
    value = 0
    avgs = []
    for _, row in input.iterrows():
        change = row["Change"]
        count += change
        value += change * (row[column] if change >= 0 else avg)
        avg = round(value / count, 2) if change >= 0 else avg
        avgs.append(avg)
    return avgs
