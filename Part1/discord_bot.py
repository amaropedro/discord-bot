"""
Pedro Amaro
"""

import discord
from discord.ext import commands

from responses_maneger import ResponseManeger
from config_maneger import ConfigManeger
from my_view import MyView


class MyBot():
    """A bot that responds to certain user sent messages in the especified default channel.
        Use '.run(YOUR TOKEN)' method to run.
    """
    def run_bot(self, TOKEN):
        intents = discord.Intents.default()
        intents.message_content = True
        client = commands.Bot(command_prefix="!", intents=intents)
        config = ConfigManeger()

        @client.event
        async def on_ready():
            print(f'{client.user} is now running!')

        @client.command()
        async def bot(ctx):
            if config.is_allowed(str(ctx.channel.id)):
                try:
                    view = MyView(author=ctx.author)
                    view.sent_message = await ctx.send(view=view)
                except Exception as e:
                    print(e)

        @client.event
        async def on_message(ctx):    
            response = ResponseManeger(ctx)

            #ignore own messages
            if ctx.author == client.user:
                return
            
            if config.is_allowed(str(ctx.channel.id)):
                try:
                    await response.send()
                except Exception as e:
                    pass

            await client.process_commands(ctx)

        client.run(TOKEN)
