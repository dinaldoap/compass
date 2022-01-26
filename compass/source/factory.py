from .base import Source
from .file import *
from .http import YahooPrice

from pathlib import Path


def create_target(config: dict) -> Source:
    return StandardTarget(path=config["target"])


def create_actual(config: dict) -> Source:
    classes = [
        StandardActual,
        AliActual,
        RicoHtmlActualPrice,
        CeiHtmlActual,
        WarrenHtmlActual,
    ]
    return _create_source(config["actual"], classes)


def create_price(config: dict) -> Source:
    # TODO: add YahooPrice
    return _create_source(
        config["price"], [StandardPrice, RicoHtmlActualPrice, WarrenHtmlPrice]
    )


def create_output(config: dict) -> Source:
    return StandardOutput(config["output"])


def _create_source(path, classes: list):
    for class_ in classes:
        try:
            return class_(path=path)
        except LayoutError:
            continue
    raise LayoutError("Layout not supported: {}.".format(path))


def create_change(config: dict):
    return Change(config["change"])
