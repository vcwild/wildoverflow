from collections import defaultdict
from .clear_strings import parse_string
from datetime import timedelta

def spawn_cache(users: str, streamers: str):
	cache = defaultdict(list)
	try:
		cache['users'] = set(parse_string(users))
		cache['streamers'] = set(parse_string(streamers))
	except BaseException as e:
		print('An exception ocurred {}'.format(e))
	return cache

def add_to_session_cache(data, value):
	for key in data.keys():
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
