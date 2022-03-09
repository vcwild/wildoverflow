from random import choice
from twitch_bot.cogs.plugin import Plugin
from twitchio.dataclasses import Context
from twitchio.ext import commands


class ManagementCog(Plugin):
    """Cog for managing the bot"""

    async def event_ready(self) -> None:
        self.logger.warning(f"{self.__class__.__name__} is plugged in!")

    @commands.command(name="flush_db", aliases=["flush", "limpar", "clean"])
    async def flush_database(self, ctx: Context) -> None:
        author = ctx.author.name

        channel = ctx.channel.name

        msg = choice(self.bot.messages.commands["generic_fail"])

        if ctx.author.is_mod:
            members = list(self.bot.db.smembers(channel))

            [self.bot.db.srem(channel, member) for member in members]

            self.bot.cache[channel] = set(self.bot.ignored_list)

            msg = self.bot.messages.commands["flush_db"]

        await ctx.send(msg.format(author))
