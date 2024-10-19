import abc
from typing import TypeVar, Tuple
from abc import abstractmethod

import discord

from .context import Context
from .checkpoint import Checkpoint
from .provider import ContextProvider
from .abc import Runnable
from .signal import Signal


S = TypeVar("S", bound=Signal, covariant=True)
P = TypeVar("P", bound=ContextProvider, covariant=True)


class Flow(Runnable[S, P], abc.ABC):
    pass
