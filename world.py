import textwrap
import math

MAP_WIDTH = 80
MAP_HEIGHT = 21

TILE_TYPES = {
    # name => char, blocks_move
    "empty":        (' ', True),
    "floor":        ('.', False),
    "hwall":        ('-', True),
    "vwall":        ('|', True),
    "door_closed":  ('+', True),
    "door_open":    ('/', False),
    "tunnel":       ('#', False)
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
        distance = math.sqrt( dx**2 + dy**2 )
        return distance

    def direction_to(self, dest_x, dest_y):
        dx = 0
        if dest_x < self.x: dx = -1
        if dest_x > self.x: dx = 1

        dy = 0
        if dest_y < self.y: dy = -1
        if dest_y > self.y: dy = 1

        return (dx, dy)


#-------------------------------------------------------------------------
class Creature(GameObject):

    def __init__(self, char, hp, mp, ac, prof):
        self.hp = { "max": hp, "current": hp }
        self.mp = { "max": mp, "current": mp }
        self.ac = ac
        self.prof = prof
        super().__init__(char)

#-------------------------------------------------------------------------
class Player(Creature):

    def __init__(self):
        super().__init__('@', 10, 5, 15, 2)
        self.name = "you"
        self.moves = 0
        self.gold = 0
        self.xp = 0
        self.level = 1


#-------------------------------------------------------------------------
class Monster(Creature):

    def __init__(self, name, x, y):
        m = MONSTERS[name]
        self.name = name
        super().__init__(m[0], m[1], m[2], m[3], m[4])
        self.set_pos(x, y)



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



#-------------------------------------------------------------------------
class Floor():
    def __init__(self):
        self.tiles = [
            [ Tile() for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH)
        ]

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

    def make_hallway(self, start_x, start_y, end_x, end_y):
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
    def __init__(self, wrap_width=75):
        self.messages = [ ]
        self.history = [ ]
        self.wrap_width = wrap_width
        self.wrap = textwrap.TextWrapper(wrap_width)

    def add(self, m):
        self.messages.append(m)
        self.history.append(m)

    def clear(self):
        self.messages.clear()

    def get_string(self):
        str = ""
        for s in self.messages:
            str += s + " "
        return self.wrap.fill(str)






