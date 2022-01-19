from compass.source import Source
from compass.target import Target

from abc import ABCMeta, abstractmethod
import pandas as pd


class Step(metaclass=ABCMeta):
    """
    One step of a transaction.

    ...
    """

    @abstractmethod
    def run(self, input: pd.DataFrame):
        """Run one step of a transaction."""
        pass


class ReadSource(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame):
        return self.source.read()


class WriteTarget(Step):
    def __init__(self, target: Source):
        self.target = target

    def run(self, input: pd.DataFrame):
        return self.target.write(input)
