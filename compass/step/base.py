from compass.source import Source

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
        self.target.write(input)
        return input


class Join(Step):
    def __init__(
        self, source: Source, on, add: list = None, how="left", fillna={}, strict=False
    ):
        self.source = source
        self.on = on
        self.add = add
        self.how = how
        self.fillna = fillna
        self.type = {key: type(value) for key, value in fillna.items()}
        self.strict = strict

    def run(self, input: pd.DataFrame) -> pd.DataFrame:
        source = self.source.read().pipe(
            lambda df: df if self.add is None else df[[self.on] + self.add]
        )
        output = (
            input.join(source.set_index(self.on), on=self.on, how=self.how)
            .pipe(lambda df: df.fillna(self.fillna))
            .pipe(lambda df: df.astype(self.type))
        )
        if self.strict and len(input) != len(output):
            raise LengthChangedError(
                f"Output's length ({len(output)}) is expected to be the same as input's ({len(input)})."
            )
        return output


class LengthChangedError(Exception):
    pass
