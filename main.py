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

    screen.addstr(22, 0, f"HP:{p.hp}({p.max_hp})")
    screen.addstr(23, 0, f"MP:{p.mp}({p.max_mp})")

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


def handle_combat(attacker, defender):
    attack_roll = random.randint(1, 20)
    damage = 3

    #"You attack the <thing> and (crtically) hit/miss."
    #"The <thing> attacks you and (crtically) hits/misses."

    # initial strings for 1st person or 2nd
    if attacker.name == "you":
        attack_str = f"You attack the {defender}"
        hit_str = "hit!"
        miss_str = "miss."
    else:
        attack_str = f"The {attacker} attacks you"
        hit_str = "hits!"
        miss_str = "misses."

    # check if the attack hits and if it's a crit
    hit = False
    crit_str = ""
    if attack_roll == 20:
        crit_str = "critically "
        hit = True
        damage *= 2
    elif attack_roll == 1:
        crit_str = "critically "
        hit = False
    elif (attack_roll + attacker.prof) >= defender.ac:
        hit = True

    # apply damage and finally add a message describing the outcome
    if hit:
        debug_str = f" [roll={attack_roll}, dmg={damage}]"
        msg.add(f"{attack_str}{debug_str} and {crit_str}{hit_str}")
        defender.hp -= damage
    else:
        debug_str = f" [roll={attack_roll}]"
        msg.add(f"{attack_str}{debug_str} and {crit_str}{miss_str}")

    # check if player is attacker and if the monster is killed
    if attacker.name == "you" and defender.hp <= 0:
        msg.add(f"You have defeated the {defender}!")
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


# only works in the positive-only quadrant?
def draw_line(scr, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    for x in range(x1, x2+1):
        y = round(y1 + dy * (x - x1) / dx)
        scr.addch(y+1, x, '*')



#--------------------------------- main() ---------------------------------
def main(stdscr):
    global done

    test_data.make_test_floor(floor, player)
    #test_data.make_test_floor2(floor, player)
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

        #draw_line(stdscr, 0, 0, player.x, player.y)

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
        if player.hp <= 0:
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

