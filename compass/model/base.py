"""Base clases for models."""
import pandas as pd


class Calculator:
    def __init__(self, value: float, expense_ratio: float):
        self.value = value
        self.expense_ratio = expense_ratio

    def calculate(self, df_change: pd.DataFrame):
        df_calc = df_change.copy()
        df_calc["Transaction"] = df_calc["Change"] * df_calc["Price"]
        self.deposit = df_calc[df_calc["Change"] > 0]["Transaction"].sum()
        self.withdraw = df_calc[df_calc["Change"] < 0]["Transaction"].sum()

    @property
    def transaction(self) -> float:
        if self.deposit is None or self.withdraw is None:
            raise RuntimeError(
                "Buy and sell are expected to calculate actual transaction."
            )
        return self.deposit + abs(self.withdraw)

    @property
    def expense(self) -> float:
        return -self.transaction * self.expense_ratio
