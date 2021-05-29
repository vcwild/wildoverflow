import os
import dotenv
from helpers.cache import (add_to_session_cache, spawn_cache)
from cogs import command_cog, greetings


dotenv.load_dotenv()

cache = spawn_cache(
	users=os.environ['IGNORED_LIST'],
	streamers=os.environ['STREAMER_LIST']
)
bot = command_cog.TwitchBot()

@bot.event
async def event_raw_data(data):
	print('\033[33m'+data+'\033[0m')

@bot.event
async def event_join(user):
	key = 'users'
	user_name = str(user.name).replace('\r', '')
	channel = bot.get_channel(os.environ['CHANNEL_NAME'])

	if user_name not in cache[key]:
		await greetings.greet_person(cache, user_name, channel)
		add_to_session_cache(cache, key, user_name)

		print("usuários no cache: {}".format(cache[key]))

bot.run()
