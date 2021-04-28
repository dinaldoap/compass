from .base import Source
from .file import StandardPrice
from .http import YahooPrice

from pathlib import Path


def create_price_source(config: dict) -> Source:
    directory = config['directory']
    path = Path(directory, 'price.xlsx')
    try:
        return StandardPrice(path=path)
    except RuntimeError as err:
        return YahooPrice(directory=directory)
