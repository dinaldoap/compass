from .base import Calculator


def create_calculator(config: dict) -> Calculator:
    return Calculator(value=config['value'], fee=config['fee'])
