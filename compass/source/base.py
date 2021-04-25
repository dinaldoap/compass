from abc import ABCMeta, abstractmethod
import pandas as pd


class Source(metaclass=ABCMeta):
    """
    One source of data.

    ...
    """

    @abstractmethod
    def read(self):
        """Read data from the source.

        """
        pass
