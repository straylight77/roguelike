#!/usr/bin/python
import curses
import random
import helpers
import dungeon
import items
import monsters
import sample


# TODO:
# - convert player.x and player.y to player.pos (tuple)
# - new Display class for all curses and draw_* stuff?
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

DIRECTION_KEY_LOOKUP = {
    'KEY_UP':    ( 0, -1),
    'KEY_DOWN':  ( 0,  1),
    'KEY_LEFT':  (-1,  0),
    'KEY_RIGHT': ( 1,  0),
    'KEY_PPAGE': ( 1, -1),
    'KEY_NPAGE': (-1,  1),
    'KEY_HOME':  (-1, -1),
    'KEY_END':   ( 1,  1),
    'k': ( 0, -1),
    'j': ( 0,  1),
    'h': (-1,  0),
    'l': ( 1,  0),
    'y': (-1, -1),
    'u': ( 1, -1),
    'b': (-1,  1),
    'n': ( 1,  1),
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
    for x in range(0, dungeon.MAP_WIDTH):
        for y in range(0, dungeon.MAP_HEIGHT):
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
    screen.getkey()


def draw_inventory(screen, ply):
    screen.move(0, 0)
    screen.clrtoeol()
    screen.addstr(0, 0, "INVENTORY:")
    y = 1
    for i in ply.inventory:
        ch = chr( ord('a')+y-1 )
        screen.addstr(y, 0, f"{ch} - {i.char} {i}")
        y += 1
    screen.addstr(y, 0, "(done)")
    screen.refresh()
    screen.getkey()


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




def prompt_direction(screen, cursor_pos = None, message = "Which direction?"):
    screen.move(0, 0)
    screen.clrtoeol()
    screen.addstr(0, 0, message)
    if cursor_pos is not None:
        screen.move(cursor_pos[1]+1, cursor_pos[0])

    c = screen.getkey()
    try:
        dir = DIRECTION_KEY_LOOKUP[c]
    except KeyError:
        dir = (0, 0)
    return dir


def prompt_inventory(screen, plyr, message = "Which item?", cat = None):
    screen.move(0, 0)
    screen.clrtoeol()
    y = 1
    for i in plyr.inventory:
        ch = chr( ord('a')+y-1 )
        screen.addstr(y, 0, f"{ch} - {i.char} {i}")
        y += 1
    screen.addstr(0, 0, message)
    screen.refresh()
    c = screen.getkey()
    idx = ord(c)-ord('a')
    if idx >= 0 and idx < len(plyr.inventory):
        item = plyr.inventory[idx]
    else:
        item = None
    return item


def handle_keys(c, screen):
    global done
    advance_time = True

    if c == 'X':
        advance_time = False
        done = True

    elif c in DIRECTION_KEY_LOOKUP.keys():
        dx, dy = DIRECTION_KEY_LOOKUP[c]
        do_player_move(dx, dy)

    elif c == '.':
        msg.add("You rest for a moment.")

    elif c == 'o':
        dx, dy = prompt_direction(screen, (player.x, player.y))
        msg.add( do_open(floor, player.x+dx, player.y+dy) )

    elif c == 'c':
        dx, dy = prompt_direction(screen, (player.x, player.y))
        msg.add( do_close(floor, player.x+dx, player.y+dy) )

    elif c == 'q':
        item = prompt_inventory(screen, player, "Quaff which item?")
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
        item = prompt_inventory(screen, player, "Drop which item?")
        if item is not None:
            item.set_pos( player.x, player.y )
            floor.add_item(item)
            player.inventory.remove(item)
            msg.add(f"You drop the {item}.")
        else:
            msg.add("Nevermind.")

    elif c == 'i':
        advance_time = False
        draw_inventory(screen, player)

    elif c == 'M':
        advance_time = False
        draw_message_history(screen, msg)

    else:
        advance_time = False
        msg.add(f"Unknown command '{c}'.  Type 'q' to exit.")

    return advance_time



#--------------------------------- main() ---------------------------------
def main(stdscr):
    global done

    #sample.make_test_floor(floor, player)
    sample.make_test_floor2(floor, player)
    #floor.add_monster( monsters.Monster("rat", 15, 8) )
    floor.add_monster( monsters.Monster("skeleton", 43, 10) )
    floor.add_item( items.Item("gold", 45, 12) )
    floor.add_item( items.Item("healing potion", 15, 8) )

    msg.add("Welcome! Type 'X' to exit.")
    player.pickup( items.Item("healing potion") )

    while not done:

        stdscr.move(0,0)
        stdscr.clrtoeol()

        draw_dungeon(stdscr, floor)
        draw_all_objects(stdscr, floor.monsters)
        draw_all_objects(stdscr, floor.items)
        draw_object(stdscr, player)
        draw_footer(stdscr, player)
        draw_messages(stdscr, msg)

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

