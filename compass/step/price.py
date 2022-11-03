import pandas as pd

from compass.source import Source

from .base import Step


class Price(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame):
        output = self.source.read()
        output = output[["Ticker", "Price"]]
        output = input.join(output.set_index("Ticker"), on="Ticker", how="inner")
        if len(input) != len(output):
            raise RuntimeError(
                "output's length ({}) is expected to be the same as input's ({}).".format(
                    len(output), len(input)
                )
            )
        return output
