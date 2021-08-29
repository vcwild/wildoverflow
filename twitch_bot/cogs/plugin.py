import logging


class Plugin:
    """Class for all bot plugins"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
