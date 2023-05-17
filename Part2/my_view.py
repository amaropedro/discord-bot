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

    async def cancel_task(self):
        try:
            self.task.cancel()
        except asyncio.CancelledError:
            pass
    
    async def fighting(self, interaction: discord.Interaction):
        if self.task is not None:
            player = playerFactory.get_player(interaction.user.id)
            monster = monsters.get_monster(player.level)

            while True:
                embed = discord.Embed(title="Fight!")
                if monster is not None:
                    embed.add_field(name=player.name, value=f"HP = {player.health}   LV = {player.level}")
                    embed.add_field(name="VS", value="")
                    embed.add_field(name=monster.name, value=f"HP = {monster.health}   LV = {monster.level}")
                else:
                    embed.add_field(name="Looking for a monster...", value="") #change to display other stats
                await self.sent_message.edit(embed=embed)

                if monster is None:
                    monster = monsters.get_monster(player.level)
                else:
                    print("lutando")
                    monster.health -= 5*player.level
                    player.health -= 2*monster.level

                    if player.health <= 0:
                        player.health = player.max_health
                        await interaction.followup.send("you have died")
                        await self.cancel_task()
                    else:
                        if monster.health <=0:
                            player.experience += 10
                            player.silver += 5*monster.level
                            monster = None
                            if player.experience%100 == 0:
                                print("LV UP!")
                                player.level+=1

                        if player.level == 4:
                            await interaction.followup.send("You Won!")
                            await self.cancel_task()
                await asyncio.sleep(2)


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
        self.start_task(self.fighting(interaction))
        await self.disable_all_buttons()
        await interaction.response.defer()

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
            await self.cancel_task()
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