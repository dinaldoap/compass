import math


class Calculator():
    def __init__(self, value: float, fee: float):
        self.value = value
        self._sign = math.copysign(1, value)
        self.fee = fee
        self.actual_buy = None
        self.actual_sell = None

    @property
    def estimated_transaction(self) -> float:
        return abs(self.value / (1 + self._sign * self.fee))

    @property
    def estimated_fee(self) -> float:
        return - self.estimated_transaction * self.fee

    @property
    def estimated_value(self) -> float:
        return self._sign * self.estimated_transaction

    @property
    def actual_transaction(self) -> float:
        assert self.actual_buy is not None and self.actual_sell is not None, 'Buy and sell are expected to calculate actual transaction.'
        return self.actual_buy + abs(self.actual_sell)

    @property
    def actual_fee(self) -> float:
        return - self.actual_transaction * self.fee

    @property
    def actual_remainder(self) -> float:
        if self.value > 0:
            return - self.value + self.actual_buy - self.actual_fee
        elif self.value < 0:
            return self.actual_sell - self.value - self.actual_fee
        else:
            return self.actual_sell + self.actual_buy - self.actual_fee
