from twitch_bot.helpers.files import read_yaml


class DataParser:
    commands = read_yaml("command_messages.yml")
    creators = read_yaml("creators.yml")
    greetings = read_yaml("greetings.yml")
    ignored_list = read_yaml("ignored_list.yml")
    initial_channels = read_yaml("initial_channels.yml")
    initial_greetings = read_yaml("initial_greetings.yml")
    streamers = read_yaml("streamers.yml")
