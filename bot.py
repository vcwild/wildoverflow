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

bot.run()
