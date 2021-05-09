from .base import Target
from .file import StandardAction

from pathlib import Path


def create_action(config: dict) -> Target:
    path = Path(config['directory'], 'action.xlsx')
    return StandardAction(path=path)
