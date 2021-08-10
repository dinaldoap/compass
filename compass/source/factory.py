from .base import Source
from .file import AliActual, CeiHtmlActual, StandardActual, StandardPrice, StandardTarget, LayoutError, RicoHtmlActualPrice, StandardOutput, WarrenHtmlActual, WarrenHtmlPrice
from .composite import CompositeActual
from .http import YahooPrice

from pathlib import Path


def create_target(config: dict) -> Source:
    return StandardTarget(path=config['target'])


def create_actual(config: dict) -> Source:
    paths = config['actual']
    classes = [StandardActual, AliActual,
               RicoHtmlActualPrice, CeiHtmlActual, WarrenHtmlActual]
    actuals = map(lambda path: _create_source(path, classes), paths)
    return CompositeActual(actuals=actuals)


def create_price(config: dict) -> Source:
    # TODO: add YahooPrice
    return _create_source(config['price'], [StandardPrice, RicoHtmlActualPrice, WarrenHtmlPrice])


def create_output(config: dict) -> Source:
    return StandardOutput(config['output'])


def _create_source(path, classes: list):
    for class_ in classes:
        try:
            return class_(path=path)
        except LayoutError:
            continue
    raise LayoutError('Layout not supported: {}.'.format(path))
