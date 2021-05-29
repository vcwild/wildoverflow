import os
import asyncio
from twitchio.ext import commands


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
