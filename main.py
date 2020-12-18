#!/usr/bin/python
import curses
import random
import helpers
import dungeon
import items
import monsters
import sample
import display

# TODO:
# - convert player.x and player.y to player.pos (tuple)
# X new Display class for all curses and draw_* stuff?
# X items and inventory
#   X gold (pickup, drop)
#   X healing potions (quaff)
#   - scrolls (read)
#   - weapons (wield)
#   - armor (Wear, take off)
# - shooting and throwing
# - field of view (visible, explored)
# - colors!
# - random levels, 5-room dungeon?
# - levelling up
# - save game, high score list, player name, death screen

#-------------------------------- globals -------------------------------
player = monsters.Player()
floor = dungeon.Floor()
done = False
msg = helpers.MessageQueue()
disp = display.Display()


def do_open(floor, x, y):
    t = floor.get_tile_at(x, y)
    if t.type == 'door_closed':
        ret_msg = "You open the door."
        t.set_type('door_open')
    else:
        ret_msg = f"There's no door to open that direction."
    return ret_msg

def do_close(floor, x, y):
    t = floor.get_tile_at(x, y)
    if t.type == 'door_open':
        ret_msg = "You close the door."
        t.set_type('door_closed')
    else:
        ret_msg = f"There's no door to close that direction."
    return ret_msg


def do_player_move(dx, dy):
    t2 = floor.get_tile_at( player.x+dx, player.y+dy )
    m2 = floor.get_monster_at(player.x+dx, player.y+dy)
    i2 = floor.get_item_at(player.x+dx, player.y+dy)

    if m2 is not None:
        combat_msg = player.do_attack(m2)
        msg.add(combat_msg)
        if m2.hp <= 0:
            msg.add(f"You have defeated the {m2}!")
            player.xp += 50
            floor.remove_monster(m2)

    elif t2.type == "door_closed":
        msg.add("You open the door.")
        t2.set_type("door_open")

    elif t2.blocks_move:
        msg.add("Your way in that direction is blocked.")

    else:
        player.move(dx, dy)

    #post-move checks
    if i2 is not None:
        msg.add(f"You see {i2} here.")
        #player.pickup(i2)
        #floor.items.remove(i2)
        #msg.add(f"You pick up {i2}.")




def handle_keys(c, screen):
    global done
    advance_time = True

    if c == 'X':
        advance_time = False
        done = True

    elif c in helpers.DIRECTION_KEY_LOOKUP.keys():
        dx, dy = helpers.DIRECTION_KEY_LOOKUP[c]
        do_player_move(dx, dy)

    elif c == '.':
        msg.add("You rest for a moment.")

    elif c == 'o':
        dx, dy = disp.prompt_direction(screen, (player.x, player.y))
        msg.add( do_open(floor, player.x+dx, player.y+dy) )

    elif c == 'c':
        dx, dy = disp.prompt_direction(screen, (player.x, player.y))
        msg.add( do_close(floor, player.x+dx, player.y+dy) )

    elif c == 'q':
        item = disp.prompt_inventory(screen, player, "Quaff which item?")
        if item is not None:
            m = item.quaff(player)
            msg.add(m)
        else:
            msg.add("Nevermind.")

    elif c == ',':
        item = floor.get_item_at(player.x, player.y)
        player.pickup(item)
        floor.items.remove(item)
        msg.add(f"You pick up {item}.")

    elif c == 'd':
        item = disp.prompt_inventory(screen, player, "Drop which item?")
        if item is not None:
            item.set_pos( player.x, player.y )
            floor.add_item(item)
            player.inventory.remove(item)
            msg.add(f"You drop the {item}.")
        else:
            msg.add("Nevermind.")

    elif c == 'i':
        advance_time = False
        disp.draw_inventory(screen, player)

    elif c == 'M':
        advance_time = False
        disp.draw_message_history(screen, msg)

    else:
        advance_time = False
        msg.add(f"Unknown command '{c}'.  Type 'q' to exit.")

    return advance_time



def empty_space(floor, start_x, start_y, dx, dy):
    for x in range(start_x, start_x+dx):
        for y in range(start_y, start_y+dy):
            t = floor.get_tile_at(x, y)
            if t.type != 'empty':
                return False
    return True


def make_random_dungeon(floor, player):
    num_rooms = random.randint(5, 8)
    max_tries = 100
    keep_going = True

    while(keep_going):
        dx = random.randint(6, 12)
        dy = random.randint(5, 8)

        x = random.randint(0, dungeon.MAP_WIDTH-dx)
        y = random.randint(0, dungeon.MAP_HEIGHT-dy)

        if empty_space(floor, x, y, dx, dy):
            floor.make_room(x, y, dx, dy)
            num_rooms -= 1

        max_tries -= 1
        if (max_tries <= 0 or num_rooms <= 0):
            player.set_pos(x+(dx//2), y+(dy//2))
            keep_going = False


def make_random_dungeon2(floor, player):
    rooms = [ ]
    num_rooms = 5

    rect = helpers.Rect(
        width = random.randint(6,10),
        height = random.randint(4,8)
    )
    rect.center = (dungeon.MAP_WIDTH//2, dungeon.MAP_HEIGHT//2)
    rooms.append(rect)

    for i in range(0, num_rooms):
        dx = random.randint(6, 12)
        dy = random.randint(5, 8)

        x = random.randint(0, dungeon.MAP_WIDTH-dx)
        y = random.randint(0, dungeon.MAP_HEIGHT-dy)

        rect2 = helpers.Rect( (x,y), dx, dy )
        #rect2.br = (dungeon.MAP_WIDTH//2+4, rect.top+1)
        rooms.append(rect2)

    for r in rooms:
        floor.make_room(r.tl[0], r.tl[1], r.width, r.height)

    for r in rooms:
        pos = r.random_point_on_edge("top")
        floor.get_tile_at(pos[0], pos[1]).set_type('door_closed')

    player.set_pos(dungeon.MAP_WIDTH//2, dungeon.MAP_HEIGHT//2)


#--------------------------------- main() ---------------------------------
def main(stdscr):
    global done


    #sample.make_test_floor(floor, player)
    #sample.make_test_floor2(floor, player)
    #make_random_dungeon(floor, player)
    make_random_dungeon2(floor, player)

    msg.add("Welcome! Type 'X' to exit.")
    player.pickup( items.Item("healing potion") )

    while not done:

        stdscr.move(0,0)
        stdscr.clrtoeol()

        disp.draw_dungeon(stdscr, floor)
        disp.draw_all_objects(stdscr, floor.items)
        disp.draw_all_objects(stdscr, floor.monsters)
        disp.draw_object(stdscr, player)
        disp.draw_footer(stdscr, player)
        disp.draw_messages(stdscr, msg)

        stdscr.move(player.y+1, player.x)

        stdscr.refresh()
        cmd = stdscr.getkey()
        if ( handle_keys(cmd, stdscr) ):
            player.moves += 1

        # move monsters
        for m in floor.monsters:
            update_msg = m.update(player, floor)
            msg.add(update_msg)

        # other updates

        # check for player death
        #if player.hp <= 0:
        #    advance_time = False
        #    stdscr.move(0, 0)
        #    stdscr.clrtoeol()
        #    stdscr.addstr(0, 0, "You have died.  Game over! (press a key)")
        #    stdscr.refresh()
        #    stdscr.getkey()
        #    done = True




#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)

