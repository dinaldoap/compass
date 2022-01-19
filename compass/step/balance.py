from .base import Step

import pandas as pd


class Balance(Step):
    def run(self, input: pd.DataFrame):
        output = input.copy()
        output["Before"] = output["Actual"] * output["Price"]
        output["Before"] = _to_percentage(output["Before"])
        output["After"] = (output["Actual"] + output["Change"]) * output["Price"]
        output["After"] = _to_percentage(output["After"])
        return output


def _to_percentage(series: pd.Series):
    series = series / series.sum()
    return series.round(2)
