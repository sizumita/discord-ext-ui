import dataclasses
import itertools
import os
from typing import List
from enum import Enum, auto

import discord
import numpy as np
from discord.ext.ui import Button, View, ObservableObject, published, Message, ViewTracker, MessageProvider
from discord.ext.ui.utils import async_interaction_partial


class GameStatus:
    Opening = auto()
    Success = auto()
    Failed = auto()


@dataclasses.dataclass
class Mass:
    is_mine: bool
    mine_count: int
    opened: bool

    def get_label(self) -> str:
        if not self.opened:
            return "\u200b"
        if self.opened and self.is_mine:
            return "💥"
        return str(self.mine_count)

    def get_real_label(self):
        if self.is_mine:
            return "💣"
        return str(self.mine_count)

    def get_style(self) -> discord.ButtonStyle:
        if not self.opened:
            return discord.ButtonStyle.gray
        if self.opened and self.is_mine:
            return discord.ButtonStyle.danger
        return discord.ButtonStyle.green


class ViewModel(ObservableObject):
    board = published("board")
    status = published("status")

    def __init__(self, mines: int = 1):
        super().__init__()
        self.status = GameStatus.Opening

        self.shape = (5, 5)
        self.size = np.prod(self.shape)
        self.mines = mines
        self.board: List[List[Mass]] = [[] for _ in range(5)]
        self.setup_board()

    def is_opened_all(self) -> bool:
        for row in self.board:
            for mass in row:
                if not mass.opened and not mass.is_mine:
                    return False
        return True

    async def mass_opened(self, _: discord.Interaction, x: int, y: int):
        self.board[y][x].opened = True
        mass = self.board[y][x]
        if mass.is_mine:
            self.status = GameStatus.Failed
        if self.is_opened_all():
            self.status = GameStatus.Success
        else:
            self.view.update_sync()

    def setup_board(self):
        board = np.zeros(self.shape, dtype=np.int8)
        # 爆弾設置
        for x in np.random.choice(range(self.size), self.mines, replace=False):
            board[divmod(x, self.shape[1])] = -1

        # 爆弾個数表示

        t = np.zeros(self.shape, dtype=np.int8)

        r, c = self.shape
        for r_, c_ in itertools.product(range(-1, 2), range(-1, 2)):
            if r_ == c_ == 0:
                continue

            t[max(0, r_):min(r, r+r_), max(0, c_):min(c, c+c_)] -= board[max(0, -r_):min(r, r-r_), max(0, -c_):min(c, c-c_)]

        t[board == -1] = -1
        board = t

        for y, values in enumerate(board):
            for value in values:
                self.board[y].append(
                    Mass(value == -1, value, False)
                )


class MineSweeperView(View):
    def __init__(self):
        super().__init__()
        self.viewModel = ViewModel()

    async def body(self) -> Message:
        msg = "open panels"
        if self.viewModel.status == GameStatus.Failed:
            msg = "You lost"
        if self.viewModel.status == GameStatus.Success:
            msg = "You won"

        return Message(msg, components=self.board_to_button())

    def board_to_button(self):
        buttons = [[] for _ in range(5)]
        for y, masses in enumerate(self.viewModel.board):
            for x, mass in enumerate(masses):
                buttons[y].append(
                    Button(mass.get_label() if self.viewModel.status == GameStatus.Opening else mass.get_real_label())
                    .style(mass.get_style())
                    .on_click(
                        async_interaction_partial(self.viewModel.mass_opened, x, y) if not mass.opened else lambda _: None
                    )
                )
        return buttons


client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_message(message: discord.Message):
    if message.content == "!minesweeper":
        view_tracker = ViewTracker(MineSweeperView())
        await view_tracker.track(MessageProvider(message.channel))

client.run(os.environ["DISCORD_BOT_TOKEN"])
