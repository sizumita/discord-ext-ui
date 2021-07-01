from typing import Optional, List, TypeVar, Generic, Callable

import discord.ui

from .item import Item
from .select_option import SelectOption
from .custom import CustomSelect


def _default_check(_: discord.Interaction) -> bool:
    return True


C = TypeVar("C", bound=discord.ui.Select)


class Select(Item, Generic[C]):
    def __init__(
            self,
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            options: Optional[list] = None,
            cls: C = CustomSelect,
            custom_id: Optional[str] = None,
    ) -> None:
        self._placeholder: Optional[str] = placeholder
        self._min_values: int = min_values
        self._max_values: int = max_values
        self._options: list = [] if options is None else options
        self._row: Optional[int] = None
        self.cls: C = cls
        self._custom_id: Optional[str] = custom_id

        self.func: Optional[Callable] = None
        self.check_func: Callable[[discord.Interaction], bool] = _default_check

    def placeholder(self, placeholder: str) -> 'Select':
        self._placeholder = placeholder
        return self

    def min_values(self, min_values: int) -> 'Select':
        self._min_values = min_values
        return self

    def max_values(self, max_values: int) -> 'Select':
        self._max_values = max_values
        return self

    def options(self, options: List[SelectOption]) -> 'Select':
        self._options = options
        return self

    def row(self, row: int) -> 'Select':
        self._row = row
        return self

    def on_select(self, func: Callable) -> 'Select':
        self.func = func

        return self

    def check(self, func: Callable[[discord.Interaction], bool]) -> 'Select':
        self.check_func = func
        return self

    def to_discord(self) -> C:
        return self.cls(
            placeholder=self._placeholder,
            min_values=self._min_values,
            max_values=self._max_values,
            options=[o.to_discord_select_option() for o in self._options],
            row=self._row,
            custom_id=self._custom_id,
            check_func=self.check_func,
            callback=self.func
        )
