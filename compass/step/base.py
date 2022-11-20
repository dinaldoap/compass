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


class Join(Step):
    """Step which joins a source data with the input data."""

    def __init__(
        self,
        source: Source,
        on: str,
        add: list = None,
        how="left",
        fillna=None,
        strict=False,
    ):  # pylint: disable=too-many-arguments
        self.source = source
        self.on = on
        self.add = add
        self.how = how
        if fillna is None:
            self.fillna = {}
        else:
            self.fillna = fillna
        self.type = {key: type(value) for key, value in self.fillna.items()}
        self.strict = strict

    def run(self, input_: pd.DataFrame) -> pd.DataFrame:
        source = self.source.read().pipe(
            lambda df: df if self.add is None else df[[self.on] + self.add]
        )
        output = (
            input_.join(source.set_index(self.on), on=self.on, how=self.how)
            .pipe(lambda df: df.fillna(self.fillna))
            .pipe(lambda df: df.astype(self.type))
        )
        if self.strict and len(input_) != len(output):
            raise LengthChangedError(
                f"Output's length ({len(output)}) is expected to be the same as input's ({len(input_)})."
            )
        return output


class LengthChangedError(Exception):
    """Exception raised when the input length is different from the output
    one."""
