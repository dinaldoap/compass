from .base import Transact
from compass import source, target
from compass.step import Action, Actual, Change, Price, Target


class Deposit(Transact):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            Target(source=source.create_target(config=self.config)),
            Actual(source=source.create_actual(config=self.config)),
            Price(source=source.create_price(config=self.config)),
            Change(value=self.config['value']),
            Action(target=target.create_action(config=self.config))
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
