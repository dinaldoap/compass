from .base import Pipeline
from compass import source, target, model
from compass.step import Actual, Change, Price, Target, Balance, Print, Report, WriteTarget


class Transaction(Pipeline):
    def __init__(self, config):
        self.config = config

    def run(self):
        calculator = model.create_calculator(config=self.config)
        steps = [
            Target(source=source.create_target(config=self.config)),
            Actual(source=source.create_actual(config=self.config)),
            Price(source=source.create_price(config=self.config)),
            Change(value=calculator.estimated_value,
                   rebalance=self.config['rebalance'],
                   absolute_distance=self.config['absolute_distance'],
                   relative_distance=self.config['relative_distance'],
                   ),
            Balance(),
            Print(),
            Report(calculator=calculator),
            WriteTarget(target=target.create_output(
                config=self.config))
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
