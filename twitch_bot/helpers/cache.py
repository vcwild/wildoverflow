from collections import defaultdict
from .clear_strings import parse_string

def spawn_cache(users: str, streamers: str):
	cache = defaultdict(list)
	try:
		cache['users'] = parse_string(users)

		cache['streamers'] = parse_string(streamers)
		print(cache)
	except BaseException as e:
		print('An exception ocurred {}'.format(e))
	return cache

def add_to_session_cache(data, key, value):
	data[key].append(value)
