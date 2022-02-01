from .base import Step

import pandas as pd


class Print(Step):
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
        return input


class ChangeHistoryView(Step):
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
            "AvgExpense",
            "AvgValue",
            "TotalExpense",
            "TotalValue",
            "CapitalGain",
            "Tax",
        ]
        input_columns = set(input.columns)
        columns = [column for column in columns if column in input_columns]
        return input.assign(Date=lambda df: df["Date"].dt.date).pipe(
            lambda df: df[columns]
        )


class SummaryView(Step):
    def run(self, input: pd.DataFrame):
        # Columns order
        columns = [
            "Name",
            "Ticker",
            "Actual",
            "TotalExpense",
            "TotalValue",
        ]
        input_columns = set(input.columns)
        columns = [column for column in columns if column in input_columns]
        columns = ["Year"] + columns
        return (
            input.assign(Year=lambda df: df["Date"].apply(lambda dt: dt.year))
            .groupby(["Year", "Ticker"], as_index=False)
            .last()
            .filter(items=columns)
        )
