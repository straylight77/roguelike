import random
import helpers


#TODO: drop pct
#TODO: add xp
#TODO: list of bosses
#TODO: move to a yaml file?
MONSTERS = {
    # name =>    min, max,    ch, hp, mp, ac, pb
    "rat":       (1,   2,   ('r',  2,  0,  8,  1)),
    "centipede": (1,   3,   ('c',  1,  0,  8,  1)),
    "skeleton":  (2,   5,   ('k',  4,  0, 12,  2)),
    "zombie":    (2,   5,   ('z',  8,  0, 10,  2)),
    "demon":     (3,   10,  ('d',  8,  0, 12,  3)),
}



#-------------------------------------------------------------------------
class Creature(helpers.GameObject):

    def __init__(self, char, hp, mp, ac, prof):
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.ac = ac
        self.prof = prof
        super().__init__(char)

    def __str__(self):
        return self.name

    def can_see(self, floor, x2, y2):
        line = helpers.get_line( (self.x, self.y), (x2, y2) )
        for pt in line:
            x, y = pt
            if floor.tiles[x][y].blocks_sight:
                return False
        return True

    def do_attack(self, defender):
        attack_roll = random.randint(1, 20)
        damage = 3

        #"You attack the <thing> and (crtically) hit/miss."
        #"The <thing> attacks you and (crtically) hits/misses."

        # initial strings for 1st person or 2nd
        if self.name == "you":
            attack_str = f"You attack the {defender}"
            hit_str = "hit!"
            miss_str = "miss."
        else:
            attack_str = f"The {self.name} attacks you"
            hit_str = "hits!"
            miss_str = "misses."

        # check if the attack hits and if it's a crit
        hit = False
        crit_str = ""
        if attack_roll == 20:
            crit_str = "critically "
            hit = True
            damage *= 2
        elif attack_roll == 1:
            crit_str = "critically "
            hit = False
        elif (attack_roll + self.prof) >= defender.ac:
            hit = True

        # apply damage and finally add a message describing the outcome
        if hit:
            debug_str = f" [{attack_roll}, {damage}]"
            outcome_str = hit_str
            defender.hp -= damage
        else:
            debug_str = f" [{attack_roll}]"
            outcome_str = miss_str

        return f"{attack_str}{debug_str} and {crit_str}{outcome_str}"


#-------------------------------------------------------------------------
class Monster(Creature):

    def __init__(self, name, x, y):
        stats = MONSTERS[name][2]
        char, hp, mp, ac, prof = stats
        self.name = name
        super().__init__(char, hp, mp, ac, prof)
        self.set_pos(x, y)
        self.last_player_pos = None

    def update(self, player, floor):
        msg_str = None

        if self.can_see(floor, player.x, player.y):
            d = self.direction_to(player.x, player.y)
        else:
            return

        x2 = self.x + d[0]
        y2 = self.y + d[1]

        t2 = floor.get_tile_at(x2, y2)
        m2 = floor.get_monster_at(x2, y2)

        if player.x == x2 and player.y == y2:
            msg_str = self.do_attack(player)

        elif not t2.blocks_move and m2 == None:
            self.move(d[0], d[1])

        return msg_str


#-------------------------------------------------------------------------
class Player(Creature):

    def __init__(self):
        super().__init__('@', 10, 5, 15, 2)
        self.name = "you"
        self.moves = 0
        self.gold = 0
        self.xp = 0
        self.level = 1
        self.depth = 1
        self.inventory = [ ]

    def pickup(self, i):
        if i.name == "gold":
            self.gold += i.qty
        else:
            self.inventory.append(i)


