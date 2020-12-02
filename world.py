import textwrap
import random

MAP_WIDTH = 80
MAP_HEIGHT = 21

TILE_TYPES = {
    # name => char, blocks_move
    "empty":        (' ', True),
    "floor":        ('.', False),
    "hwall":        ('-', True),
    "vwall":        ('|', True),
    "door_closed":  ('+', True),
    "door_open":    ('`', False),
    "tunnel":       ('#', False),
    "fountain":     ('0', True),
    "altar":        ('&', True),
    "stairs_down":  ('>', False),
    "stairs_up":    ('<', False),
}

MONSTERS = {
    # name => char, hp, mp, ac, prof
    "skeleton": ('k', 4, 0, 12, 2),
    "rat":      ('r', 1, 0, 11, 2),
}


#-------------------------------------------------------------------------
class GameObject():

    def __init__(self, char, x=0, y=0, color=0):
        self.char = char
        self.color = color
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance_from(self, dest_x, dest_y):
        dx = dest_x - self.x
        dy = dest_y - self.y
        distance = ( dx**2 + dy**2 ) ** 0.5
        return distance

    def direction_to(self, dest_x, dest_y):
        dx = 0
        if dest_x < self.x: dx = -1
        if dest_x > self.x: dx = 1

        dy = 0
        if dest_y < self.y: dy = -1
        if dest_y > self.y: dy = 1

        return (dx, dy)

    def get_line(self, start, end):
        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end
        http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points


#-------------------------------------------------------------------------
class Creature(GameObject):

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
        line = self.get_line( (self.x, self.y), (x2, y2) )
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
class Player(Creature):

    def __init__(self):
        super().__init__('@', 10, 5, 15, 2)
        self.name = "you"
        self.moves = 0
        self.gold = 0
        self.xp = 0
        self.level = 1
        self.depth = 1


#-------------------------------------------------------------------------
class Monster(Creature):

    def __init__(self, name, x, y):
        char, hp, mp, ac, prof = MONSTERS[name]
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
class Tile():
    def __init__(self, type=None):
        if type == None:
            type = "empty"
        self.set_type(type)

    def set_type(self, t):
        self.type = t
        self.char = TILE_TYPES[t][0]
        self.blocks_move = TILE_TYPES[t][1]
        self.blocks_sight = self.blocks_move

    def __str__(self):
        return self.name


#-------------------------------------------------------------------------
class Floor():
    def __init__(self):
        self.depth = 1
        self.monsters = [ ]
        self.tiles = [
            [ Tile() for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH)
        ]

    def add_monster(self, m):
        self.monsters.append(m)

    def remove_monster(self, m):
        self.monsters.remove(m)

    def get_monster_at(self, x, y):
        for m in self.monsters:
            if m.x == x and m.y == y:
                return m
        return None

    def get_tile_at(self, x, y):
        return self.tiles[x][y]


    def make_room(self, start_x, start_y, dx, dy):
        # create the floor tiles
        for x in range(0, dx):
            for y in range(0, dy):
                self.tiles[start_x+x][start_y+y].set_type("floor")

        # create the east and west walls
        for y in range(0, dy):
            self.tiles[start_x][start_y+y].set_type("vwall")
            self.tiles[start_x+dx-1][start_y+y].set_type("vwall")

        # create the north and south walls
        for x in range(0, dx):
            self.tiles[start_x+x][start_y].set_type("hwall")
            self.tiles[start_x+x][start_y+dy-1].set_type("hwall")

    def make_tunnel(self, start_x, start_y, end_x, end_y):
        # TODO: this only works when drawing from top-left to bottom-right.
        # It's also inconsistent, should have length+dir instead of second
        # coord.
        for x in range(start_x, end_x+1):
            for y in range(start_y, end_y+1):
                if self.tiles[x][y].type in ("hwall", "vwall"):
                    self.tiles[x][y].set_type("floor")
                else:
                    self.tiles[x][y].set_type("tunnel")


#-------------------------------------------------------------------------
class MessageQueue():
    def __init__(self, wrap_width=80):
        self.messages = [ ]
        self.history = [ ]
        self.wrap_width = wrap_width
        self.wrap = textwrap.TextWrapper(wrap_width)

    def add(self, m):
        if m is None:
            return
        self.messages.append(m)
        self.history.append(m)

    def extend(self, m_list):
        self.messages.extend(m_list)
        self.history.extend(m_list)

    def clear(self):
        self.messages.clear()

    def get_string(self):
        str = ""
        for s in self.messages:
            str += s + " "
        return self.wrap.fill(str)

    def __len__(self):
        return len(self.messages)

    def __str__(self):
        return self.get_string()

    def __iadd__(self, m):
        self.add(m)





