from abc import ABCMeta, abstractmethod


class Source(metaclass=ABCMeta):
    """
    One source of data.

    ...
    """

    @abstractmethod
    def read(self):
        '''Read data from the source.

        Parameters
        ----------

        Returns
        -------
        pandas.DataFrame    
            DataFrame with the columns specified by each implementation.

        '''
        pass
