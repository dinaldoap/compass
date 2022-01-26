from .base import Pipeline
from compass import source, target
from compass.step import (
    ReadSource,
    Join,
    WriteTarget,
)


class Report(Pipeline):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            ReadSource(source=source.create_change(config=self.config)),
            Join(
                source=source.create_target(config=self.config),
                on="Ticker",
                how="inner",
            ),
            WriteTarget(target=target.create_output(config=self.config)),
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
