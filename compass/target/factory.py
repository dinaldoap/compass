from .base import Target
from .file import Standard


def create_output(
    config: dict, sheet_name: str = "sheet", append: bool = False
) -> Target:
    return Standard(path=config["output"], sheet_name=sheet_name, append=append)


def create_actual(config: dict) -> Target:
    return Standard(path=config["actual"])
