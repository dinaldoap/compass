from .base import Step
from compass.model import Calculator
from compass.number import format_currency
import pandas as pd
import numpy as np


class AllocationReport(Step):
    def run(self, input: pd.DataFrame):
        output = input.copy()
        output["Before"] = output["Actual"] * output["Price"]
        output["Before"] = _to_percentage(output["Before"])
        output["After"] = (output["Actual"] + output["Change"]) * output["Price"]
        output["After"] = _to_percentage(output["After"])
        return output


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)


class TransactionPrint(Step):
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


class HistoricReport(Step):
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
                    Actual=lambda df: df["Change"].cumsum()
                )
                .assign(AvgPrice=lambda df: _cum_avg(df, "Price"))
                .assign(TotalPrice=lambda df: df["Actual"] * df["AvgPrice"])
                .assign(AvgExpense=lambda df: _cum_avg(df, "Expense"))
                .assign(TotalExpense=lambda df: df["Actual"] * df["AvgExpense"])
                .assign(AvgValue=lambda df: _cum_avg(df, "Value"))
                .assign(TotalValue=lambda df: df["Actual"] * df["AvgValue"])
            )
            .reset_index(level="Ticker", drop=True)
            .assign(
                CapitalGain=lambda df: np.abs(np.minimum(df["Change"], 0))
                * (df["Value"] - df["AvgValue"])
            )
            .sort_index()
            .assign(TotalCapitalGain=lambda df: _cum_sum_negative(df, "CapitalGain"))
            .assign(
                Tax=lambda df: (
                    (df["TotalCapitalGain"] > 0)
                    * df["TotalCapitalGain"]
                    * self.tax_rate
                ).round(2)
            )
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


def _cum_sum_negative(input: pd.DataFrame, column):
    """
    This method is useful for accumulating losses over time and reseting total after paying tax over capital gains.
    """
    total = 0
    totals = []
    input_id = input.assign(Id=range(len(input)))
    last = input_id.groupby([input.index.year, input.index.month]).last()
    last = set(last["Id"])
    for _, row in input_id.iterrows():
        value = row[column]
        total += value
        totals.append(total)
        # accumulate only negative total over month
        if row["Id"] in last:
            total = np.minimum(total, 0)
    return totals
