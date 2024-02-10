"""Factory for sources."""

from .base import Source
from .file import StandardPortfolio


def create_portfolio(config: dict) -> Source:
    """Create source for portfolio data.

    Args:
        config (dict): Configuration.

    Returns:
        Source: Source.
    """
    return StandardPortfolio(path=config["portfolio"])
