"""
Pedro Amaro
"""

class PLayer():
    def __init__(self, discord_id, name): #or recive ctx and acess here
        self.discord_id = discord_id
        self.name = name
        self.level = 1
        self.experience = 0
        self.silver = 0
        self.health = 250
        self.max_health = 250