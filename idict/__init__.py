from abc import ABC
from typing import TypeVar

from .idict import Idict


class Stringifable(ABC):
    """
    Stringifable
    """

    def __str__(self) -> str:
        """
        __str__

        Returns:
            str
        """
        raise NotImplementedError()


KT = TypeVar("KT", str, Stringifable)
KV = TypeVar("KV")
A = TypeVar("A", str, Stringifable)

__all__ = ["Idict", "KT", "KV", "A", "Stringifable"]
