import dungeon
import random
import helpers

def default_random_floor(floor, player):
    rdg_simple_v1(floor, player, player.depth, 6)


def random_direction(ignore=None):
    dirs = ["N", "E", "W", "S"]
    if ignore is not None:
        dirs.remove(ignore)
    i = random.randint(0, len(dirs)-1)
    return dirs[i]


def random_feature():
    return "tunnel"


def random_line_seg():
    pass


def random_rect():
    dx = random.randint(8, 12)
    dy = random.randint(6, 8)

    x = random.randint(0, dungeon.MAP_WIDTH-dx)
    y = random.randint(0, dungeon.MAP_HEIGHT-dy)

    rect = helpers.Rect( (x,y), dx, dy )
    return rect


def opposite_direction(direction):
    lookup = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E'
    }
    return lookup[direction]


def make_line_segs(pt1, pt2, horiz=0):
    x1, y1 = pt1
    x2, y2 = pt2

    dx = x2 - x1
    dy = y2 - y1


    if horiz == 0:
        direction = 'E' if dx > 0 else 'W'
        seg1 = helpers.LineSeg((x1, y1), direction, abs(dx))

        direction = 'S' if dy > 0 else 'N'
        seg2 = helpers.LineSeg((x2, y1), direction, abs(dy))

    else:
        direction = 'S' if dy > 0 else 'N'
        seg2 = helpers.LineSeg((x1, y1), direction, abs(dy))

        direction = 'E' if dx > 0 else 'W'
        seg1 = helpers.LineSeg((x1, y2), direction, abs(dx))

    return [seg1, seg2]


#--------------------------------------------------------------------
# TODO: add padding param to the overlaps_with
def rdg_simple_v1(floor, player, depth=1, num_rooms=5):
    rooms = [ ]
    lines = [ ]

    rect = random_rect()
    rect.center = (dungeon.MAP_WIDTH//2, dungeon.MAP_HEIGHT//2)
    rooms.append(rect)
    num_rooms -= 1

    for i in range(0, num_rooms):

        retries = 20
        while (retries > 0):
            rect2 = random_rect()
            is_good = True
            for r in rooms:
                if rect2.overlaps_with(r):
                    is_good = False

            if is_good:
                rooms.append(rect2)
                retries = 0
            else:
                retries -= 1

    # take the first room and connect it to all the rest
    origin_room = rooms[0]
    unconnected = [ ]
    for r in rooms[1:]:
        seg_list = make_line_segs(origin_room.center, r.center)
        for l in seg_list:
            is_good = True
            for r2 in rooms:
                if l.overlaps_with_edge(r2):
                    is_good = False
                    unconnected.append(r2)
            if is_good:
                lines.append(l)


    #TODO: IDEA!  check if line goes through a corner of a rect

    #TODO: IDEA! connect each room only to the closest one


    #take the rects and lines and actually make the rooms and corridors
    for r in rooms:
        floor.make_room(r.tl[0], r.tl[1], r.width, r.height)

    for l in lines:
        floor.make_tunnel_from_seg(l)

    #choose one of the rooms to start in
    idx = random.randint(0, len(rooms)-1)
    x, y = rooms[idx].center
    player.set_pos(x, y)
    floor.tiles[x][y].set_type("stairs_up")
    rooms.remove( rooms[idx] )

    #choose one of the rooms for down stairs
    idx = random.randint(0, len(rooms)-1)
    x, y = rooms[idx].center
    floor.tiles[x][y].set_type("stairs_down")






#--------------------------------------------------------------------
def make_random_dungeon3(floor, player):
    rooms = [ ]
    lines = [ ]

    rect = random_rect()
    rect.center = (dungeon.MAP_WIDTH//2, dungeon.MAP_HEIGHT//2)
    player.set_pos(rect.center[0], rect.center[1])
    floor.make_room(rect.tl[0], rect.tl[1], rect.width, rect.height)

    num_features = 3

    dig_dir = random_direction()
    dig_pt = rect.random_point_on_edge(dig_dir)

    while num_features > 0:

        retries = 10
        while retries > 0:
            length = random.randint(3, 8)
            seg = helpers.LineSeg(dig_pt, dig_dir, length)
            floor.make_tunnel_from_seg(seg)
            retries = 0
            #if seg.check_empty_space(floor):
            #    floor.make_tunnel_from_seg(seg)
            #    retries = 0
            #else:
            #    retries -= 1

        dig_pt = seg.get_endpoint()
        dig_dir = random_direction(opposite_direction(dig_dir))

        num_features -= 1

    #for r in rooms:
    #    floor.make_room(r.tl[0], r.tl[1], r.width, r.height)

    #for l in lines:
    #    floor.make_tunnel_from_seg(l)

    #x, y = rect.random_point_on_edge('E')
    #floor.tiles[x][y].set_type("door_closed")






#--------------------------------------------------------------------
def random_floor_rooms_only(floor, player):
    rooms = [ ]
    doors = [ ]
    num_rooms = 2

    #start with a random room in the center
    rect = random_rect()
    rect.center = (dungeon.MAP_WIDTH//2, dungeon.MAP_HEIGHT//2)
    player.set_pos(rect.center[0], rect.center[1])
    rooms.append(rect)

    dig_dir = random_direction()
    dig_pt = rect.random_point_on_edge(dig_dir)

    while num_rooms > 0:

        # build a random room in a random direction
        doors.append(dig_pt)

        new_rect = random_rect()
        if dig_dir == 'N':
            new_rect.br = ( dig_pt[0] + new_rect.width // 2, dig_pt[1] )
        elif dig_dir == 'S':
            new_rect.tl = ( dig_pt[0] - new_rect.width // 2, dig_pt[1] )
        elif dig_dir == 'E':
            new_rect.tl = ( dig_pt[0], dig_pt[1] - new_rect.height // 2)
        elif dig_dir == 'W':
            new_rect.br = ( dig_pt[0], dig_pt[1] + new_rect.height // 2)

        rooms.append(new_rect)
        #floor.make_room(new_rect.tl[0],
        #                new_rect.tl[1],
        #                new_rect.width,
        #                new_rect.height)
        num_rooms -= 1

        dig_dir = random_direction(opposite_direction(dig_dir))
        dig_pt = new_rect.random_point_on_edge(dig_dir)


    #for r in rooms:
    #    floor.make_room(r.tl[0], r.tl[1], r.width, r.height)

    for d in doors:
        floor.tiles[d[0]][d[1]].set_type("door_closed")



