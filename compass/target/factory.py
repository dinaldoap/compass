from .base import Target
from .file import Standard

from pathlib import Path


def create_action(config: dict) -> Target:
    return Standard(path=config['output'])


def create_actual(config: dict) -> Target:
    return Standard(path=config['actual'][0])
