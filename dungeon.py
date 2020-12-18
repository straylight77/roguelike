import helpers
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

    def __init__(self, depth=1):
        self.depth = depth
        self.monsters = [ ]
        self.items = [ ]
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

    def add_item(self, i):
        self.items.append(i)

    def remove_item(self, i):
        self.items.remove(m)

    def get_item_at(self, x, y):
        for m in self.items:
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

