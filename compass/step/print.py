import pandas as pd

from compass.target import Target

from .base import Step


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
        data = _reset_safe_filter(input, columns)
        _print_last("Historic", data)
        self.target.write(data)
        return input


class MonthPrint(Step):
    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input: pd.DataFrame):
        # Columns order
        columns = [
            "Date",
            "TotalCapitalGain",
            "Tax",
        ]

        data = _resample_last(input, "M")
        data = _reset_safe_filter(data, columns)
        _print_last("Month", data, by=["Date"])
        self.target.write(data)
        return input


class YearPrint(Step):
    def __init__(self, target: Target):
        super().__init__()
        self.target = target

    def run(self, input: pd.DataFrame):
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
        data = input.groupby([input.index.year, "Ticker"]).last()
        data = _reset_safe_filter(data, columns)
        _print_last("Year", data, by=["Date", "Ticker"])
        self.target.write(data)
        return input


def _reset_safe_filter(input: pd.DataFrame, columns: list):
    output = input.reset_index()
    common_columns = [column for column in columns if column in set(output.columns)]
    return output.filter(items=common_columns)


def _resample_last(input: pd.DataFrame, period: str):
    return input.resample(period).last()


def _print_last(title: str, data: pd.DataFrame, by="Ticker"):
    print(f"================= {title} =================")
    last = data.groupby(by=by).last()
    print(last)
