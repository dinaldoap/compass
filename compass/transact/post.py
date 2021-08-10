from compass.step.base import ReadSource
from .base import Transact
from compass import source, target
from compass.step import ReadSource, ActualAddedChange, WriteTarget


class Post(Transact):
    def __init__(self, config):
        self.config = config

    def run(self):
        steps = [
            ReadSource(source=source.create_output(config=self.config)),
            ActualAddedChange(),
            WriteTarget(target=target.create_actual(config=self.config)),
        ]
        data = None
        for step in steps:
            data = step.run(input=data)
