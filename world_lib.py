MAP_WIDTH = 80
MAP_HEIGHT = 21

#-------------------------------------------------------------------------
class Object():

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
class Tile():
    def __init__(self):
        self.type = None
        self.char = ' '
        self.blocks_move = True
        self.blocks_sight = False
        self.visible = True

    def set_type(self, char, blocks_move, blocks_sight, visible=False):
        self.char = char
        self.blocks_move = blocks_move
        self.blocks_sight = blocks_sight



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
                self.tiles[start_x+x][start_y+y].set_type('.', False, False)

        # create the east and west walls
        for y in range(0, dy):
            self.tiles[start_x][start_y+y].set_type('|', True, True)
            self.tiles[start_x+dx-1][start_y+y].set_type('|', True, True)

        # create the north and south walls
        for x in range(0, dx):
            self.tiles[start_x+x][start_y].set_type('-', True, True)
            self.tiles[start_x+x][start_y+dy-1].set_type('-', True, True)

    def make_hallway(self, start_x, start_y, end_x, end_y):
        for x in range(start_x, end_x+1):
            for y in range(start_y, end_y+1):
                self.tiles[x][y].set_type('#', False, False)

#-------------------------------------------------------------------------
class MessageQueue():
    def __init__(self):
        self.messages = [ ]
        self.history = [ ]

    def add(self, m):
        self.messages.append(m)

    def clear(self):
        self.history.append( self.messages )
        self.messages.clear()


    def get_string(self, wrap_width=80):
        str = ""
        for s in self.messages:
            str += s + " "
        return str






