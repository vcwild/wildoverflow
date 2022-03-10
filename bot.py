from twitch_bot.cogs import (
    TwitchBot,
    EventCog,
    MessageCog,
    ManagementCog,
    PlayCog,
)

import warnings
import click
from logging import DEBUG, INFO, basicConfig, captureWarnings, getLogger

logger = getLogger(__name__)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--debug", "-d", help="Enable debug logging", is_flag=True, default=False
)
def main(debug):
    basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(threadName)20s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=DEBUG if debug else INFO,
    )

    def custom_formatwarning(msg, *args, **kwargs):
        return str(msg)

    warnings.formatwarning = custom_formatwarning
    warnings.simplefilter("default")
    captureWarnings(True)

    logger.warning("Starting wildoverflow bot!")


@main.command("run")
def run():
    bot = TwitchBot()

    plugins = [EventCog, MessageCog, ManagementCog, PlayCog]

    [bot.add_cog(plugin(bot)) for plugin in plugins]

    bot.run()


if __name__ == "__main__":
    main()
