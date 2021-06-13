import os
from twitchio.ext import commands


class TwitchBot(commands.Bot):
	def __init__(self):
		super().__init__(
			irc_token=os.environ['OAUTH_TOKEN'],
			client_id=os.environ['CLIENT_ID'],
			nick=os.environ['BOT_USERNAME'],
			prefix=['!', '@wildOverflow ', '@wildoverflow '],
			initial_channels=[os.environ['CHANNEL_NAME']],
			# webhook_server=True,
			# local_host='127.0.0.1',
			# port='9999'
		)

	async def event_ready(self):
		# await self.modify_webhook_subscription(
		# 	mode=twitchio.enums.WebhookMode.subscribe,
		# 	topic=twitchio.webhook.UserFollows(to_id=int(os.environ['USER_ID'])))
		# await self.get_channel(self.initial_channels[0]).send("Bom dia chat TehePelo")
		print(f'{self.nick} is ready!')

	async def event_message(self, message):
		if message.author.name == self.nick: return
		message.content = message.content.lower()
		await self.handle_commands(message)

	@commands.command(name='42', aliases=['quarentaedois', 'quarenta e dois'])
	async def message_42(self, ctx):
		msg = os.environ['MSG_42']
		await ctx.send(msg.format(ctx.author.name))

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
		else: return
		await ctx.send(msg.format(ctx.author.name))

	@commands.command(name='sh')
	async def sh_so(self, ctx):
		return

	@commands.command(name='hub', aliases=['ahub', 'hub tech', 'ahub tech'])
	async def message_hub(self, ctx):
		msg = os.environ['MSG_HUB']
		await ctx.send(msg)

	@commands.command(name="commands",
					  aliases=['comandos', 'comands', 'comando', 'ajuda'])
	async def list_command(self, ctx):
		await ctx.send(
			"{}, meus comandos são: ".format(ctx.author.name) +\
				str(list(self.commands.keys()))[1:-1])
