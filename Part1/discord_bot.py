"""
Pedro Amaro
"""

import discord
from discord.ext import commands

from responses_maneger import ResponseManeger
from config_maneger import ConfigManeger
from my_view import MyView
from task_maneger import taskState


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
            if config.is_allowed(str(ctx.channel)):
                try:
                    view = MyView(author=ctx.author)
                    view.sent_message = await ctx.send(view=view)
                    if taskState.task is None: #e se duas pessoas quiserem contar? se 1 pessoa chamar 2x !bot, fica um mirror
                        taskState.task = client.loop.create_task(view.update_counter())
                except Exception as e:
                    print(e)

        @client.event
        async def on_button_click(interaction):
            view = MyView(author=interaction.author)
            view.sent_message = interaction.message
            await view(interaction)

        @client.event
        async def on_message(ctx):    
            response = ResponseManeger(ctx)
            channel = str(ctx.channel)

            #ignore own messages
            if ctx.author == client.user:
                return
            
            #debug
            print(f"{str(ctx.author)} said: '{str(ctx.content)}' in {str(ctx.channel)}")
            
            if config.is_allowed(channel):
                try:
                    await response.send()
                except Exception as e:
                    print(e)

            await client.process_commands(ctx)

        client.run(TOKEN)
