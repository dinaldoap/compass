"""Base clases for models."""

import pandas as pd


class Calculator:
    """Calculates gross and net deposit and withdraw values."""

    def __init__(self, value: float, expense_ratio: float):
        self.value = value
        self.expense_ratio = expense_ratio
        self.deposit: float = 0
        self.withdraw: float = 0

    def calculate(self, df_change: pd.DataFrame):
        """Calculates gross deposit and withdraw values.

        Args:
            df_change (pd.DataFrame): Output from a change step. See @Change class.
        """
        df_calc = df_change.copy()
        df_calc["Transaction"] = df_calc["Change"] * df_calc["Price"]
        self.deposit = df_calc[df_calc["Change"] > 0]["Transaction"].sum()
        self.withdraw = df_calc[df_calc["Change"] < 0]["Transaction"].sum()

    @property
    def transaction(self) -> float:
        """Calculates net transaction value.

        Raises:
            RuntimeError: when deposit or withdraw value is None.

        Returns:
            float: Net transaction value.
        """
        if self.deposit is None or self.withdraw is None:
            raise RuntimeError(
                "Call Calculator.calculate() before calling Calculator.transaction()."
            )
        return self.deposit + abs(self.withdraw)

    @property
    def expense(self) -> float:
        """Calculates expenses value.

        Returns:
            float: Expenses value.
        """
        return -self.transaction * self.expense_ratio
