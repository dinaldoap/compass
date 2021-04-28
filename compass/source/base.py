from abc import ABCMeta, abstractmethod
import pandas as pd


class Source(metaclass=ABCMeta):
    """
    One source of data.

    ...
    """

    @abstractmethod
    def read(self, tickers=None):
        '''Read data from the source.

        Parameters
        ----------
        tickers : list or array-like
            Tickers to use as filter.

        Returns
        -------
        pandas.DataFrame    
            DataFrame with the columns specified by each implementation.

        '''
        pass
