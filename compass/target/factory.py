from .base import Target
from .file import StandardAction

from pathlib import Path


def create_action(config: dict) -> Target:
    return StandardAction(path=config['output'])


def create_actual(config: dict) -> Target:
    return StandardAction(path=config['actual'][0])
