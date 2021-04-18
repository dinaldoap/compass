from .base import Transact
from compass.step import Actual, Change, Plan, Price, Quantity


class Deposit(Transact):
    def run(self):
        steps = [Plan(), Actual(), Change(), Price(), Quantity()]
        data = None
        for step in steps:
            data = step.run(data=data)
