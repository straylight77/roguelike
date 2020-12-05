import random
import helpers


#-------------------------------------------------------------------------
ITEMS_LIST = {
    "gold": ('$'),
    "healing potion": ('!'),
    "mana potion": ('!'),
    "scroll": ('?'),
}

class Item(helpers.GameObject):
    def __init__(self, name, x=0, y=0):
        char = ITEMS_LIST[name]
        self.name = name
        if name == "gold":
            self.qty = random.randint(3, 12)
        super().__init__(char, x, y)

    def __str__(self):
        if self.name == "gold":
            s = f"{self.qty} gold pieces"
        else:
            s = f"a {self.name}"
        return s

    def quaff(self, player):
        if self.name == "healing potion":
            player.inventory.remove(self)
            player.hp += 5
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            return f"You drink {self}.  You feel great!"
        return None



