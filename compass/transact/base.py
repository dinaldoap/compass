from abc import ABCMeta, abstractmethod


class Transact(metaclass=ABCMeta):
    """
    A transaction.

    ...
    """

    @abstractmethod
    def run(self):
        """Run the transaction.

        """
        pass
