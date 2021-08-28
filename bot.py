from twitch_bot.cogs import TwitchBot

import logging


logger = logging.getLogger(__name__)

bot = TwitchBot()


@bot.event
async def event_raw_data(data):
    logger.debug('\033[33m' + data + '\033[0m')


bot.run()
