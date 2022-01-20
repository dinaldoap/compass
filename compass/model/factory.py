from .base import Calculator


def create_calculator(config: dict) -> Calculator:
    return Calculator(
        value=config["value"],
        expense_ratio=config["expense_ratio"],
    )
