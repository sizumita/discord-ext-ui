from typing import Optional, List, Union

from discord import ui

from .button import Button


class Component:
    def __init__(self, buttons: Optional[List[Union[Button, List[Button]]]] = None) -> None:
        self.buttons = buttons

    def __eq__(self, other: 'Component'):
        return self.buttons == other.buttons

    def make_view(self) -> ui.View:
        view = ui.View(None)
        i = 0
        for button in self.buttons:
            if not isinstance(button, list):
                view.add_item(button.to_discord_button())
                continue
            for button_ in button:  # type: Button
                button_._group = i
                view.add_item(button_.to_discord_button())
            i += 1
        return view
