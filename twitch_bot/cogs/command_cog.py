import os
import random
import dotenv
import redis
from twitch_bot.cogs import greetings
from twitch_bot.helpers.clear_strings import parse_string
from twitchio.ext import commands
from twitch_bot.helpers.cache import (
	add_to_session_cache,
	send_from_cache_to_redis,
	spawn_cache,
	add_all_users_in_chat_to_cache
)

dotenv.load_dotenv()


class TwitchBot(commands.Bot):
	def __init__(self, silent_initial=True, interactions=False):
		channels = list(set(parse_string(os.environ['INITIAL_CHANNELS'])))
		db = redis.Redis(
			host=os.environ['REDIS_ENDPOINT'],
			port=6379,
			db=0)
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
		self.silent_initial = silent_initial

	async def event_ready(self):
		if self.silent_initial:
			for channel in self.channels:
				add_all_users_in_chat_to_cache(
					cache=self.cache,
					key=channel,
					chatters=await self.get_chatters(channel)
				)

		await self.get_channel(self.channels[0]).send(os.environ['MSG_DEFAULT_GREETING'])
		print(f'{self.nick} is ready!')

	async def event_message(self, message):
		if message.author.name == self.nick:
			return

		message.content = message.content.lower()
		await self.handle_commands(message)

	async def event_join(self, user):
			key = user.channel.name

			if user.name not in self.cache[key]:
				await self.greet_person(self.cache, user.name, user.channel)

				self.cache[key].add(user.name)

				print(f"usuários no cache de `{key}`: {self.cache[key]}")

				send_from_cache_to_redis(self.cache, self.db)

				print(f"Usuários no cache geral: {list(self.cache.items())}")

	async def greet_person(self, data, user_name, channel):
		if user_name in data['streamers'] and user_name not in self.channels:
			return await greetings.sh_person(user_name, channel)

		if self.interactions:
			await greetings.say_hello(user_name, channel)

	@commands.command(name='42', aliases=['quarentaedois', 'quarenta e dois'])
	async def message_42(self, ctx):
		if ctx.channel.name == 'vcwild':
			msg = os.environ['MSG_42']
			await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='flush', aliases=['avc', 'flushdb', 'limpar', 'clean'])
	async def flush_database(self, ctx):
		if ctx.author.is_mod:
			members = list(self.db.smembers(ctx.channel.name))

			[self.db.srem(ctx.channel.name, member) for member in members]

			# self.cache.pop(ctx.channel.name)
			self.cache[ctx.channel.name] = set(self.channels)

			return await ctx.send(os.environ['MSG_FLUSH_DB'].format(ctx.author.name))

		await ctx.send(os.environ['MSG_FLUSH_DB_FAIL'].format(ctx.author.name))

	@commands.command(name="commands",
					  aliases=['comandos', 'comands', 'comando', 'ajuda'])
	async def list_command(self, ctx):
		if ctx.author.is_mod:
			return await ctx.send(
				"{}, meus comandos são: ".format(ctx.author.name) +\
					str(list(self.commands.keys()))[1:-1]
			)
		await ctx.send(os.environ['MSG_LIST_COMMANDS_FAIL'].format(ctx.author.name))

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
		await ctx.send(msg.format(ctx.author.name, os.environ['CHANNEL_NAME']))

	@commands.command(name='linkedin')
	async def message_linkedin(self, ctx):
		msg = os.environ['MSG_LINKEDIN']
		await ctx.send(msg.format(ctx.author.name, os.environ['CHANNEL_NAME']))

	@commands.command(name='twitter')
	async def message_twitter(self, ctx):
		msg = os.environ['MSG_TWITTER']
		await ctx.send(msg.format(ctx.author.name, os.environ['CHANNEL_NAME']))

	@commands.command(name='instagram')
	async def message_instagram(self, ctx):
		msg = os.environ['MSG_INSTAGRAM']
		await ctx.send(msg.format(ctx.author.name, os.environ['CHANNEL_NAME']))

	@commands.command(name='tempo')
	async def message_tempo(self, ctx):
		msg = os.environ['MSG_TEMPO']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='playlist')
	async def message_playlist(self, ctx):
		if os.environ['CHANNEL_NAME'] == 'vcwild':
			msg = os.environ['MSG_PLAYLIST']
			await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='sh', aliases=['sh-so'])
	async def sh_so(self, ctx):
		user_name = ctx.message.clean_content.split(' ')[1].lower()
		add_to_session_cache(self.cache, user_name)

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
