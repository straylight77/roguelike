
# ---- test data ---------
def make_test_floor(floor, player):
    #make a simple dungeon map for testing
    floor.make_room(10, 5, 8, 5)
    floor.make_room(32, 8, 16, 6)
    floor.make_room(18, 6, 7, 3)
    floor.tiles[17][7].set_type("door_closed")
    floor.tiles[18][7].set_type("floor")

    floor.make_room(22, 8, 3, 5)
    floor.tiles[23][8].set_type("floor")
    floor.tiles[24][8].set_type("vwall")

    floor.make_room(25, 10, 8, 3)
    floor.tiles[24][11].set_type("floor")
    floor.tiles[25][11].set_type("floor")
    floor.tiles[24][10].set_type("hwall")

    floor.tiles[32][10].set_type("vwall")
    floor.tiles[32][12].set_type("vwall")
    floor.tiles[32][11].set_type("door_closed")

    player.set_pos(12, 7)

def make_test_floor2(floor, player):
    #make a simple dungeon map for testing
    floor.make_room(10, 5, 8, 5)
    floor.make_room(32, 8, 16, 6)

    floor.make_tunnel(17, 7, 25, 7)
    floor.make_tunnel(25, 7, 25, 11)
    floor.make_tunnel(25, 11, 32, 11)

    floor.tiles[17][7].set_type("door_closed")
    floor.tiles[32][11].set_type("door_closed")

    floor.make_room(5, 13, 12, 5)
    floor.make_tunnel(13, 9, 13, 13)
    floor.make_tunnel(16, 15, 43, 15)
    floor.make_tunnel(43, 13, 43, 15)

    floor.make_room(52, 3, 12, 5)
    floor.make_room(55, 12, 8, 6)
    floor.make_tunnel(47, 10, 58, 10)
    floor.make_tunnel(59, 7, 59, 12)
    floor.tiles[59][7].set_type("door_closed")
    floor.tiles[59][12].set_type("door_closed")

    player.set_pos(12, 7)



