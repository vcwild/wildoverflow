import asyncio
from random import randint
from twitch_bot.cogs.greeting_messages import hello_msgs

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
