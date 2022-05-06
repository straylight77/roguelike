#!/usr/bin/python
import curses
import random
import helpers
import dungeon
import items
import monsters
import sample
import display
import generators

# TODO:
# - convert player.x and player.y to player.pos (tuple)
#   - Floor.get_tile_at()
#   - Floor.get_monster_at()
#   - Floor.get_item_at()
#   - Player.set_pos
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
# X random levels, 5-room dungeon?
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
            player.xp += m2.xp
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
    global done, floor
    advance_time = True

    if c == 'X':
        advance_time = False
        done = True

    elif c in helpers.DIRECTION_KEY_LOOKUP.keys():
        dx, dy = helpers.DIRECTION_KEY_LOOKUP[c]
        do_player_move(dx, dy)

    elif c == '>':
        t = floor.get_tile_at(player.x, player.y)
        if t.type == 'stairs_down':
            msg.add("You decend the ancient stairs.")
            floor = dungeon.Floor( floor.depth+1 )
            player.depth += 1
            generators.default_random_floor(floor, player)
        else:
            msg.add("You don't see any stairs down here.")

    elif c == '<':
        t = floor.get_tile_at(player.x, player.y)
        if t.type == 'stairs_up':
            msg.add("Your way is magically blocked!")
        else:
            msg.add("You don't see any stairs up here.")

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




#--------------------------------- main() ---------------------------------
def main(stdscr):
    global done

    generators.default_random_floor(floor, player)

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
        if player.hp <= 0:
            advance_time = False
            score = player.xp + player.gold
            stdscr.move(0, 0)
            stdscr.clrtoeol()
            s = f"You have died.  Game over! (press a key)"
            stdscr.addstr(0, 0, s)
            stdscr.refresh()
            stdscr.getkey()
            done = True




#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)

    score = player.xp + player.gold
    s = f"Thanks for playing!  Final score: {score}"
    print(s)

