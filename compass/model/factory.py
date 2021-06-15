from .base import Calculator


def create_calculator(config: dict) -> Calculator:
    return Calculator(gross=config['value'], fee=config['fee'])
