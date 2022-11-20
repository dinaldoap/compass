"""Actual step."""
import pandas as pd

from compass.source import Source

from .base import Step


class Actual(Step):
    """Step which reads actual data."""

    def __init__(self, source: Source):
        self.source = source

    def run(self, input_: pd.DataFrame) -> pd.DataFrame:
        output = self.source.read()
        output = output[["Ticker", "Actual"]]
        output = input_.join(output.set_index("Ticker"), on="Ticker", how="left")
        output["Actual"] = output["Actual"].fillna(0).astype(int)
        if len(input_) != len(output):
            raise RuntimeError(
                f"output's length ({len(output)}) is expected to be the same as input's ({len(input_)})."
            )
        return output
