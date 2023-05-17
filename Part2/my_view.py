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
        start_task() assigns a given task to self.task.
        *_embed() are quality of life methods to help update the view embed with new numbers.
        work() creates the 'Work!' button. It's callback initiates count.
        cancel() creates the 'Cancel' button. It's callback stops the count.
        start_hunting() creates the 'Start Hunting' button. It's callback starts the hunting task. 
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
    
    async def hunting(self, interaction: discord.Interaction):
        if self.task is not None:
            player = playerFactory.get_player(interaction.user.id)            
            if player.level == 4:
                await self.sent_message.edit(embed=None)
                await interaction.followup.send("you have already mastered the hunt.")
                await self.cancel_task()
            elif player.is_fighting:
                await self.sent_message.edit(embed=None)
                await interaction.followup.send("you are already hunting.")
                await self.cancel_task()
            else:
                player.is_fighting = True
                monster = monsters.get_monster(player.level)
                while player.is_fighting:
                    if monster is not None:
                        embed = self.fight_embed(player, monster)
                    else:
                        embed = self.stats_embed(player, player.defeated_monsters)
                    await self.sent_message.edit(embed=embed)

                    if monster is None:
                        monster = monsters.get_monster(player.level)
                    else:
                        monster.health -= 5*player.level
                        if monster.health <=0:
                                player.defeated_monsters += 1
                                player.experience += 10
                                player.silver += 5*monster.level
                                monster = None
                                if player.experience%100 == 0:
                                    player.level+=1
                        else:
                            player.health -= 2*monster.level

                        if player.health <= 0:
                            player.health = player.max_health
                            player.is_fighting = False
                            await interaction.followup.send("you have died")
                            await self.cancel_task()
                        if player.level == 4:
                            player.is_fighting = False
                            await interaction.followup.send("You Won!")
                            await self.cancel_task()
                    await asyncio.sleep(2)

    def fight_embed(self, player, monster):
        embed = discord.Embed(title="Hunting!")
        embed.add_field(name=player.name, value=f"HP = {player.health}   LV = {player.level}")
        embed.add_field(name="VS", value="")
        embed.add_field(name=monster.name, value=f"HP = {monster.health}   LV = {monster.level}")
        return embed

    def stats_embed(self, player, defeated_monsters):
        embed = discord.Embed(title=f"{player.name} is looking for a monster...")
        embed.add_field(name="Monsters Defeated", value=defeated_monsters)
        embed.add_field(name="Total Experience", value=player.experience)
        embed.add_field(name="Silver Gained", value=player.silver)
        embed.add_field(name="Level", value=player.level)
        return embed

    async def update_counter(self):
        while self.task is not None:
            await asyncio.sleep(5)
            self.update_count += 1
            await self.sent_message.edit(embed=self.counter_embed())

    def counter_embed(self):
        embed = discord.Embed(title="Counter")
        embed.add_field(name="current count:", value=self.update_count)
        return embed

    async def disable_all_buttons(self):
        for btn in self.children:
            btn.disabled = True
        await self.sent_message.edit(view=self)

    @discord.ui.button(label="Start Hunting", style=discord.ButtonStyle.success)
    async def start_hunting(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.start_task(self.hunting(interaction))
        await self.disable_all_buttons()
        await interaction.response.defer()

    @discord.ui.button(label="Work!", style=discord.ButtonStyle.primary)
    async def work(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.start_task(self.update_counter())
        button.disabled = True
        button.label = "Working..."
        await interaction.message.edit(view=self)
        await interaction.response.send_message("I started to count. Press 'Cancel' to stop.", ephemeral=True)
        await interaction.message.edit(embed=self.counter_embed())
        
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
        return interaction.user.id == self.author
    
    async def on_timeout(self) -> None:
        if self.task is None:
            if self.sent_message:
                await self.sent_message.delete()
                self.sent_message = None