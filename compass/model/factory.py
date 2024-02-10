"""Factory for models."""

from .base import Calculator


def create_calculator(config: dict) -> Calculator:
    """Create calculator model.

    Args:
        config (dict): Configuration

    Returns:
        Calculator: Calculator.
    """
    return Calculator(
        value=config["value"],
        expense_ratio=config["expense_ratio"],
    )
