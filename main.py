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
def draw_footer(screen, p):

    screen.addstr(22, 0, "HP:{}({})".format(p.hp["current"], p.hp["max"]))
    screen.addstr(23, 0, "MP:{}({})".format(p.mp["current"], p.mp["max"]))

    screen.addstr(22, 12, "St:18 Dx:12  Atk:{:+}".format(p.prof))
    screen.addstr(23, 12, "Co:14 Mi:8   Def:{}".format(p.ac))

    screen.addstr(22, 34, "Dmg:3-11(s)")
    #screen.addstr(23, 34, "Halu Conf Bles")

    screen.addstr(22, 58, "Au:{}".format(p.xp))
    screen.addstr(23, 58, "XP:{}/{}".format(p.level, p.xp))

    screen.addstr(22, 73, "D:1")
    screen.addstr(23, 73, "T:{}".format(p.moves))
    screen.addstr(21, 73, "({:2n},{:2n})".format(p.x, p.y))

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


def handle_combat(attacker, defender):
    attack_roll = random.randint(1, 20)
    damage = 3

    #"You attack the <thing> and (crtically) hit/miss."
    #"The <thing> attacks you and (crtically) hits/misses."

    # initial strings for 1st person or 2nd
    crit_str = ""
    if attacker.name == "you":
        attack_str = "You attack the {}".format(defender.name)
        hit_str = "hit!"
        miss_str = "miss."
    else:
        attack_str = "The {} attacks you".format(attacker.name)
        hit_str = "hits!"
        miss_str = "misses."

    # check if the attack hits and if it's a crit
    hit = False
    if attack_roll == 20:
        crit_str = "crtically "
        hit = True
        damage *= 2
    elif attack_roll == 1:
        crit_str = "crtically "
        hit = False
    elif (attack_roll + attacker.prof) >= defender.ac:
        hit = True

    # apply damage and finally add a message describing the outcome
    if hit:
        debug_str = " [roll={}, dmg={}]".format(attack_roll, damage)
        msg.add("{}{} and {}{}".format(attack_str, debug_str, crit_str, hit_str))
        defender.hp["current"] -= damage
    else:
        debug_str = " [roll={}]".format(attack_roll)
        msg.add("{}{} and {}{}".format(attack_str, debug_str, crit_str, miss_str))

    # check if player is attacker and if the monster is killed
    if attacker.name == "you" and defender.hp["current"] <= 0:
        msg.add("You have defeated the {}!".format(defender.name))
        player.xp += 50
        monsters.remove(defender)


def do_move(obj, dx, dy):
    t2 = floor.tiles[ obj.x+dx ][ obj.y+dy ]

    m2 = None
    for m in monsters:
        if m.x == obj.x+dx and m.y == obj.y+dy:
            m2 = m

    if m2 is not None:
        handle_combat(player, m2)

    elif t2.type == "door_closed":
        msg.add("You open the door.")
        t2.set_type("door_open")

    elif t2.blocks_move:
        msg.add("Your way in that direction is blocked.")

    else:
        obj.move(dx, dy)


def do_monster_turn(obj):
    dist = obj.distance_from(player.x, player.y)
    if dist > 5:
        return

    d = obj.direction_to(player.x, player.y)
    t2 = floor.tiles[ obj.x+d[0] ][ obj.y+d[1] ]
    m2 = None
    for m in monsters:
        if m.x == obj.x+d[0] and m.y == obj.y+d[1]:
            m2 = m

    if player.x == obj.x+d[0] and player.y == obj.y+d[1]:
        handle_combat(obj, player)
    elif not t2.blocks_move and m2 == None:
        obj.move(d[0], d[1])


def handle_keys(c, screen):
    global done
    advance_time = True

    if c == ord('q'):
        done = True
        advance_time = False

    elif c in (ord('k'), curses.KEY_UP):
        do_move(player, 0, -1)

    elif c in (ord('j'), curses.KEY_DOWN):
        do_move(player, 0, 1)

    elif c in (ord('h'), curses.KEY_LEFT):
        do_move(player, -1, 0)

    elif c in (ord('l'), curses.KEY_RIGHT):
        do_move(player, 1, 0)

    elif c == ord('y'): do_move(player, -1, -1)
    elif c == ord('u'): do_move(player, 1, -1)
    elif c == ord('b'): do_move(player, -1, 1)
    elif c == ord('n'): do_move(player, 1, 1)
    elif c == ord('.'): msg.add("You rest for a moment.")

    elif c == ord('M'):
        advance_time = False
        screen.move(0, 0)
        screen.clrtoeol()
        screen.addstr(0, 0, "LAST 20 MESSAGES:")
        y = 1
        for m in msg.history[-20:]:
            screen.addstr(y, 0, m)
            y += 1
        screen.addstr(y, 0, "(done)")
        screen.refresh()
        screen.getch()

    else:
        advance_time = False
        msg.add("Unknown command.  Type 'q' to exit.")

    return advance_time



#--------------------------------- main() ---------------------------------
def main(stdscr):
    global done

    test_data.make_test_floor2(floor, player)
    monsters.append( Monster("rat", 15, 8) )
    monsters.append( Monster("skeleton", 43, 10) )

    msg.add("Welcome! Press 'q' to exit.")

    while not done:

        stdscr.move(0,0)
        stdscr.clrtoeol()

        draw_dungeon(stdscr, floor)
        draw_all_objects(stdscr, monsters)
        draw_object(stdscr, player)
        draw_footer(stdscr, player)
        draw_messages(stdscr, msg)
        stdscr.move(player.y+1, player.x)

        stdscr.refresh()
        cmd = stdscr.getch()
        if ( handle_keys(cmd, stdscr) ):
            player.moves += 1

        # move monsters
        for m in monsters:
            do_monster_turn(m)

        # other updates

        # check for player death
        if player.hp["current"] <= 0:
            advance_time = False
            stdscr.move(0, 0)
            stdscr.clrtoeol()
            stdscr.addstr(0, 0, "You have died.  Game over! (press a key)")
            stdscr.refresh()
            stdscr.getch()
            done = True




#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)

