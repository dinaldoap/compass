import math


class Calculator():
    def __init__(self, value: float, expense_ratio: float, spread_ratio: float):
        self.value = value
        self._sign = math.copysign(1, value)
        self.expense_ratio = expense_ratio
        self.spread_ratio = spread_ratio
        self.actual_deposit = None
        self.actual_withdraw = None

    @property
    def estimated_transaction(self) -> float:
        return abs(self.value / (1 + self._sign * (self.expense_ratio + self.spread_ratio)))

    @property
    def estimated_expense(self) -> float:
        return - self.estimated_transaction * self.expense_ratio

    @property
    def estimated_spread(self) -> float:
        return - self.estimated_transaction * self.spread_ratio

    @property
    def estimated_value(self) -> float:
        return self._sign * self.estimated_transaction

    @property
    def actual_transaction(self) -> float:
        assert self.actual_deposit is not None and self.actual_withdraw is not None, 'Buy and sell are expected to calculate actual transaction.'
        return self.actual_deposit + abs(self.actual_withdraw)

    @property
    def actual_expense(self) -> float:
        return - self.actual_transaction * self.expense_ratio

    @property
    def actual_spread(self) -> float:
        return - self.actual_transaction * self.spread_ratio

    @property
    def actual_remainder(self) -> float:
        return - self.value + self.actual_deposit + self.actual_withdraw - self.actual_expense
