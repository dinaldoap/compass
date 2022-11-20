"""Price step."""
import pandas as pd

from compass.source import Source

from .base import Step


class Price(Step):
    """Step which reads price data."""

    def __init__(self, source: Source):
        self.source = source

    def run(self, input_: pd.DataFrame):
        output = self.source.read()
        output = output[["Ticker", "Price"]]
        output = input_.join(output.set_index("Ticker"), on="Ticker", how="inner")
        if len(input_) != len(output):
            raise RuntimeError(
                f"output's length ({len(output)}) is expected to be the same as input's ({len(input_)})."
            )
        return output
