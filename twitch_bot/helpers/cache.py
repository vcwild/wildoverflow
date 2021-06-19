from collections import defaultdict
from twitch_bot.helpers.decorators import run_once
from .clear_strings import parse_string
from datetime import timedelta

def spawn_cache(channels: list, users: str, streamers: str, database):
	cache = defaultdict(list)
	try:
		for channel in channels:
				cache[channel] = set(parse_string(users))
		cache['users'] = set(parse_string(users))
		cache['streamers'] = set(parse_string(streamers))
		send_from_redis_to_cache(cache, database)

	except BaseException as e:
		print('An exception ocurred {}'.format(e))
	return cache

def add_to_session_cache(data, key, value):
	data[key].add(value)

def send_from_redis_to_cache(cache, conn):
	for key in cache.keys():
		for m in conn.smembers(key):
			cache[key].add(m.decode('utf-8'))

def send_from_cache_to_redis(cache, conn):
	with conn.pipeline() as pipe:
		for set_id, set_value in cache.items():
			pipe.sadd(set_id, *set_value)
			pipe.expire(set_id, timedelta(weeks=1))
		pipe.execute()

# @run_once
def add_all_users_in_chat_to_cache(cache, key, chatters):
	print(f"Adicionou chatters ao cache de `{key}`: {chatters.all}")
	return [cache[key].add(c) for c in chatters.all]
