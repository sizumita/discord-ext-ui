from __future__ import annotations
from discord.ext.ui import View, ViewTracker, Message, PaginationView, MessageProvider, LinkButton, PaginationButtons, Button
import discord
import os


client = discord.Client()


class Page(View):
    def __init__(self, content: str, button: LinkButton):
        super(Page, self).__init__()
        self.content = content
        self.button = button

    async def body(self) -> Message | View:
        return Message(self.content).item([self.button])


class CustomButtons(PaginationButtons):
    def first(self, now: int, last_page: int) -> Button:
        return Button("朝に戻る").style(discord.ButtonStyle.blurple)

    def last(self, now: int, last_page: int) -> Button:
        return Button("おやすみなさい！").style(discord.ButtonStyle.blurple).disabled(now == last_page)


@client.event
async def on_message(message: discord.Message):
    if message.content != "!test":
        return

    view = PaginationView([
        Page("The first page -- Morning --",
             LinkButton("https://www.google.co.jp/search?q=朝早く起きる方法", "Search for 朝早く起きる方法")
             ),
        Page("The second page -- Noon --",
             LinkButton("https://www.google.co.jp/search?q=昼ごはん", "Search for 昼ごはん")),
        Page("The third page -- Afternoon --",
             LinkButton("https://www.google.co.jp/search?q=午後の紅茶", "Search for 午後の紅茶")),
        Page("The forth page -- Evening --",
             LinkButton("https://www.google.co.jp/search?q=イタリアンバル", "Search for イタリアンバル")),
        Page("The last page -- Good night! --",
             LinkButton("https://www.google.co.jp/search?q=寝つきを良くする方法", "Search for 寝つきを良くする方法")),
    ], show_indicator=False, cls=CustomButtons)
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(message.channel))


client.run(os.environ["DISCORD_BOT_TOKEN"])
