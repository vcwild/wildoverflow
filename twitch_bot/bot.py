from asyncio import events
import os
import asyncio
import dotenv
from twitchio.ext import commands
from helpers.cache import (add_to_session_cache, spawn_cache)

# Define cog
class TwitchBot(commands.Bot):
	def __init__(self):
		super().__init__(
			irc_token=os.environ['OAUTH_TOKEN'],
			client_id=os.environ['CLIENT_ID'],
			nick=os.environ['BOT_USERNAME'],
			prefix='!',
			initial_channels=[os.environ['CHANNEL_NAME']]
		)

	async def event_ready(self):
		print(f'{self.nick} is ready!')

	async def event_message(self, message):
		user_name = str(message.author.name)
		if user_name == self.nick:
			return
		return await self.handle_commands(message)

	@commands.command(name='42')
	async def message_42(self, ctx):
		msg = os.environ['MSG_42']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='github')
	async def github(self, ctx):
		msg = os.environ['MSG_GITHUB']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='linkedin')
	async def linkedin(self, ctx):
		msg = os.environ['MSG_LINKEDIN']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='twitter')
	async def twitter(self, ctx):
		msg = os.environ['MSG_TWITTER']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='tempo')
	async def tempo(self, ctx):
		msg = os.environ['MSG_TEMPO']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='playlist')
	async def playlist(self, ctx):
		msg = os.environ['MSG_PLAYLIST']
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='sh')
	async def sh_so(self, ctx):
		return

async def greet_person(data, user_name, channel):
	if user_name in data['streamers']:
		return await sh_person(user_name, channel)
	await say_hello(user_name, channel)


if __name__ == "__main__":
	dotenv.load_dotenv()
	cache = spawn_cache(
		users=os.environ['IGNORED_LIST'],
		streamers=os.environ['STREAMER_LIST']
	)
	bot = TwitchBot()

	@bot.event
	async def event_raw_data(data):
		print('\033[33m'+data+'\033[0m')

	@bot.event
	async def event_join(user):
		key = 'users'
		user_name = str(user.name).replace('\r', '')
		channel = bot.get_channel(os.environ['CHANNEL_NAME'])

		if user_name not in cache[key]:
			await greet_person(cache, user_name, channel)
			add_to_session_cache(cache, key, user_name)

			print("usuários no cache: {}".format(cache[key]))

	async def sh_person(user_name, channel):
		loop = asyncio.get_event_loop()
		await loop.create_task(
				channel.send("!sh {}".format(user_name))
			)

	async def say_hello(user_name, channel):
		loop = asyncio.get_event_loop()
		await loop.create_task(
				channel.send("Olá @{}, tudo certo? DarkMode".format(user_name))
			)

	bot.run()
