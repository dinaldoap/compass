"""Change pipeline."""
from compass import model, source, target
from compass.step import (
    Actual,
    AllocationReport,
    Change,
    ChangePrint,
    Price,
    Target,
    TransactionPrint,
)

from .base import Pipeline


class ChangePosition(Pipeline):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            Target(source=source.create_target(config=self.config)),
            Actual(source=source.create_actual(config=self.config)),
            Price(source=source.create_price(config=self.config)),
            Change(
                value=self.config["value"],
                rebalance=self.config["rebalance"],
                absolute_distance=self.config["absolute_distance"],
                relative_distance=self.config["relative_distance"],
            ),
            AllocationReport(),
            TransactionPrint(
                rebalance=self.config["rebalance"],
                calculator=model.create_calculator(config=self.config),
            ),
            ChangePrint(target=target.create_output(config=self.config)),
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
