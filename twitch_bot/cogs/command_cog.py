from datetime import timedelta
import os
import random
import dotenv
import redis

from twitchio.ext import commands
from twitchio.dataclasses import Channel, User, Message, Context

from twitch_bot.cogs import greetings
from twitch_bot.helpers.clear_strings import parse_string
from twitch_bot.cogs import greeting_messages
from twitch_bot.helpers.cache import (
	add_to_session_cache,
	send_from_cache_to_redis,
	spawn_cache,
	add_all_users_in_chat_to_cache
)

from .greeting_messages import initial_greetings

dotenv.load_dotenv()

class TwitchBot(commands.Bot):
	def __init__(self, silent_initial=True, interactions=False):
		"""Twitch Bot class

		Args:
			silent_initial (bool, optional): When the bot starts, should it add all chatters into the session cache. Defaults to True.
			interactions (bool, optional): If the bot should show a greeting message when someone joins the chat. Defaults to False.
		"""
		channels = list(set(parse_string(os.environ['INITIAL_CHANNELS'])))
		ignored_list = list(set(parse_string(os.environ['IGNORED_LIST'])))
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
			initial_channels=channels,
		)
		self.cache = spawn_cache(
			channels=channels,
			users=os.environ['IGNORED_LIST'],
			streamers=os.environ['STREAMER_LIST'],
			database=db
		)
		self.channels = channels
		self.db = db
		self.interactions = interactions
		self.ignored_list = ignored_list
		self.silent_initial = silent_initial

	async def event_ready(self):
		"""When the bot is ready to interact with the chat"""
		if self.silent_initial:
			for channel in self.channels:
				add_all_users_in_chat_to_cache(
					cache=self.cache,
					key=channel,
					chatters=await self.get_chatters(channel)
				)
		for channel in self.channels:
			msg = random.choice(initial_greetings)
			await self.get_channel(channel).send(msg)

		print(f'{self.nick} is ready!')

	async def event_message(self, message: Message):
		"""Triggers every time the bot receives a new message"""
		if message.author.name == self.nick:
			# TODO: Faltou corrigir porque está bugado e não funciona
			# if not message.author.is_mod:
			# 	print(f"{self.nick} partiu de {message.channel.name}")
			# 	await self.part_channels([message.channel.name])
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
		"""Sh's if the user is a streamer, else shows greeting if interactions are active"""
		if user_name in cache['streamers'] and user_name not in self.channels:
			return await greetings.sh_person(user_name, channel)

		if self.interactions:
			await greetings.say_hello(user_name, channel)

	@commands.command(name='42', aliases=['quarentaedois', 'quarenta e dois'])
	async def message_42(self, ctx):
		if ctx.channel.name == 'vcwild':
			msg = os.environ['MSG_42']
			await ctx.send(msg.format(ctx.author.name))

	@commands.command(
        name='interagir',
        aliases=['interações', 'fala', 'falar', 'desmutar']
    )
	async def interact(self, ctx):
		if ctx.author.is_mod:
			self.interactions = True
			return await ctx.send("Interações ativadas!")
		await ctx.send("Foi mal, mas você não pode fazer isso BibleThump")

	@commands.command(
        name='shh',
        aliases=[
            'silêncio', 'quieto', 'silencio', 'xiu','shiu',
            'vacilao', 'vacilão' 'mutado'
        ]
    )
	async def shush(self, ctx):
		if ctx.author.is_mod:
			self.interactions = False
			return await ctx.send("Tá bom, vou ficar quieto :(")
		await ctx.send(os.environ['MSG_GENERIC_FAIL'].format(ctx.author.name))

	@commands.command(
        name='flush',
        aliases=['avc', 'flushdb', 'limpar', 'clean']
    )
	async def flush_database(self, ctx):
		if ctx.author.is_mod:
			members = list(self.db.smembers(ctx.channel.name))

			[self.db.srem(ctx.channel.name, member) for member in members]

			self.cache[ctx.channel.name] = set(self.ignored_list)

			return await ctx.send(
                os.environ['MSG_FLUSH_DB'].format(ctx.author.name)
            )

		await ctx.send(os.environ['MSG_GENERIC_FAIL'].format(ctx.author.name))

	@commands.command(
        name="commands",
		aliases=['comandos', 'comands', 'comando', 'ajuda']
    )
	async def list_command(self, ctx):
		if ctx.author.is_mod:
			return await ctx.send(
				"{}, meus comandos são: ".format(ctx.author.name) +\
					str(list(self.commands.keys()))[1:-1]
			)
		await ctx.send(
            os.environ['MSG_LIST_COMMANDS_FAIL'].format(ctx.author.name)
        )

	@commands.command(name="dado", aliases=['dados', 'dice'])
	async def play_dice(self, ctx):
		number = random.randint(0, 6)
		msg = os.environ['MSG_DICE']

		if number == 0:
			msg = os.environ['MSG_DICE_ZERO']

		await ctx.send(msg.format(ctx.author.name, number))

	@commands.command(name='github', aliases=['gh'])
	async def message_github(self, ctx):
		msg = os.environ['MSG_GITHUB']
		await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

	@commands.command(name='linkedin')
	async def message_linkedin(self, ctx):
		msg = os.environ['MSG_LINKEDIN']
		await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

	@commands.command(name='twitter')
	async def message_twitter(self, ctx):
		msg = os.environ['MSG_TWITTER']
		await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

	@commands.command(name='instagram')
	async def message_instagram(self, ctx):
		msg = os.environ['MSG_INSTAGRAM']
		await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

	@commands.command(name='tempo')
	async def message_tempo(self, ctx):
		if ctx.channel.name != 'kaduzius':
			msg = os.environ['MSG_TEMPO']
			await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='ping')
	async def message_ping(self, ctx):
		msg = "{} pong!"
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='playlist')
	async def message_playlist(self, ctx):
		if ctx.channel.name == 'vcwild':
			msg = os.environ['MSG_PLAYLIST']
			await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='sh', aliases=['sh-so'])
	async def sh_so(self, ctx):
		user_name = ctx.message.clean_content.split(' ')[1].lower()
		add_to_session_cache(self.cache, ctx.channel.name, user_name)
		print(f"Adicionado {user_name} ao cache {ctx.channel.name}")

	@commands.command(name='hub', aliases=['ahub', 'hub tech', 'ahub tech'])
	async def message_hub(self, ctx):
		msg = os.environ['MSG_HUB']
		await ctx.send(msg)

	@commands.command(name='davi', aliases=['daviprm', 'daviprm_'])
	async def spotted(self, ctx):
		msg = os.environ['MSG_DAVIPRM'].format(ctx.author.name)
		await ctx.send(msg)

	@commands.command(name='cafemaker')
	async def cafe_maker(self, ctx):
		if ctx.channel.name != 'kaduzius':
			msg = os.environ['MSG_CAFEMAKER']
			await ctx.send(msg)

	@commands.command(name='eurotrip')
	async def eurotrip(self, ctx):
		msg = os.environ['MSG_EUROTRIP']
		await ctx.send(msg)

	@commands.command(name='maker')
	async def maker(self, ctx):
		msg = os.environ['MSG_MAKER']
		await ctx.send(msg)

	@commands.command(name='jp', aliases=['jp_amis'])
	async def jp_amis(self, ctx):
		msg = os.environ['MSG_JP_AMIS']
		await ctx.send(msg)

	@commands.command(
        name='jey',
        aliases=[
            'jeylab',
            'jey_lab',
            'jeylab_robotica',
            'json',
            'yaml',
            'protobuff'
        ]
    )
	async def jeylab(self, ctx):
		msg = os.environ['MSG_JEYLAB'].format(ctx.author.name)
		await ctx.send(msg)

	@commands.command(name='windows')
	async def windows(self, ctx):
		msg = "/me {}, você quis dizer KDE Plasma?".format(ctx.author.name)
		await ctx.send(msg)

	@commands.command(name='whatsapp2')
	async def whatsapp_dois(self, ctx):
		msg = "/me cê viu que lançaram o whatsapp 2?? 😳😳😳😳😳😳😳😳😳😳😳😳😳😳 +353 833152259984 (Whats do em1dio)"
		await ctx.send(msg)
