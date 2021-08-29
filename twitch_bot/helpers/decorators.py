from functools import wraps
from twitchio.ext import commands


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


def is_mod(f):
    @wraps(f)
    async def wrapper(self, ctx):
        if ctx.author.is_mod:
            await f(self, ctx)

    return wrapper


def message(name, aliases=None, *args, **kwargs):
    def decorator(func):
        @wraps(func)
        @commands.command(name=name, aliases=aliases, *args, **kwargs)
        async def wrapper(self, ctx):
            await func(self, ctx, self.messages.commands[name])

        return wrapper

    return decorator
