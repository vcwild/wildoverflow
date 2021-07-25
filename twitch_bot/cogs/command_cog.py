from datetime import timedelta

from twitchio.ext import commands
from twitchio.dataclasses import Channel, User, Message, Context

# from twitch_bot.helpers.decorators import is_mod


from random import choice

from twitch_bot.cogs.messages import Messages
from twitch_bot.cogs.data_loader import DataParser
from twitch_bot.helpers.cache import (
    add_to_session_cache,
    send_from_cache_to_redis,
    spawn_cache,
    add_all_users_in_chat_to_cache
)

import asyncio
import dotenv
import os
import random
import redis

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

        db = redis.Redis(
            host="redis",
            db=0,
            socket_timeout=5
        )

        super().__init__(
            irc_token=os.environ['OAUTH_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_USERNAME'],
            prefix=['!', '@wildOverflow ', '@wildoverflow '],
            initial_channels=channels
        )

        self.cache = spawn_cache(
            channels=channels,
            users=ignored_list,
            streamers=streamers,
            database=db
        )

        self.channels = channels
        self.db = db
        self.ignored_list = ignored_list
        self.interactions = interactions

        self.messages = Messages()

        self.silent_initial = silent_initial

    async def sh_person(self, user_name, channel):
        loop = asyncio.get_event_loop()
        await loop.create_task(
            channel.send("!sh {}".format(user_name))
        )

    async def say_hello(self, user_name, channel):
        loop = asyncio.get_event_loop()
        msg = choice(self.messages.greetings)
        await loop.create_task(
            channel.send(msg.format(user_name))
        )

    async def event_ready(self):
        """When the bot is ready to interact with the chat"""
        if self.silent_initial:
            for channel in self.channels:

                chatters = await self.get_chatters(channel)

                add_all_users_in_chat_to_cache(
                    cache=self.cache,
                    key=channel,
                    chatters=chatters
                )

        for channel in self.channels:
            msg = choice(self.messages.initial_greetings)
            await self.get_channel(channel).send(msg)

        print(f'{self.nick} is ready!')

    async def event_message(self, message: Message):
        """Triggers every time the bot receives a new message"""
        if message.author.name == self.nick:
            # TODO: Faltou corrigir porque está bugado e não funciona
            # if not message.author.is_mod:
            #   print(f"{self.nick} partiu de {message.channel.name}")
            #   await self.part_channels([message.channel.name])
            return

        message.content = message.content.lower()
        await self.handle_commands(message)

    async def event_join(self, user: User) -> None:
        """Triggers every time a new user joins the chat"""
        key = user.channel.name
        if user.name not in self.cache[key]:
            await self.greet_person(self.cache, user.name, user.channel)

            self.cache[key].add(user.name)
            # print(f"usuários no cache de `{key}`: {self.cache[key]}")

            send_from_cache_to_redis(self.cache, self.db, timedelta(days=2))
            # print(f"Usuários no cache geral: {list(self.cache.items())}")

    async def greet_person(self, cache, user_name, channel: Channel):
        """Sh's if the user is a streamer,
           else shows greeting if interactions are active"""
        if user_name in cache['streamers'] and user_name not in self.channels:
            return await self.sh_person(user_name, channel)

        if self.interactions:
            await self.say_hello(user_name, channel)

    @commands.command(name='42', aliases=['quarentaedois', 'quarenta e dois'])
    async def message_42(self, ctx: Context):
        if ctx.channel.name == 'vcwild':
            msg = self.messages.commands['MSG_42']
            await ctx.send(msg.format(ctx.author.name))

    @commands.command(
        name='interagir',
        aliases=['interações', 'falar', 'desmutar',
                 'ativar', 'ativo', 'activate', 'active']
    )
    async def interact(self, ctx):
        if ctx.author.is_mod:
            self.interactions = True
            return await ctx.send("Opa! Saindo do lurk! Kappa")
        await ctx.send("Foi mal, mas você não pode fazer isso BibleThump")

    @commands.command(name='shh',
                      aliases=['silêncio', 'quieto', 'silencio', 'xiu',
                               'shiu', 'vacilao', 'vacilão' 'mutado'])
    async def shush(self, ctx):
        if ctx.author.is_mod:
            self.interactions = False
            return await ctx.send(self.messages.commands['MSG_SHUSH_SUCCESS'])
        await ctx.send(choice(self.messages.commands['MSG_GENERIC_FAIL'])
                       .format(ctx.author.name))

    @commands.command(name='flush',
                      aliases=['avc', 'flushdb', 'limpar', 'clean'])
    async def flush_database(self, ctx):
        if ctx.author.is_mod:
            members = list(self.db.smembers(ctx.channel.name))

            [self.db.srem(ctx.channel.name, member) for member in members]

            self.cache[ctx.channel.name] = set(self.ignored_list)

            return await ctx.send(
                self.messages.commands['MSG_FLUSH_DB'].format(ctx.author.name)
            )

        await ctx.send(choice(self.messages.commands['MSG_GENERIC_FAIL'])
                       .format(ctx.author.name))

    @commands.command(name="commands",
                      aliases=['comandos', 'comands', 'comando', 'ajuda'])
    async def list_command(self, ctx):
        if ctx.author.is_mod:
            return await ctx.send("{}, meus comandos são: "
                                  .format(ctx.author.name)
                                  + str(list(self.commands.keys()))[1:-1])
        await ctx.send(self.messages.commands['MSG_LIST_COMMANDS_FAIL']
                       .format(ctx.author.name))

    @commands.command(name="dado", aliases=['dados', 'dice'])
    async def play_dice(self, ctx):
        number = random.randint(0, 6)
        msg = self.messages.commands['MSG_DICE']

        if number == 0:
            msg = self.messages.commands['MSG_DICE_ZERO']

        await ctx.send(msg.format(ctx.author.name, number))

    @commands.command(name='github', aliases=['gh'])
    async def message_github(self, ctx):
        msg = self.messages.commands['MSG_GITHUB']
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @commands.command(name='linkedin')
    async def message_linkedin(self, ctx):
        msg = self.messages.commands['MSG_LINKEDIN']
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @commands.command(name='twitter')
    async def message_twitter(self, ctx):
        msg = self.messages.commands['MSG_TWITTER']
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @commands.command(name='instagram')
    async def message_instagram(self, ctx):
        msg = self.messages.commands['MSG_INSTAGRAM']
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @commands.command(name='tempo')
    async def message_tempo(self, ctx):
        if ctx.channel.name != 'kaduzius':
            msg = self.messages.commands['MSG_TEMPO']
            await ctx.send(msg.format(ctx.author.name))

    @commands.command(name='ping')
    async def message_ping(self, ctx):
        msg = "{} pong!"
        await ctx.send(msg.format(ctx.author.name))

    @commands.command(name='sh', aliases=['sh-so'])
    async def sh_so(self, ctx):
        user_name = ctx.message.clean_content.split(' ')[1].lower()
        add_to_session_cache(self.cache, ctx.channel.name, user_name)
        print(f"Adicionado {user_name} ao cache {ctx.channel.name}")

    @commands.command(name='hub', aliases=['ahub', 'hub tech', 'ahub tech'])
    async def message_hub(self, ctx):
        msg = self.messages.commands['MSG_HUB']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='creator', aliases=['seja', 'creators'])
    async def message_creator(self, ctx):
        msg = self.messages.commands['MSG_CREATOR']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='davi', aliases=['daviprm', 'daviprm_'])
    async def spotted(self, ctx):
        msg = self.messages.commands['MSG_DAVIPRM']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='cafemaker')
    async def cafe_maker(self, ctx):
        if ctx.channel.name != 'kaduzius':
            msg = self.messages.commands['MSG_CAFEMAKER']
            await ctx.send(msg)

    @commands.command(name='eurotrip')
    async def eurotrip(self, ctx):
        msg = self.messages.commands['MSG_EUROTRIP']
        await ctx.send(msg)

    @commands.command(name='maker')
    async def maker(self, ctx):
        msg = self.messages.commands['MSG_MAKER']
        await ctx.send(msg)

    @commands.command(name='jp', aliases=['jp_amis'])
    async def jp_amis(self, ctx):
        msg = self.messages.commands['MSG_JP_AMIS']
        await ctx.send(msg)

    @commands.command(
        name='jey',
        aliases=['jeylab', 'jey_lab', 'jeylab_robotica',
                 'json', 'yaml', 'protobuff']
    )
    async def jeylab(self, ctx):
        msg = self.messages.commands['MSG_JEYLAB']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='windows')
    async def windows(self, ctx):
        msg = self.messages.commands['MSG_WINDOWS']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='whatsapp2')
    async def whatsapp_dois(self, ctx):
        msg = self.messages.commands['MSG_WHATSAPP_DOIS']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='devcaminhante', aliases=['klaus', 'caminhante'])
    async def dev_caminhante(self, ctx):
        msg = self.messages.commands['MSG_DEV_CAMINHANTE']\
            .format(ctx.author.name)
        await ctx.send(msg)

    @commands.command(name='greeting',
                      aliases=['oi', 'olá', 'fala', 'salve',
                               'bom', 'boa', 'eae', 'eai', 'eaí'])
    async def mock_greeting(self, ctx):
        msg = choice(self.messages.greetings)\
            .format(ctx.author.name)
        await ctx.send(msg)
