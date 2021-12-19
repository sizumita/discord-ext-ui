from __future__ import annotations
import asyncio
import os
from typing import TypedDict

import discord
from discord.ext import commands
from discord.ext.ui.combine import AsyncPublisher, URLRequestPublisher
from discord.ext.ui import ObservableObject, published, View, Message, ViewTracker, MessageProvider


class Article(TypedDict):
    id: str
    title: str
    url: str


class ArticleProtocol:
    async def fetch(self) -> AsyncPublisher:
        raise NotImplementedError


class ArticleRequest(ArticleProtocol):
    scheme = "https"
    host = "qiita.com"
    base_path = "/api/v2"

    def fetch(self) -> AsyncPublisher:
        return URLRequestPublisher(self.api_components("/items"))\
            .json()

    def api_components(self, path: str) -> str:
        return f"{self.scheme}://{self.host}{self.base_path}{path}"


class ViewModel(ObservableObject):
    articles: list[Article] = published("articles")
    is_loading = published("is_loading")

    def __init__(self):
        super().__init__()
        self.articles = []
        self.is_loading = True
        self._article_request = ArticleRequest()

    async def fetch_articles(self):
        await self._article_request.fetch()\
            .sink(lambda x: setattr(self, "articles", x))
        self.is_loading = False


class SampleView(View):
    def __init__(self):
        super().__init__()
        self.view_model = ViewModel()

    async def body(self) -> Message:
        if self.view_model.is_loading:
            return Message("Now loading...")
        if not self.view_model.articles:
            return Message("No results")
        return Message(
            embeds=[
                discord.Embed(
                    title="Qiita articles",
                    description="\n\n".join(
                        [f'[{x["title"]}]({x["url"]})' for x in self.view_model.articles]
                    )
                )
            ]
        )

    async def on_appear(self) -> None:
        await self.view_model.fetch_articles()


bot = commands.Bot("!")


@bot.event
async def on_message(message: discord.Message):
    if message.content != "!qiita":
        return

    view = SampleView()
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


bot.run(os.environ["DISCORD_BOT_TOKEN"])
