from .base import Transact
from compass.step import Action, Actual, Change, Price, Target


class Deposit(Transact):
    def run(self):
        steps = [Target(), Actual(), Price(), Change(), Action()]
        data = None
        for step in steps:
            data = step.run(input=data)
        print(data)
