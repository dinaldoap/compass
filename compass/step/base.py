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


class Join(Step):
    def __init__(self, source: Source, on, how="left", fillna={}):
        self.source = source
        self.on = on
        self.how = how
        self.fillna = fillna
        self.type = {key: type(value) for key, value in fillna.items()}

    def run(self, input: pd.DataFrame) -> pd.DataFrame:
        source = self.source.read()
        output = (
            input.join(source.set_index("Ticker"), on="Ticker", how="left")
            .pipe(lambda df: df.fillna(self.fillna))
            .pipe(lambda df: df.astype(self.type))
        )
        assert len(input) == len(
            output
        ), "output's length ({}) is expected to be the same as input's ({}).".format(
            len(output), len(input)
        )
        return output
