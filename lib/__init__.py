from abc import ABC
from typing import TypeVar


class Stringifable(ABC):
    pass


KT = TypeVar('KT', str, Stringifable)
KV = TypeVar('KV')
A = TypeVar('A', str, str)
