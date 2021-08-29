from datetime import timedelta

from twitchio.ext import commands
from twitchio.dataclasses import Channel, User, Message, Context

from twitch_bot.helpers.decorators import is_mod, message

from random import choice

from twitch_bot.cogs.messages import Messages
from twitch_bot.cogs.data_loader import DataParser
from twitch_bot.helpers.cache import (
    add_to_session_cache,
    send_from_cache_to_redis,
    spawn_cache,
    add_all_users_in_chat_to_cache,
)

import dotenv
import os
import random

import logging
import redis


logger = logging.getLogger(__name__)

dotenv.load_dotenv()


class TwitchBot(commands.Bot):
    def __init__(self, silent_initial=True, interactions=False):
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

        db = redis.Redis(host="0.0.0.0", db=0, socket_timeout=5)

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

    async def sh_person(self, author, channel):
        msg = "!sh {}"

        if author == 'vcwild':
            msg = self.messages.commands['deny_sh']

        await channel.send(msg.format(author))

    async def say_hello(self, author, channel):
        msg = choice(self.messages.greetings)
        await channel.send(msg.format(author))

    async def event_ready(self):
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

    async def event_message(self, message: Message):
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
        author = user.name
        channel = user.channel.name
        if author not in self.cache[channel]:
            await self.greet_person(author, user.channel)

            self.cache[channel].add(author)
            logger.info(
                f"usuários no cache de `{channel}`: {self.cache[channel]}"
            )

            send_from_cache_to_redis(self.cache, self.db, timedelta(days=2))
            logger.info(f"Usuários no cache geral: {list(self.cache.items())}")

    async def greet_person(self, author, channel: Channel):
        """Sh's if the user is a streamer,
        else shows greeting if interactions are active"""
        if author in self.cache['streamers']:
            return await self.sh_person(author, channel)

        if self.interactions:
            await self.say_hello(author, channel)

    @message(name='quarentaedois', aliases=['42', 'quarenta e dois'])
    async def message_42(self, ctx: Context, msg):
        if ctx.channel.name == 'vcwild':
            await ctx.send(msg.format(ctx.author.name))

    @commands.command(
        name='interagir',
        aliases=[
            'interações',
            'falar',
            'desmutar',
            'ativar',
            'ativo',
            'activate',
            'active',
        ],
    )
    async def interact(self, ctx):
        if ctx.author.is_mod:
            self.interactions = True
            return await ctx.send("Opa! Saindo do lurk! Kappa")
        await ctx.send("Foi mal, mas você não pode fazer isso BibleThump")

    @commands.command(name='shh')
    async def shush(self, ctx):
        if ctx.author.is_mod:
            self.interactions = False
            return await ctx.send(self.messages.commands['shush_success'])
        await ctx.send(
            choice(self.messages.commands['generic_fail']).format(
                ctx.author.name
            )
        )

    @commands.command(name='flush_db', aliases=['flush', 'limpar', 'clean'])
    async def flush_database(self, ctx: Context):
        author = ctx.author.name
        channel = ctx.channel.name

        if ctx.author.is_mod:
            members = list(self.db.smembers(channel))

            [self.db.srem(channel, member) for member in members]

            self.cache[channel] = set(self.ignored_list)

            return await ctx.send(
                self.messages.commands['flush_db'].format(author)
            )

        await ctx.send(
            choice(self.messages.commands['generic_fail']).format(author)
        )

    @message(
        name="list_commands",
        aliases=['comandos', 'commands', 'comands', 'comando', 'ajuda', 'help'],
    )
    async def list_command(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='github', aliases=['gh'])
    async def message_github(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='linkedin')
    async def message_linkedin(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='twitter')
    async def message_twitter(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='instagram')
    async def message_instagram(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='tempo')
    async def message_tempo(self, ctx, msg):
        if ctx.channel.name != 'kaduzius':
            await ctx.send(msg.format(ctx.author.name))

    @message(name='ping')
    async def message_ping(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @commands.command(name='sh', aliases=['sh-so'])
    async def sh_so(self, ctx):
        user_name = ctx.message.clean_content.split(' ')[1].lower()
        add_to_session_cache(self.cache, ctx.channel.name, user_name)
        logger.info(f"Adicionado {user_name} ao cache {ctx.channel.name}")

    @message(name='hub', aliases=['ahub', 'hub tech', 'ahub tech'])
    async def message_hub(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='creator', aliases=['seja', 'creators'])
    async def message_creator(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='daviprm', aliases=['daviprm'])
    async def message_davi(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='cafemaker')
    async def message_cafemaker(self, ctx, msg):
        if ctx.channel.name != 'kaduzius':
            await ctx.send(msg)

    @message(name='eurotrip')
    async def eurotrip(self, ctx, msg):
        await ctx.send(msg)

    @message(name='maker')
    async def maker(self, ctx, msg):
        await ctx.send(msg)

    @message(name='jp_amis', aliases=['jp'])
    async def jp_amis(self, ctx, msg):
        await ctx.send(msg)

    @message(name='jeylab', aliases=['json'])
    async def jeylab(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='windows')
    async def windows(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='whatsapp2')
    async def whatsapp_dois(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='dev_caminhante', aliases=['klaus', 'devcaminhante'])
    async def dev_caminhante(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @commands.command(
        name='greeting',
        aliases=[
            'oi',
            'olá',
            'fala',
            'salve',
            'bom',
            'boa',
            'eae',
            'eai',
            'eaí',
        ],
    )
    async def mock_greeting(self, ctx):
        msg = choice(self.messages.greetings)
        await ctx.send(msg.format(ctx.author.name))

    @message(name='tip', aliases=['tips', 'donate', 'doar', 'contribuir'])
    async def tip(self, ctx: Context, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='dornelles', aliases=['dornelestv', '3bc'])
    async def dornelles(self, ctx: Context):
        msg = self.messages.commands['dornelles'].format(ctx.author.name)
        await ctx.send(msg.format(ctx.author.name))
