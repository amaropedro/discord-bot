"""
Pedro Amaro
"""

class PlayerFactory():
    def __init__(self):
        self.players = {}
    
    def create_newPlayer(self, ctx):
        if ctx.author.id not in self.players:
            self.players[ctx.author.id] = Player(ctx.author.id, ctx.author)
            
    
    def get_player(self, id) -> 'Player':
        """ Takes discord.Interaction.user.id
        """
        return self.players[id]

class Player():
    def __init__(self, discord_id, name):
        self.discord_id = discord_id
        self.name = name
        self.level = 1
        self.experience = 0
        self.silver = 0
        self.health = 250
        self.max_health = 250
        self.defeated_monsters = 0
        self.is_fighting = False

playerFactory = PlayerFactory()