"""Init pipeline."""

from compass import target
from compass.step import Init, WriteTarget

from .base import Pipeline


class InitPipeline(Pipeline):
    """Pipeline wich initilizes the portfolio spreadsheet."""

    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            Init(),
            WriteTarget(target=target.create_output(config=self.config)),
        ]
        data = None
        for step in steps:
            data = step.run(input_=data)
