"""
Pedro Amaro
"""

class Monster():
    def __init__(self, name, level, max_health):
        self.name = name
        self.level = level
        self.health = max_health
        self.max_health = max_health

class Rat(Monster):
    def __init__(self):
        super().__init__("Rat", 1, 20)

class Boar(Monster):
    def __init__(self):
        super().__init__("Boar", 2, 40)

class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", 3, 60)


def get_monster(lv: int) -> 'Monster':
    if lv == 1:
        return Rat()
    if lv == 2:
        return Boar()
    return Goblin()