import logging
from twitch_bot.cogs.twitch import TwitchBot


class Plugin:
    """Class for all bot plugins"""

    def __init__(self, bot: TwitchBot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
