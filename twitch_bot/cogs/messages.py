from twitch_bot.cogs.data_loader import DataParser


class Messages:

    def __init__(self):
        self.greetings = DataParser.greetings
        self.initial_greetings = DataParser.initial_greetings
        self.commands = DataParser.commands
