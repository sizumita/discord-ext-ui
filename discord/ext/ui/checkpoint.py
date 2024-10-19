from typing import TypeVar, TYPE_CHECKING, Generic

from .signal import Signal
from .provider import ContextProvider


if TYPE_CHECKING:
    from .abc import Displayable
    from .context import Context


P = TypeVar("P", bound=ContextProvider, covariant=True)
S = TypeVar("S", bound=Signal)


class Checkpoint(Generic[S, P]):
    def __init__(self, ctx: "Context[P]", displayable: "Displayable[S, P]"):
        self.ctx = ctx
        self.view = displayable

    async def display(self) -> S:
        return await self.view.appear(self.ctx)
