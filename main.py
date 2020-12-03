#!/usr/bin/python
import curses
import random
from world import *  # repalce with explicit list
import sample


# TODO:
# - convert player.x and player.y to player.pos (tuple)
# - new Display class for all curses and draw_* stuff?
# - items and inventory
#   - gold (pickup, drop)
#   - healing potions (quaff, use/activate)
#   - weapons (wield)
#   - armor (wear, take off)
# - shooting and throwing
# - field of view (visible, explored)
# - colors!

#-------------------------------- globals -------------------------------
player = Player()
floor = Floor()
done = False
msg = MessageQueue()

DIRECTION_KEY_LOOKUP = {
    curses.KEY_UP:    ( 0, -1),
    curses.KEY_DOWN:  ( 0,  1),
    curses.KEY_LEFT:  (-1,  0),
    curses.KEY_RIGHT: ( 1,  0),
    ord('k'): ( 0, -1),
    ord('j'): ( 0,  1),
    ord('h'): (-1,  0),
    ord('l'): ( 1,  0),
    ord('y'): (-1, -1),
    ord('u'): ( 1, -1),
    ord('b'): (-1,  1),
    ord('n'): ( 1,  1),
}


#--------------------------------- funcs ---------------------------------
def draw_footer(screen, p):

    screen.addstr(22, 0, f"HP:{p.hp}({p.max_hp}) ")
    screen.addstr(23, 0, f"MP:{p.mp}({p.max_mp}) ")

    screen.addstr(22, 12, f"St:18 Dx:12  Atk:{p.prof:+}")
    screen.addstr(23, 12, f"Co:14 Mi:8   Def:{p.ac}")

    screen.addstr(22, 34, f"Dmg:3-11(s)")
    #screen.addstr(23, 34, "Halu Conf Bles")

    screen.addstr(22, 58, f"Au:{p.gold}")
    screen.addstr(23, 58, f"XP:{p.level}/{p.xp}")

    screen.addstr(22, 73, f"D:{p.depth}")
    screen.addstr(23, 73, f"T:{p.moves}")
    screen.addstr(21, 73, f"({p.x},{p.y})")

    #screen.vline(0, 80, '|', 24)
    #screen.hline(24, 0, '-', 80)

def draw_dungeon(screen, m):
    # top line of the screen is the message line, so y+1
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            screen.addch(y+1, x, m.tiles[x][y].char)

def draw_object(screen, obj):
    screen.addch(obj.y+1, obj.x, obj.char)

def draw_all_objects(screen, objects):
    # top line of the screen is the message line, so y+1
    for obj in objects:
        draw_object(screen, obj)

def draw_messages(screen, mq):
    screen.addstr(0, 0, str(mq))
    mq.clear()

def draw_message_history(screen, mq):
    screen.move(0, 0)
    screen.clrtoeol()
    screen.addstr(0, 0, "LAST 20 MESSAGES:")
    y = 1
    for m in mq.history[-20:]:
        screen.addstr(y, 0, m)
        y += 1
    screen.addstr(y, 0, "(done)")
    screen.refresh()
    screen.getch()


def do_open(floor, x, y):
    t = floor.get_tile_at(x, y)
    if t.type == 'door_closed':
        ret_msg = "You open the door."
        t.set_type('door_open')
    else:
        ret_msg = "There's no door to open there."
    return ret_msg

def do_close(floor, x, y):
    t = floor.get_tile_at(x, y)
    if t.type == 'door_open':
        ret_msg = "You close the door."
        t.set_type('door_closed')
    else:
        ret_msg = "There's no door to close there."
    return ret_msg


def do_player_move(dx, dy):
    t2 = floor.get_tile_at( player.x+dx, player.y+dy )
    m2 = floor.get_monster_at(player.x+dx, player.y+dy)

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


def prompt_direction(screen, cursor_pos = None, message = "Which direction?"):
    screen.move(0, 0)
    screen.clrtoeol()
    screen.addstr(0, 0, message)
    if cursor_pos is not None:
        screen.move(cursor_pos[1]+1, cursor_pos[0])

    c = screen.getch()
    try:
        dir = DIRECTION_KEY_LOOKUP[c]
    except KeyError:
        dir = (0, 0)
    return dir


def handle_keys(c, screen):
    global done
    advance_time = True

    if c == ord('q'):
        advance_time = False
        done = True

    elif c in DIRECTION_KEY_LOOKUP.keys():
        dx, dy = DIRECTION_KEY_LOOKUP[c]
        do_player_move(dx, dy)

    elif c == ord('.'):
        msg.add("You rest for a moment.")

    elif c == ord('o'):
        dx, dy = prompt_direction(screen, (player.x, player.y))
        msg.add( do_open(floor, player.x+dx, player.y+dy) )

    elif c == ord('c'):
        dx, dy = prompt_direction(screen, (player.x, player.y))
        msg.add( do_close(floor, player.x+dx, player.y+dy) )

    elif c == ord('M'):
        advance_time = False
        draw_message_history(screen, msg)

    else:
        advance_time = False
        msg.add("Unknown command.  Type 'q' to exit.")

    return advance_time



#--------------------------------- main() ---------------------------------
def main(stdscr):
    global done

    #sample.make_test_floor(floor, player)
    sample.make_test_floor2(floor, player)
    floor.add_monster( Monster("rat", 15, 8) )
    floor.add_monster( Monster("skeleton", 43, 10) )

    msg.add("Welcome! Press 'q' to exit.")

    while not done:

        stdscr.move(0,0)
        stdscr.clrtoeol()

        draw_dungeon(stdscr, floor)
        draw_all_objects(stdscr, floor.monsters)
        draw_object(stdscr, player)
        draw_footer(stdscr, player)
        draw_messages(stdscr, msg)

        stdscr.move(player.y+1, player.x)

        stdscr.refresh()
        cmd = stdscr.getch()
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
        #    stdscr.getch()
        #    done = True




#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)

