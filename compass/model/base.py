class Calculator():
    def __init__(self, gross: float, fee: float):
        self.gross = gross
        self._fee = fee
        self._transaction = None

    @property
    def net(self) -> float:
        return self.gross / (1 + self._fee)

    @property
    def fee(self) -> float:
        return self.net * self._fee

    @property
    def transaction(self) -> float:
        assert self._transaction is not None, 'Transaction value is expected to be defined before the first usage.'
        return self._transaction

    @transaction.setter
    def transaction(self, transaction: float):
        self._transaction = transaction

    @property
    def remainder(self):
        return self.net - self.transaction
