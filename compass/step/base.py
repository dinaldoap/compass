"""Base classes for steps."""

from abc import ABCMeta, abstractmethod

import pandas as pd

from compass.source import Source
from compass.target import Target


class Step(metaclass=ABCMeta):
    """
    One step of a pipeline.

    ...
    """

    @abstractmethod
    def run(self, input_: pd.DataFrame):
        """Run one step of a pipeline."""


class ReadSource(Step):
    """Step which reads a source."""

    def __init__(self, source: Source):
        self.source = source

    def run(self, input_: pd.DataFrame):
        return self.source.read()


class WriteTarget(Step):
    """Step which writes a target."""

    def __init__(self, target: Target):
        self.target = target

    def run(self, input_: pd.DataFrame):
        self.target.write(input_)
        return input_
