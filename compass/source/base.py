"""Base classes for sources."""

from abc import ABCMeta, abstractmethod

import pandas as pd


class Source(metaclass=ABCMeta):
    """
    One source of data.

    ...
    """

    @abstractmethod
    def read(self) -> pd.DataFrame:
        """Read data from the source.

        Parameters
        ----------

        Returns
        -------
        pandas.DataFrame
            DataFrame with the columns specified by each implementation.
        """
