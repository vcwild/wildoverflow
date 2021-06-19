from twitch_bot.cogs import TwitchBot

bot = TwitchBot()

@bot.event
async def event_raw_data(data):
	print('\033[33m'+data+'\033[0m')

bot.run()
