import random

from twitchio.dataclasses import Context
from twitch_bot.cogs.plugin import Plugin
from twitchio.ext import commands


class PlayCog(Plugin):
    async def event_ready(self):
        self.logger.warning(f"{self.__class__.__name__} is plugged in!")

    @commands.command(name="dice", aliases=["dados", "dado"])
    async def play_dice(self, ctx: Context) -> None:
        number = random.randint(0, 6)
        msg = self.bot.messages.commands["dice"]

        if number == 0:
            msg = self.bot.messages.commands["dice_zero"]

        await ctx.send(msg.format(ctx.author.name, number))
