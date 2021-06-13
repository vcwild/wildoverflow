import os
from twitch_bot.helpers.decorators import run_once
import dotenv
from twitch_bot.helpers.cache import (
	add_to_session_cache,
	send_from_redis_to_cache,
	send_from_cache_to_redis,
	spawn_cache
)
from twitch_bot.cogs import command_cog, greetings
import redis

dotenv.load_dotenv()

r = redis.Redis(host=os.environ['REDIS_ENDPOINT'], port=6379, db=0)

cache = spawn_cache(
	users=os.environ['IGNORED_LIST'],
	streamers=os.environ['STREAMER_LIST']
)

send_from_redis_to_cache(cache, r)

bot = command_cog.TwitchBot()

@bot.event
async def event_raw_data(data):
	print('\033[33m'+data+'\033[0m')

@run_once
def add_all_users_in_chat_to_cache_only_once(cache, chatters):
	print(f"Adicionou chatters ao cache: {chatters.all}")
	return [add_to_session_cache(cache, c) for c in chatters.all]

@bot.event
async def event_join(user):
	key = 'users'
	user_name = str(user.name).replace('\r', '')
	channel = bot.get_channel(bot.initial_channels[0])

	add_all_users_in_chat_to_cache_only_once(
		cache,
		await bot.get_chatters(bot.initial_channels[0])
	)

	if user_name not in cache[key]:
		await greetings.greet_person(cache, user_name, channel)

		add_to_session_cache(cache, user_name)
		print("usuários no cache: {}".format(cache[key]))
		send_from_cache_to_redis(cache, r)

# @bot.event
# async def publish_message():
# 	channel = bot.get_channel(bot.initial_channels[0])
# 	loop = asyncio.get_event_loop()
# 	await asyncio.sleep(640000)
# 	loop.create_task(
# 			channel.send(os.environ['MSG_HUB'])
# 		)

bot.run()
