from .base import Step
from compass.target import Target

import pandas as pd


class ChangePrint(Step):
    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input: pd.DataFrame):
        formatted = input.copy()
        # Columns order
        columns = [
            "Name",
            "Ticker",
            "Change",
            "Price",
            "Actual",
            "Before",
            "After",
            "Target",
            "Group",
        ]
        input_columns = set(input.columns)
        columns = [column for column in columns if column in input_columns]
        # Replace NaN with empty string
        if "Group" in input_columns:
            formatted["Group"] = formatted["Group"].fillna("")
        # Format percentage
        percentage_columns = ["Before", "After", "Target"]
        if set(percentage_columns).issubset(input_columns):
            formatted[percentage_columns] = formatted[percentage_columns] * 100
            formatted[percentage_columns] = formatted[percentage_columns].round()
            formatted[percentage_columns] = formatted[percentage_columns].astype(int)
            formatted[percentage_columns] = formatted[percentage_columns].applymap(
                lambda x: "{}%".format(x)
            )
        print(formatted[columns])
        self.target.write(formatted[columns])
        return input


class HistoricPrint(Step):
    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input: pd.DataFrame):
        # Columns order
        columns = [
            "Date",
            "Name",
            "Ticker",
            "Change",
            "Actual",
            "Price",
            "Expense",
            "Value",
            "AvgPrice",
            "AvgExpense",
            "AvgValue",
            "TotalPrice",
            "TotalExpense",
            "TotalValue",
            "CapitalGain",
            "TotalCapitalGain",
            "Tax",
        ]
        input_columns = set(input.columns)
        columns = [column for column in columns if column in input_columns]
        data = input.assign(Date=lambda df: df["Date"].dt.date).filter(items=columns)
        _print_last("Historic", data)
        self.target.write(data)
        return input


class SummaryPrint(Step):
    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input: pd.DataFrame):
        # Columns order
        columns = [
            "Year",
            "Name",
            "Ticker",
            "Actual",
            "TotalPrice",
            "TotalExpense",
            "TotalValue",
        ]
        input_columns = set(input.columns)
        columns = [column for column in columns if column in input_columns]
        data = (
            input.groupby(["Year", "Ticker"], as_index=False)
            .last()
            .filter(items=columns)
        )
        _print_last("Year", data)
        self.target.write(data)
        return input


def _print_last(title: str, data: pd.DataFrame):
    print(f"================= {title} =================")
    last = data.groupby("Ticker").last()
    print(last)
