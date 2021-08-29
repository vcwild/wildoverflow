from twitch_bot.cogs import (
    TwitchBot,
    EventCog,
    MessageCog,
    ManagementCog,
    PlayCog,
)

import logging


logger = logging.getLogger(__name__)

bot = TwitchBot()

plugins = [EventCog, MessageCog, ManagementCog, PlayCog]

[bot.add_cog(plugin(bot)) for plugin in plugins]


@bot.event
async def event_raw_data(data):
    logger.debug('\033[33m' + data + '\033[0m')


bot.run()
