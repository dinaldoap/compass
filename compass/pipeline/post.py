from .base import Pipeline
from compass import source, target
from compass.step import ReadSource, ActualAddedChange, WriteTarget, Print


class Post(Pipeline):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            ReadSource(source=source.create_output(config=self.config)),
            ActualAddedChange(),
            Print(),
            WriteTarget(target=target.create_actual(config=self.config)),
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
