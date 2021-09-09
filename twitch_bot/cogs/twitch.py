import logging
import os
from datetime import timedelta
from random import choice

import dotenv
import redis
from twitchio.dataclasses import Channel, Context, Message, User
from twitchio.ext import commands

from twitch_bot.cogs.data_loader import DataParser, Messages
from twitch_bot.helpers.cache import (
    add_all_users_in_chat_to_cache,
    add_to_session_cache,
    send_from_cache_to_redis,
    spawn_cache,
)


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

dotenv.load_dotenv()


class TwitchBot(commands.Bot):
    def __init__(self, silent_initial: bool = True, interactions: bool = False):
        """Twitch Bot class

        Args:
            silent_initial (bool, optional): When the bot starts, should it add
            all chatters into the session cache. Defaults to True.
            interactions (bool, optional): If the bot should show a greeting
            message when someone joins the chat. Defaults to False.
        """

        channels = DataParser.initial_channels

        ignored_list = DataParser.ignored_list

        streamers = DataParser.streamers

        db = redis.Redis(
            host=os.environ['DATABASE_HOST'], db=0, socket_timeout=5
        )

        super().__init__(
            irc_token=os.environ['OAUTH_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_USERNAME'],
            prefix=['!', '@wildOverflow ', '@wildoverflow '],
            initial_channels=channels,
        )

        self.cache = spawn_cache(
            channels=channels,
            users=ignored_list,
            streamers=streamers,
            database=db,
        )

        self.channels = channels

        self.db = db

        self.ignored_list = ignored_list

        self.interactions = interactions

        self.messages = Messages()

        self.silent_initial = silent_initial

    async def sh_person(self, author: str, channel: Channel) -> None:
        msg = "!sh {}"

        if author == 'vcwild' or author == channel.name:
            msg = self.messages.commands['deny_sh']

        await channel.send(msg.format(author))

    async def say_hello(self, author: str, channel: Channel) -> None:
        msg = choice(self.messages.greetings)
        await channel.send(msg.format(author))

    async def greet_person(self, author: str, channel: Channel) -> None:
        """Sh's if the user is a streamer,
        else shows greeting if interactions are active"""
        if author in self.cache['streamers']:
            return await self.sh_person(author, channel)

        if self.interactions:
            await self.say_hello(author, channel)

    async def event_ready(self) -> None:
        """When the bot is ready to interact with the chat"""
        if self.silent_initial:
            for channel in self.channels:

                chatters = await self.get_chatters(channel)

                add_all_users_in_chat_to_cache(
                    cache=self.cache, key=channel, chatters=chatters
                )

        for channel in self.channels:
            msg = choice(self.messages.initial_greetings)
            await self.get_channel(channel).send(msg)

        logger.info(f'{self.nick} is ready!')

    async def event_message(self, message: Message) -> None:
        """Triggers every time the bot receives a new message"""
        author = message.author.name
        channel = message.channel.name
        myself = self.nick

        if (
            author not in self.cache[channel]
            and author != channel
            and author != myself
        ):
            await self.greet_person(author, message.channel)

            self.cache[channel].add(author)

        message.content = message.content.lower()

        await self.handle_commands(message)

    async def event_join(self, user: User) -> None:
        """Triggers every time a new user joins the chat"""
        send_from_cache_to_redis(self.cache, self.db, timedelta(days=2))
        logger.info(f"Usuários no cache geral: {list(self.cache.items())}")

    @commands.command(
        name='interagir',
        aliases=['falar', 'desmutar', 'ativar', 'ativo', 'activate', 'active'],
    )
    async def interact(self, ctx: Context) -> None:
        if ctx.author.is_mod:
            self.interactions = True
            return await ctx.send("Opa! Saindo do lurk! Kappa")
        await ctx.send("Foi mal, mas você não pode fazer isso BibleThump")

    @commands.command(name='shh')
    async def shush(self, ctx: Context) -> None:
        if ctx.author.is_mod:
            self.interactions = False
            return await ctx.send(self.messages.commands['shush_success'])
        await ctx.send(
            choice(self.messages.commands['generic_fail']).format(
                ctx.author.name
            )
        )

    @commands.command(name='sh', aliases=['sh-so'])
    async def sh_so(self, ctx: Context) -> None:
        streamer = ctx.message.clean_content.split(' ')[1].lower()
        add_to_session_cache(self.cache, ctx.channel.name, streamer)
        logger.warning(f"Adicionado {streamer} ao cache {ctx.channel.name}")

    @commands.command(
        name='greeting',
        aliases=['oi', 'olá', 'fala', 'salve', 'bom', 'boa', 'alo', 'tudo'],
    )
    async def mock_greeting(self, ctx: Context) -> None:
        msg = choice(self.messages.greetings)
        await ctx.send(msg.format(ctx.author.name))
