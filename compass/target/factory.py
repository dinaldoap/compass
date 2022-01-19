from .base import Target
from .file import Standard


def create_output(config: dict) -> Target:
    return Standard(path=config["output"])


def create_actual(config: dict) -> Target:
    return Standard(path=config["actual"])
