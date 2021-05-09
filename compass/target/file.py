from .base import Target

import pandas as pd
from pathlib import Path


class StandardAction(Target):
    '''
    Excel sheet with all the received columns.

    ...
    '''

    def __init__(self, path: Path):
        self.path = Path(path)

    def write(self, data: pd.DataFrame):
        data.to_excel(self.path, index=False)
