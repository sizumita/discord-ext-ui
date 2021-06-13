from typing import List, Any, TYPE_CHECKING

from discord import ui
import discord

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
