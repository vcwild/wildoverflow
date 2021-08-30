from twitch_bot.helpers.files import read_yaml


class DataParser:
    commands = read_yaml("command_messages.yml")
    greetings = read_yaml("greetings.yml")
    ignored_list = read_yaml("ignored_list.yml")
    initial_channels = read_yaml("initial_channels.yml")
    initial_greetings = read_yaml("initial_greetings.yml")
    streamers = read_yaml("streamers.yml")


class Messages:
    def __init__(self):
        self.greetings = DataParser.greetings
        self.initial_greetings = DataParser.initial_greetings
        self.commands = DataParser.commands
