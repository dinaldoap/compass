"""Base classes for targets."""

from abc import ABCMeta, abstractmethod

import pandas as pd


class Target(metaclass=ABCMeta):
    """
    One target for data.

    ...
    """

    @abstractmethod
    def write(self, data: pd.DataFrame) -> None:
        """Write data into the target.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame with the data.

        Returns
        -------
        """
