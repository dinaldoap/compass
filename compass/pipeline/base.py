"""Base classes for pipelines."""

from abc import ABCMeta, abstractmethod


class Pipeline(metaclass=ABCMeta):
    """
    A pipeline.

    ...
    """

    @abstractmethod
    def run(self):
        """Run the pipeline."""
