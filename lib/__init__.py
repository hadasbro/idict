from abc import ABC
from typing import TypeVar


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
        pass


KT = TypeVar('KT', str, Stringifable)
KV = TypeVar('KV')
A = TypeVar('A', str, str)
