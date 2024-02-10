"""Change pipeline."""

from compass import model, source, target
from compass.step import (
    AllocationReport,
    Change,
    ChangePrint,
    ReadSource,
    TransactionPrint,
    Validate,
)

from .base import Pipeline


class ChangePosition(Pipeline):
    """Pipeline wich reads portfolio data and calculates the change necessary
    to move the actual allocation towards the target one."""

    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            ReadSource(source=source.create_portfolio(config=self.config)),
            Validate(),
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
            data = step.run(input_=data)
