from .base import Transact
from compass.step import Action, Actual, Change, Price, Target


class Deposit(Transact):
    def run(self):
        # TODO: parameterize value passed to Change()
        steps = [Target(), Actual(), Price(), Change(100.), Action()]
        data = None
        for step in steps:
            data = step.run(input=data)
        print(data)
