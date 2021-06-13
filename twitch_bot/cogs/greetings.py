import asyncio
from os import pipe
from random import randint
from .greeting_messages import hello_msgs

async def sh_person(user_name, channel):
	loop = asyncio.get_event_loop()
	await loop.create_task(
			channel.send("!sh {}".format(user_name))
		)

async def say_hello(user_name, channel):
	loop = asyncio.get_event_loop()
	msg = hello_msgs[randint(0, len(hello_msgs))]
	await loop.create_task(
			channel.send(msg.format(user_name))
		)

async def greet_person(data, user_name, channel):
	if user_name in data['streamers']:
		return await sh_person(user_name, channel)
	await say_hello(user_name, channel)
