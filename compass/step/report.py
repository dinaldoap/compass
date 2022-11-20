"""Report step."""
from datetime import datetime

import numpy as np
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
    return series.round(2)


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


class HistoricReport(Step):
    """Step which calculates historic changes to the report."""

    def __init__(
        self, expense_ratio: float, tax_rate: float, current_date: datetime.date = None
    ):
        self.expense_ratio = expense_ratio
        self.tax_rate = tax_rate
        self.current_date = datetime.now() if current_date is None else current_date

    def run(self, input_: pd.DataFrame):
        last_day_months = pd.DataFrame(
            {
                "Date": pd.date_range(
                    start=input_.index.min(), end=self.current_date, freq="M"
                )
            }
        )
        tickers = input_.filter(["Ticker"]).drop_duplicates()
        date_ticker = last_day_months.merge(tickers, how="cross")
        output = (
            input_.set_index("Ticker", append=True)
            .join(date_ticker.set_index(["Date", "Ticker"]), how="outer")
            .fillna(value={"Change": 0}, downcast="infer")
            .fillna(value={"Price": 0.0})
            .assign(Expense=lambda df: (df["Price"] * self.expense_ratio).round(2))
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
            .reset_index(level="Ticker")
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


def _cum_avg(input_: pd.DataFrame, column):
    count = 0
    value = 0.0
    avg = 0.0
    avgs = []
    for _, row in input_.iterrows():
        change = row["Change"]
        count += change
        value += change * (row[column] if change >= 0 else avg)
        avg = (
            (round(value / count, 2) if value > 0.0 and count > 0 else 0.0)
            if change >= 0
            else avg
        )
        avgs.append(avg)
    return avgs


def _cum_sum_negative(input_: pd.DataFrame, column):
    """This method is useful for accumulating losses over time and reseting
    total after paying tax over capital gains."""
    total = 0
    totals = []
    input_id = input_.assign(Id=range(len(input_)))
    last = input_id.groupby([input_.index.year, input_.index.month]).last()
    last = set(last["Id"])
    for _, row in input_id.iterrows():
        value = row[column]
        total += value
        totals.append(total)
        # accumulate only negative total over month
        if row["Id"] in last:
            total = np.minimum(total, 0)
    return totals
