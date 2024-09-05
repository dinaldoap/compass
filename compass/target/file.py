"""File targets."""

from pathlib import Path

import pandas as pd

from .base import Target


class Standard(Target):
    """
    Excel sheet with all the received columns.

    ...
    """

    def __init__(self, path: Path, sheet_name="sheet", append=False):
        self.path = Path(path)
        self.sheet_name = sheet_name
        self.append = append

    def write(self, data: pd.DataFrame):
        if self.append and self.path.exists():
            current = pd.read_excel(self.path, sheet_name=None)
        else:
            current = {}
        with pd.ExcelWriter(self.path) as writer:
            for sheet_name, df in current.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            data.to_excel(writer, sheet_name=self.sheet_name, index=False)
