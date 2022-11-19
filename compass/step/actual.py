"""Actual step."""
import pandas as pd

from compass.source import Source

from .base import Step


class Actual(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame) -> pd.DataFrame:
        output = self.source.read()
        output = output[["Ticker", "Actual"]]
        output = input.join(output.set_index("Ticker"), on="Ticker", how="left")
        output["Actual"] = output["Actual"].fillna(0).astype(int)
        if len(input) != len(output):
            raise RuntimeError(
                "output's length ({}) is expected to be the same as input's ({}).".format(
                    len(output), len(input)
                )
            )
        return output
