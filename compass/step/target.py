"""Target step."""
import pandas as pd

from compass.source import Source

from .base import Step


class Target(Step):
    def __init__(self, source: Source):
        self.source = source

    def run(self, input: pd.DataFrame):
        output = self.source.read()
        return output[["Name", "Ticker", "Target", "Group"]]
