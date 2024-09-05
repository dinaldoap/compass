"""Factory for targets."""

from .base import Target
from .file import Standard


def create_output(
    config: dict, sheet_name: str = "sheet", append: bool = False
) -> Target:
    """Create output target.

    Args:
        config (dict): Configuration.
        sheet_name (str, optional): Sheet name. Defaults to "sheet".
        append (bool, optional): Whether must append to existing output target. Defaults to False.

    Returns:
        Target: Output target.
    """
    return Standard(path=config["output"], sheet_name=sheet_name, append=append)
