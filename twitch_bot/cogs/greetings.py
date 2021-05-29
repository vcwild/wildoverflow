import asyncio

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

async def greet_person(data, user_name, channel):
	if user_name in data['streamers']:
		return await sh_person(user_name, channel)
	await say_hello(user_name, channel)
