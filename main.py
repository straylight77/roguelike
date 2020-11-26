#!/usr/bin/python
import curses
from world_lib import *  # repalce with explicit list

#-------------------------------- globals -------------------------------
player = Object('@')
floor = Floor()
done = False
msg = MessageQueue()



#--------------------------------- funcs ---------------------------------
def init():
    curses.curs_set(0)  # make cursor invisible

def draw_footer(screen, p):
    screen.addstr(22, 0, "MAP: ({}, {})".format(p.x, p.y))
    screen.addstr(23, 0, "SCR: ({}, {})".format(p.y+1, p.x))
    screen.vline(0, 80, '|', 25)
    screen.hline(24, 0, '-', 81)

def draw_dungeon(screen, m):
    # top line of the screen is the message line, so y+1
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            screen.addch(y+1, x, m.tiles[x][y].char)

def draw_object(screen, obj):
    # top line of the screen is the message line, so y+1
    screen.addch(obj.y+1, obj.x, obj.char)

def draw_messages(screen, mq):
    screen.addstr(0, 0, mq.get_string())
    mq.clear()

def handle_keys(c):
    if c in (ord('q'), 'q'):
        return True

    elif c == curses.KEY_UP:
        if floor.tiles[player.x][player.y-1].blocks_move:
            msg.add("Your way to the north is blocked!")
        else:
            player.move(0, -1)

    elif c == curses.KEY_DOWN:
        if floor.tiles[player.x][player.y+1].blocks_move:
            msg.add("Your way to the south is blocked!")
        else:
            player.move(0, 1)

    elif c == curses.KEY_LEFT:
        if floor.tiles[player.x-1][player.y].blocks_move:
            msg.add("Your way to the west is blocked!")
        else:
            player.move(-1, 0)

    elif c == curses.KEY_RIGHT:
        if floor.tiles[player.x+1][player.y].blocks_move:
            msg.add("Your way to the east is blocked!")
        else:
            player.move(1, 0)

    else:
        msg.add("Unknown command.  Type 'q' to exit.")

    return False




#--------------------------------- main() ---------------------------------
def main(stdscr):
    init()

    #make a simple dungeon map for testing
    floor.make_room(10, 5, 8, 5)
    floor.make_room(32, 8, 16, 6)
    floor.make_room(18, 6, 7, 3)
    floor.tiles[17][7].set_type('/', False, False)
    floor.tiles[18][7].set_type('.', False, False)

    floor.make_room(22, 8, 3, 5)
    floor.tiles[23][8].set_type('.', False, False)
    floor.tiles[24][8].set_type('|', True, True)

    floor.make_room(25, 10, 8, 3)
    floor.tiles[24][11].set_type('.', False, False)
    floor.tiles[25][11].set_type('.', False, False)
    floor.tiles[24][10].set_type('-', True, True)

    floor.tiles[32][10].set_type('|', True, True)
    floor.tiles[32][12].set_type('|', True, True)
    floor.tiles[32][11].set_type('+', False, False)

    player.set_pos(12, 7)
    msg.add("Welcome! Press 'q' to exit.")

    while True:

        stdscr.clear()

        draw_dungeon(stdscr, floor)
        draw_object(stdscr, player)
        draw_footer(stdscr, player)
        draw_messages(stdscr, msg)

        stdscr.refresh()
        cmd = stdscr.getch()
        if ( handle_keys(cmd) ):
            break



#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)

