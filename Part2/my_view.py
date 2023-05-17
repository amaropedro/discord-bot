"""
Pedro Amaro
"""

import discord
import asyncio
from player import playerFactory
import monsters

class MyView(discord.ui.View):
    """Inherits from discord.ui.view
    
    Implemented methods
    -----------
        interaction_check() now will only allow the user that triggered the message to interact with it.
        on_timeout() now will delete sent message after timeout is reached

    New methods
    -----------
        start_task() assigns a given task to self.task where :
            update_counter() is the counting task;
            fighting() is the fighting task;
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

    def start_task(self, task):
        self.task = asyncio.create_task(task)  

    async def fighting(self, id):
        if self.task is not None:
            player = playerFactory.get_player(id)
            monster = monsters.get_monster(player.level)
            while True:
                if monster is None:
                    player = playerFactory.get_player(id)
                    monster = monsters.get_monster(player.level)
                else:
                    print("lutando")
                    #battle code here
                    pass
                embed = discord.Embed(title="Fight!")
                embed.add_field(name=monster.name + '  -VERSUS-', value=monster.health)
                embed.add_field(name=player.name, value=player.health)
                await self.sent_message.edit(embed=embed)
                await asyncio.sleep(2)
        else:
            #say its occupied
            pass

    async def update_counter(self):
        while self.task is not None:
            await asyncio.sleep(5)
            self.update_count += 1
            await self.sent_message.edit(embed=self.embed())

    def embed(self):
        embed = discord.Embed(title="Counter")
        embed.add_field(name="current count:", value=self.update_count)
        return embed

    async def disable_all_buttons(self):
        for btn in self.children:
            btn.disabled = True
        await self.sent_message.edit(view=self)

    @discord.ui.button(label="Start Hunting", style=discord.ButtonStyle.success)
    async def start_hunting(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.start_task(self.fighting(interaction.user.id))
        await self.disable_all_buttons()
        await interaction.response.send_message("The hunt has started...", ephemeral=True)

    @discord.ui.button(label="Work!", style=discord.ButtonStyle.primary)
    async def work(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.start_task(self.update_counter())
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