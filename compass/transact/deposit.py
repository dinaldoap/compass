from .base import Transact
from compass import source
from compass.step import Action, Actual, Change, Price, Target


class Deposit(Transact):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [Target(), Actual(source=source.create_actual(config=self.config)),
                 Price(), Change(value=self.config['value']), Action()]
        data = None
        for step in steps:
            data = step.run(input=data)
        print(data)
