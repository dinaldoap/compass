from .base import Source
from .file import CeiActual, StandardActual, StandardPrice, StandardTarget, LayoutError
from .http import YahooPrice

from pathlib import Path


def create_target(config: dict) -> Source:
    path = Path(config['directory'], 'target.xlsx')
    return StandardTarget(path=path)


def create_actual(config: dict) -> Source:
    path = Path(config['directory'], 'actual.xlsx')
    try:
        return StandardActual(path=path)
    except LayoutError:
        return CeiActual(path=path)


def create_price(config: dict) -> Source:
    directory = config['directory']
    path = Path(directory, 'price.xlsx')
    try:
        return StandardPrice(path=path)
    except (FileNotFoundError, LayoutError):
        return YahooPrice(directory=directory)
