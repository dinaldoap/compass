from .base import Source
from .file import AliActual, CeiHtmlActual, StandardActual, StandardPrice, StandardTarget, LayoutError, RicoHtmlActualPrice, WarrenHtmlActual, WarrenHtmlPrice
from .http import YahooPrice

from pathlib import Path


def create_target(config: dict) -> Source:
    return StandardTarget(path=config['target'])


def create_actual(config: dict) -> Source:
    return _create_source(config['actual'], [StandardActual, AliActual, RicoHtmlActualPrice, CeiHtmlActual, WarrenHtmlActual])


def create_price(config: dict) -> Source:
    # TODO: add YahooPrice
    return _create_source(config['price'], [StandardPrice, RicoHtmlActualPrice, WarrenHtmlPrice])


def _create_source(path, classes: list):
    for class_ in classes:
        try:
            return class_(path=path)
        except LayoutError:
            continue
    raise LayoutError('Layout not supported: {}.'.format(path))
