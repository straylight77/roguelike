import textwrap

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

#-------------------------------------------------------------------------
class Creature(GameObject):

    def __init__(self, char):
        self.hp = { "max": 10, "current": 10 }
        self.mp = { "max": 5, "current": 5 }
        self.ac = 10
        self.prof = 2
        super().__init__(char)

#-------------------------------------------------------------------------
class Player(Creature):

    def __init__(self):
        super().__init__('@')
        self.moves = 0
        self.gold = 0
        self.xp = 0
        self.level = 1


#-------------------------------------------------------------------------
class Monster(Creature):

    def __init__(self, name, char, x, y):
        super().__init__(char)
        self.name = name
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






