
# ---- test data ---------
def make_test_floor(floor, player):
    #make a simple dungeon map for testing
    floor.make_room(10, 5, 8, 5)
    floor.make_room(32, 8, 16, 6)
    floor.make_room(18, 6, 7, 3)
    floor.tiles[17][7].set_type('/', False, False)
    floor.tiles[18][7].set_type('.', False, False)

    floor.make_room(22, 8, 3, 5)
    floor.tiles[23][8].set_type('.', False, False)
    floor.tiles[24][8].set_type('|', True, True)

    floor.make_room(25, 10, 8, 3)
    floor.tiles[24][11].set_type('.', False, False)
    floor.tiles[25][11].set_type('.', False, False)
    floor.tiles[24][10].set_type('-', True, True)

    floor.tiles[32][10].set_type('|', True, True)
    floor.tiles[32][12].set_type('|', True, True)
    floor.tiles[32][11].set_type('+', False, False)

    player.set_pos(12, 7)

def make_test_floor2(floor, player):
    #make a simple dungeon map for testing
    floor.make_room(10, 5, 8, 5)
    floor.tiles[17][7].set_type('/', False, False)
    floor.make_room(32, 8, 16, 6)
    floor.tiles[32][11].set_type('+', False, False)

    floor.make_hallway(18, 7, 25, 7)
    floor.make_hallway(25, 7, 25, 11)
    floor.make_hallway(25, 11, 31, 11)
    player.set_pos(12, 7)



