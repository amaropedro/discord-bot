"""
Pedro Amaro
"""

import discord
import asyncio

class MyView(discord.ui.View):
    """Inherits from discord.ui.view
    
    Implemented methods
    -----------
        interaction_check() now will only allow the user that triggered the message to interact with it.
        on_timeout() now will delete sent message after timeout is reached

    New methods
    -----------
        start_task() assigns update_counter() task to self.task, which starts count.
        embed() is a quality of life method to help update the view embed with new numbers.
        work() creates the 'Work!' button. Its callback initiates count.
        cancel() creates the 'Cancel' button. Its callback stops the count.
    """
    def __init__(self, author, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.sent_message = None
        self.task = None
        self.update_count = 0

    def start_task(self):
        self.task = asyncio.create_task(self.update_counter())  

    async def update_counter(self):
        while self.task is not None:
            await asyncio.sleep(5)
            self.update_count += 1
            await self.sent_message.edit(embed=self.embed())

    def embed(self):
        embed = discord.Embed(title="Counter")
        embed.add_field(name="current count:", value=self.update_count)
        return embed

    @discord.ui.button(label="Work!", style=discord.ButtonStyle.primary)
    async def work(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.start_task()
        button.disabled = True
        button.label = "Working..."
        await interaction.message.edit(view=self)
        await interaction.response.send_message("I started to count. Press 'Cancel' to stop.", ephemeral=True)
        await interaction.message.edit(embed=self.embed())
        
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.task is not None:
            self.task.cancel()
            self.update_count = 0
            self.task = None
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("Goodbye")
        

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author
    
    async def on_timeout(self) -> None:
        if self.task is None:
            if self.sent_message:
                await self.sent_message.delete()
                self.sent_message = None