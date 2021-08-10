from .base import Pipeline
from compass import source, target, model
from compass.step import Action, Actual, Change, Price, Target


class Transaction(Pipeline):
    def __init__(self, config):
        self.config = config

    def run(self):
        calculator = model.create_calculator(config=self.config)
        steps = [
            Target(source=source.create_target(config=self.config)),
            Actual(source=source.create_actual(config=self.config)),
            Price(source=source.create_price(config=self.config)),
            Change(value=calculator.estimated_value),
            Action(target=target.create_action(
                config=self.config), calculator=calculator)
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
