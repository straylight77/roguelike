#!/usr/bin/python
import curses
import random
from world import *  # repalce with explicit list
import test_data

#-------------------------------- globals -------------------------------
player = Player()
floor = Floor()
done = False
msg = MessageQueue()
monsters = [ ]

#--------------------------------- funcs ---------------------------------
def init():
    curses.curs_set(0)  # make cursor invisible

def draw_footer(screen, p):

    screen.addstr(22, 0, "HP:{}({})".format(p.hp["current"], p.hp["max"]))
    screen.addstr(23, 0, "MP:{}({})".format(p.mp["current"], p.mp["max"]))

    screen.addstr(22, 12, "St:18 Dx:12  Atk:{:+}".format(p.prof))
    screen.addstr(23, 12, "Co:14 Mg:8   Def:{}".format(p.ac))

    screen.addstr(22, 34, "Dmg:3-11(s)")
    #screen.addstr(23, 34, "Halu Conf Bles")

    screen.addstr(22, 58, "Au:{}".format(p.xp))
    screen.addstr(23, 58, "XP:{}/{}".format(p.level, p.xp))

    screen.addstr(22, 73, "D:1")
    screen.addstr(23, 73, "T:{}".format(p.moves))
    #screen.addstr(21, 73, "({:2n},{:2n})".format(p.x, p.y))

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
        #screen.addch(obj.y+1, obj.x, obj.char)

def draw_messages(screen, mq):
    msg_str = mq.get_string()
    screen.addstr(0, 0, msg_str)
    mq.clear()


def handle_player_attack(defender):
    attack_roll = random.randint(1, 20)

    hit = False
    if attack_roll == 20:
        msg.add("Critical hit!")
        hit = True
        damage = 6
    elif attack_roll == 1:
        msg.add("Critical miss!")
        hit = False
    elif (attack_roll + player.prof) >= defender.ac:
        hit = True
        damage = 3
    else:
        msg.add("You miss the {} (roll={}).".format(defender.name, attack_roll))

    if hit:
        msg.add("You hit the {} (roll={}, dmg={}).".format(defender.name,
                                                           attack_roll,
                                                           damage)
               )
        defender.hp["current"] -= damage

    if defender.hp["current"] <= 0:
        msg.add("You have defeated the {}!".format(defender.name))
        monsters.remove(defender)





def do_move(obj, dx, dy):
    t2 = floor.tiles[ obj.x+dx ][ obj.y+dy ]

    m2 = None
    for m in monsters:
        if m.x == obj.x+dx and m.y == obj.y+dy:
            m2 = m

    if m2 is not None:
        #msg.add("There's a {} there.".format(m2.name))
        handle_player_attack(m2)

    elif t2.type == "door_closed":
        msg.add("You open the door.")
        t2.set_type("door_open")

    elif t2.blocks_move:
        msg.add("Your way in that direction is blocked.")

    else:
        obj.move(dx, dy)


def handle_keys(c, screen):
    global done
    advance_time = True

    if c in (ord('q'), 'q'):
        done = True
        advance_time = False

    elif c == curses.KEY_UP:
        do_move(player, 0, -1)

    elif c == curses.KEY_DOWN:
        do_move(player, 0, 1)

    elif c == curses.KEY_LEFT:
        do_move(player, -1, 0)

    elif c == curses.KEY_RIGHT:
        do_move(player, 1, 0)

    elif c in (ord('M'), 'M'):
        advance_time = False
        screen.move(0, 0)
        screen.clrtoeol()
        screen.addstr(0, 0, "LAST 20 MESSAGES:")
        y = 1
        for m in msg.history[-20:]:
            screen.addstr(y, 0, m)
            y += 1
        screen.addstr(y, 0, "-done-")
        screen.refresh()
        screen.getch()

    else:
        advance_time = False
        msg.add("Unknown command.  Type 'q' to exit.")

    return advance_time



#--------------------------------- main() ---------------------------------
def main(stdscr):
    init()
    test_data.make_test_floor2(floor, player)

    monsters.append( Monster("skeleton", 'k', 15, 8) )


    msg.add("Welcome! Press 'q' to exit.")

    while not done:

        stdscr.clear()

        draw_dungeon(stdscr, floor)
        draw_all_objects(stdscr, monsters)
        draw_object(stdscr, player)
        draw_footer(stdscr, player)
        draw_messages(stdscr, msg)

        stdscr.refresh()
        cmd = stdscr.getch()
        if ( handle_keys(cmd, stdscr) ):
            player.moves += 1

        # move monsters

        # other updates



#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)

