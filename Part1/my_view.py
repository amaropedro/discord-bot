"""
Pedro Amaro
"""

import discord
import asyncio
from task_maneger import taskState

class MyView(discord.ui.View):
    """Inherits from discord.ui.view
    
    Implemented methods
    -----------
        interaction_check() now will only allow the user that triggered the message to interact with it.
        on_timeout() now will delete sent message after timeout is reached

    New methods
    -----------
        
    """
    def __init__(self, author, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.sent_message = None

    async def update_counter(self):
        while True:
            await asyncio.sleep(5)
            taskState.update_count += 1
            await self.sent_message.edit(embed=self.embed())

    def embed(self):
        embed = discord.Embed(title="Counter")
        embed.add_field(name="current count:", value=taskState.update_count)
        return embed

    @discord.ui.button(label="Work!", style=discord.ButtonStyle.primary)
    async def work(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.label = "Working..."
        await interaction.message.edit(view=self)
        await interaction.response.send_message("I started to count. Press 'Cancel' to stop.", ephemeral=True)
        await interaction.message.edit(embed=self.embed())
        
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if taskState.task is not None:
            taskState.task.cancel()
            taskState.update_count = 0
            taskState.task = None
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("Goodbye")
        

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author
    
    async def on_timeout(self) -> None:
        if taskState.task is None:
            if self.sent_message:
                await self.sent_message.delete()
                self.sent_message = None