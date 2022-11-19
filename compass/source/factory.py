"""Factory for source step."""
from .base import Source
from .file import DirectoryChange, StandardActual, StandardPrice, StandardTarget


def create_target(config: dict) -> Source:
    """Create source step for target data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: source step.
    """
    return StandardTarget(path=config["target"])


def create_actual(config: dict) -> Source:
    """Create source step for actual data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: source step.
    """
    return StandardActual(config["actual"])


def create_price(config: dict) -> Source:
    """Create source step for price data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: source step.
    """
    return StandardPrice(config["price"])


def create_change(config: dict):
    """Create source step for change data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: source step.
    """
    return DirectoryChange(config["change"])
