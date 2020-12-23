import dungeon
import monsters
import random
import helpers

def default_random_floor(floor, player):
    rdg_simple_v1(floor, player, player.depth, 8)
    #rdg_simple_v2(floor, player, 6)
    #rdg_simple_v3(floor, player, player.depth, 8)


def random_direction(ignore=None):
    dirs = ["N", "E", "W", "S"]
    if ignore is not None:
        dirs.remove(ignore)
    i = random.randint(0, len(dirs)-1)
    return dirs[i]


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

def get_random_room(existing_rooms = [ ], retries = 20):
    new_room = None
    while (retries > 0):
        rect = random_rect()
        is_good = True
        for r in existing_rooms:
            if rect.overlaps_with(r, 1):
                is_good = False

        if is_good:
            new_room = rect
            retries = 0
        else:
            retries -= 1

    return new_room



def generate_random_rooms(num_rooms):
    rooms = [ ]

    rect = random_rect()
    rect.center = (dungeon.MAP_WIDTH//2, dungeon.MAP_HEIGHT//2)
    rooms.append(rect)
    num_rooms -= 1

    for i in range(0, num_rooms):
        new_room = get_random_room(rooms)
        if new_room is not None:
            rooms.append(new_room)

    return rooms


def random_item_from_list(l):
    i = random.randint(0, len(l)-1)
    return l[i]


def check_line_segs_overlap(segs, rects):
    is_good = True
    for l in segs:
        for r in rects:
            if l.overlaps_with_edge(r):
                is_good = False

    return is_good


def random_monster_list(rect):
    mon_list = [ ]
    mon_name_list = list(monsters.MONSTERS)
    qty = random.randint(1, 2)
    while qty > 0:
        x = random.randint(rect.left+1, rect.right-1)
        y = random.randint(rect.top+1, rect.bottom-1)
        mon_name = random_item_from_list(mon_name_list)
        mon_list.append( monsters.Monster(mon_name, x, y) )
        qty -= 1
    return mon_list


def populate_rooms(floor, player, rect_list, depth = 1):
    rooms = rect_list.copy()

    #choose one of the rooms to start in
    r = random_item_from_list(rooms)
    x, y = r.center
    player.set_pos(x, y)
    floor.get_tile(r.center).set_type("stairs_up")
    rooms.remove(r)

    #choose one of the rooms for down stairs
    r = random_item_from_list(rooms)
    floor.get_tile(r.center).set_type("stairs_down")

    for r in rooms:
        mon_list = random_monster_list(r)
        for m in mon_list:
            floor.add_monster(m)



#--------------------------------------------------------------------
def rdg_simple_v1(floor, player, depth=1, num_rooms=5):
    rooms = generate_random_rooms(num_rooms)
    lines = [ ]

    # take the first room and connect it to all the rest
    origin = rooms[0]
    unconnected = 0
    for dest in rooms[1:]:
        seg_list = make_line_segs(origin.center, dest.center)
        if check_line_segs_overlap(seg_list, rooms):
            lines.extend(seg_list)
        else:
            unconnected += 1
            rooms.remove(dest)

    for i in range(0, unconnected):
        retries = 10
        while retries > 0:
            new_room = get_random_room(rooms)
            if new_room is None:
                retries -= 1
                break
            dest = new_room.closest_neighbour(rooms)
            seg_list = make_line_segs(new_room.center, dest.center)
            if check_line_segs_overlap(lines + seg_list, rooms + [new_room]):
                rooms.append(new_room)
                lines.extend(seg_list)
                retries = 0
            else:
                retries -= 1

    #take the rects and lines and actually make the rooms and corridors
    for r in rooms:
        floor.make_room(r.tl[0], r.tl[1], r.width, r.height)

    for l in lines:
        floor.make_tunnel_from_seg(l)

    populate_rooms(floor, player, rooms, depth)




#--------------------------------------------------------------------
def rdg_simple_v2(floor, player, num_rooms=5):
    rooms = generate_random_rooms(num_rooms)
    lines = [ ]

    for origin in rooms:
        dest = origin.closest_neighbour(rooms)
        segs = make_line_segs(origin.center, dest.center)
        lines.extend(segs)

    #take the rects and lines and actually make the rooms and corridors
    for r in rooms:
        floor.make_room(r.tl[0], r.tl[1], r.width, r.height)

    for l in lines:
        #floor.make_tunnel_from_seg(l, True)
        floor.make_tunnel_from_seg(l, False)


#--------------------------------------------------------------------
def rdg_simple_v3(floor, player, depth=1, num_rooms=5):
    rooms = [ ]
    lines = [ ]

    new_room = get_random_room()
    rooms.append(new_room)
    num_rooms -= 1

    for i in range(1, num_rooms):
        retries = 10
        while retries > 0:
            new_room = get_random_room(rooms)
            if new_room is None:
                retries -= 1
                break
            dest = new_room.closest_neighbour(rooms)
            seg_list = make_line_segs(new_room.center, dest.center)
            if check_line_segs_overlap(seg_list, rooms):
                rooms.append(new_room)
                lines.extend(seg_list)
                retries = 0
            else:
                retries -= 1

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



