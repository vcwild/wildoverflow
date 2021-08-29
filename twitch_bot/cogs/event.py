from twitch_bot.cogs.plugin import Plugin


class EventCog(Plugin):
    async def event_ready(self):
        print(f"{self.__class__.__name__} is plugged in!")
