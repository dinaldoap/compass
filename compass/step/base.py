from abc import ABCMeta, abstractmethod
import pandas as pd


class Step(metaclass=ABCMeta):
    """
    One step of a transaction.

    ...
    """

    @abstractmethod
    def run(self, data: pd.DataFrame):
        """Run one step of a transaction.

        """
        pass
