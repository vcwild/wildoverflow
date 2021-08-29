from twitch_bot.cogs.plugin import Plugin
from twitchio.dataclasses import Context
from twitch_bot.helpers.decorators import message


class MessageCog(Plugin):
    """Cog for the bot messages"""

    async def event_ready(self):
        print(f"{self.__class__.__name__} is plugged in!")

    @message(name='quarentaedois', aliases=['42', 'quarenta e dois'])
    async def message_42(self, ctx: Context, msg):
        if ctx.channel.name == 'vcwild':
            await ctx.send(msg.format(ctx.author.name))

    @message(
        name="list_commands",
        aliases=['comandos', 'commands', 'comands', 'comando', 'ajuda', 'help'],
    )
    async def message_list_command(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='github', aliases=['gh'])
    async def message_github(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='linkedin')
    async def message_linkedin(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='twitter')
    async def message_twitter(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='instagram')
    async def message_instagram(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='tempo')
    async def message_tempo(self, ctx, msg):
        if ctx.channel.name != 'kaduzius':
            await ctx.send(msg.format(ctx.author.name))

    @message(name='ping')
    async def message_ping(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='hub', aliases=['ahub', 'hub tech', 'ahub tech'])
    async def message_hub(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='creator', aliases=['seja', 'creators'])
    async def message_creator(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='daviprm', aliases=['davi'])
    async def message_davi(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='cafemaker')
    async def message_cafemaker(self, ctx, msg):
        if ctx.channel.name != 'kaduzius':
            await ctx.send(msg)

    @message(name='eurotrip')
    async def message_eurotrip(self, ctx, msg):
        await ctx.send(msg)

    @message(name='maker')
    async def message_maker(self, ctx, msg):
        await ctx.send(msg)

    @message(name='jp_amis', aliases=['jp'])
    async def message_jp_amis(self, ctx, msg):
        await ctx.send(msg)

    @message(name='jeylab', aliases=['json'])
    async def message_jeylab(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='windows')
    async def message_windows(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='whatsapp2')
    async def message_whatsapp_dois(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='dev_caminhante', aliases=['klaus', 'devcaminhante'])
    async def message_dev_caminhante(self, ctx, msg):
        await ctx.send(msg.format(ctx.author.name))

    @message(name='tip', aliases=['tips', 'donate', 'doar', 'contribuir'])
    async def message_tip(self, ctx: Context, msg):
        await ctx.send(msg.format(ctx.author.name, ctx.channel.name))

    @message(name='dornelles', aliases=['dornelestv', '3bc'])
    async def message_dornelles(self, ctx: Context):
        msg = self.messages.commands['dornelles'].format(ctx.author.name)
        await ctx.send(msg.format(ctx.author.name))
