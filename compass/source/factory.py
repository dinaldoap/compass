"""Factory for sources."""
from .base import Source
from .file import StandardActual, StandardPrice, StandardTarget


def create_target(config: dict) -> Source:
    """Create source for target data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: Source.
    """
    return StandardTarget(path=config["target"])


def create_actual(config: dict) -> Source:
    """Create source for actual data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: Source.
    """
    return StandardActual(config["actual"])


def create_price(config: dict) -> Source:
    """Create source for price data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: Source.
    """
    return StandardPrice(config["price"])
