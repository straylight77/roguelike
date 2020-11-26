#!/usr/bin/python
import curses
from world import *  # repalce with explicit list
import test_data

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
    #screen.vline(0, 80, '|', 25)
    #screen.hline(24, 0, '-', 81)

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

def handle_keys(c, screen):
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

    elif c in (ord('M'), 'M'):
        y = 0
        screen.move(0, 0)
        screen.clrtoeol()
        for m in msg.history[-20:]:
            screen.addstr(y, 0, m)
            y += 1
        screen.addstr(y, 0, "-press any key-")
        screen.refresh()
        screen.getch()


    else:
        msg.add("Unknown command.  Type 'q' to exit.")

    return False



#--------------------------------- main() ---------------------------------
def main(stdscr):
    init()
    test_data.make_test_floor2(floor, player)
    msg.add("Welcome! Press 'q' to exit.")

    while True:

        stdscr.clear()

        draw_dungeon(stdscr, floor)
        draw_object(stdscr, player)
        draw_footer(stdscr, player)
        draw_messages(stdscr, msg)

        stdscr.refresh()
        cmd = stdscr.getch()
        if ( handle_keys(cmd, stdscr) ):
            break



#-------------------------------------------------------------
if __name__ == "__main__":
    curses.wrapper(main)






