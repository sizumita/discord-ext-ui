from typing import List, Any, TYPE_CHECKING, Callable, Optional, Union

from discord import ui, PartialEmoji, ButtonStyle
import discord
from discord.utils import MISSING

from .utils import _call_any

if TYPE_CHECKING:
    from .view_manager import ViewManager


class CustomView(ui.View):
    def __init__(self, manager: 'ViewManager') -> None:
        super(CustomView, self).__init__(timeout=None)
        self.replaced: bool = False
        self.manager: 'ViewManager' = manager

    def refresh(self, components: List[discord.Component]) -> None:
        pass

    def dispatch(self, state: Any, item: ui.Item, interaction: discord.Interaction):
        if self.replaced:
            if self._stopped.done():
                return

            self._stopped.set_result(True)
            return
        super(CustomView, self).dispatch(state, item, interaction)


class CustomButton(ui.Button):
    def __init__(
            self,
            *,
            style: ButtonStyle,
            label: str,
            disabled: bool = False,
            custom_id: Optional[str] = None,
            url: Optional[str] = None,
            emoji: Optional[Union[str, PartialEmoji]] = None,
            row: Optional[int] = None,
            callback: Optional[Callable] = None,
            check_func: Callable[[discord.Interaction], bool]
    ) -> None:
        super(CustomButton, self).__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row
        )
        self.callback_func: Optional[Callable] = callback
        self.check_func: Callable[[discord.Interaction], bool] = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func(interaction):
            await _call_any(self.callback_func, interaction)


class CustomSelect(ui.Select):
    def __init__(
            self,
            *,
            custom_id: Optional[str],
            placeholder: Optional[str] = None,
            min_values: int = 1,
            max_values: int = 1,
            options: Optional[List[discord.SelectOption]],
            row: Optional[int] = None,
            callback: Optional[Callable] = None,
            check_func: Callable[[discord.Interaction], bool]
    ) -> None:
        custom_id = custom_id or MISSING
        options = options or MISSING
        super(CustomSelect, self).__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
            row=row
        )
        self.callback_func = callback
        self.check_func = check_func

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.callback_func is None:
            return
        if self.check_func(interaction):
            selected_options = []
            for label in interaction.data.get("values", []):
                for option in self.options:
                    if option.label == label:
                        selected_options.append(option)
                        continue
            await _call_any(self.callback_func, interaction, selected_options)
