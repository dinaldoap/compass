from .base import Transact
from compass.step import Actual, Change, Price, Quantity, Target


class Deposit(Transact):
    def run(self):
        steps = [Target(), Actual(), Price(), Change(), Quantity()]
        data = None
        for step in steps:
            data = step.run(data=data)
