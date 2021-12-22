from __future__ import annotations
from typing import Callable, Optional, Type

import discord

from .message import Message
from .view import View
from .button import Button
from .state import state


class PaginationButtons:
    def first(self, now: int, last_page: int) -> Button:
        return Button("<<").style(discord.ButtonStyle.blurple).disabled(now == 0)

    def previous(self, now: int, last_page: int) -> Button:
        return Button("<").style(discord.ButtonStyle.green).disabled(now == 0)

    def indicator(self, now: int, last_page: int):
        return Button(f"{now+1}/{last_page+1}").style(discord.ButtonStyle.gray).disabled(True)

    def next(self, now: int, last_page: int) -> Button:
        return Button(">").style(discord.ButtonStyle.green).disabled(now == last_page)

    def last(self, now: int, last_page: int) -> Button:
        return Button(">>").style(discord.ButtonStyle.blurple).disabled(now == last_page)


class PaginationView(View):
    page = state("page")

    def __init__(
            self,
            views: list[PageView] | PageView,
            *,
            show_buttons: bool = True,
            show_disabled: bool = False,
            show_indicator: bool = True,
            check: Optional[Callable[[discord.Interaction], bool]] = None,
            first_page: int = 0,
            cls: Type[PaginationButtons] = PaginationButtons
    ):
        super(PaginationView, self).__init__()
        self._views = views
        self.show_buttons = show_buttons
        self.show_disabled = show_disabled,
        self.show_indicator = show_indicator
        self.check = check

        self.page = first_page  # index 0始まり
        self.max_page = len(self._views) - 1
        self.button_gen = cls()

    def change_page(self, interaction: discord.Interaction, page: int):
        if self.check is not None and not self.check(interaction):
            return
        self.page = page

    async def body(self) -> Message | View:
        view = self._views[self.page] if isinstance(self._views, list) else self._views
        buttons = []
        first = self.button_gen.first(self.page, self.max_page)
        if not (not self.show_disabled and getattr(first, "_disabled", False)):
            buttons.append(first.on_click(lambda x: self.change_page(x, 0)))

        prev = self.button_gen.previous(self.page, self.max_page)
        if not (not self.show_disabled and getattr(prev, "_disabled", False)):
            buttons.append(prev.on_click(lambda x: self.change_page(x, self.page - 1)))

        if self.show_indicator:
            indicator = self.button_gen.indicator(self.page, self.max_page)
            buttons.append(indicator)

        next_ = self.button_gen.next(self.page, self.max_page)
        if not (not self.show_disabled and getattr(next_, "_disabled", False)):
            buttons.append(next_.on_click(lambda x: self.change_page(x, self.page + 1)))

        last = self.button_gen.last(self.page, self.max_page)
        if not (not self.show_disabled and getattr(last, "_disabled", False)):
            buttons.append(last.on_click(lambda x: self.change_page(x, self.max_page)))

        await view.on_appear(self)
        body = await view.body(self)
        body.items([buttons])

        return body


class PageView(View):
    async def body(self, paginator: PaginationView) -> Message | View:
        return await super(PageView, self).body()

    async def on_appear(self, paginator: PaginationView) -> None:
        """
        ページが表示される前に実行されます。
        一つのPageViewだけをPaginationViewに登録していた場合でも、ページが変更されるごとに毎回実行されます。
        :param paginator:
        :return:
        """
        pass
