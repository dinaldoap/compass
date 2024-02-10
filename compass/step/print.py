"""Print step."""

import pandas as pd

from compass.target import Target

from .base import Step


class ChangePrint(Step):
    """Print changes calculated in the change step.

    See @Change class.
    """

    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input_: pd.DataFrame):
        formatted = input_.copy()
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
        input_columns = set(input_.columns)
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
            formatted[percentage_columns] = formatted[percentage_columns].map(
                lambda x: f"{x}%"
            )
        print(formatted[columns])
        self.target.write(formatted[columns])
        return input_


class HistoricPrint(Step):
    """Print historic changes to the report."""

    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input_: pd.DataFrame):
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
        data = _reset_safe_filter(input_, columns)
        _print_last("Historic", data)
        self.target.write(data)
        return input_


class MonthPrint(Step):
    """Print month gain or loss to the report."""

    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input_: pd.DataFrame):
        # Columns order
        columns = [
            "Date",
            "TotalCapitalGain",
            "Tax",
        ]

        data = _resample_last(input_, "M")
        data = _reset_safe_filter(data, columns)
        _print_last("Month", data, by=["Date"])
        self.target.write(data)
        return input_


class YearPrint(Step):
    """Print accumulated actual by Year."""

    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input_: pd.DataFrame):
        # Columns order
        columns = [
            "Date",
            "Name",
            "Ticker",
            "Actual",
            "TotalPrice",
            "TotalExpense",
            "TotalValue",
        ]
        data = input_.groupby([input_.index.year, "Ticker"]).last()
        data = _reset_safe_filter(data, columns)
        _print_last("Year", data, by=["Date", "Ticker"])
        self.target.write(data)
        return input_


def _reset_safe_filter(input_: pd.DataFrame, columns: list):
    output = input_.reset_index()
    common_columns = [column for column in columns if column in set(output.columns)]
    return output.filter(items=common_columns)


def _resample_last(input_: pd.DataFrame, period: str):
    return input_.resample(period).last()


def _print_last(title: str, data: pd.DataFrame, by="Ticker"):
    print(f"================= {title} =================")
    last = data.groupby(by=by).last()
    print(last)
