import dungeon
import helpers


class Display():

    def __init__(self):
        pass


    #--------------------------------- funcs ---------------------------------
    def draw_footer(self, screen, p):

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

    def draw_dungeon(self, screen, m):
        # top line of the screen is the message line, so y+1
        for x in range(0, dungeon.MAP_WIDTH):
            for y in range(0, dungeon.MAP_HEIGHT):
                screen.addch(y+1, x, m.tiles[x][y].char)

    def draw_object(self, screen, obj):
        screen.addch(obj.y+1, obj.x, obj.char)

    def draw_all_objects(self, screen, objects):
        # top line of the screen is the message line, so y+1
        for obj in objects:
            self.draw_object(screen, obj)

    def draw_messages(self, screen, mq):
        screen.addstr(0, 0, str(mq))
        mq.clear()

    def draw_message_history(self, screen, mq):
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


    def draw_inventory(self, screen, ply):
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


    def prompt_direction(self, screen, cursor_pos = None, message = "Which direction?"):
        screen.move(0, 0)
        screen.clrtoeol()
        screen.addstr(0, 0, message)
        if cursor_pos is not None:
            screen.move(cursor_pos[1]+1, cursor_pos[0])

        c = screen.getkey()
        try:
            dir = helpers.DIRECTION_KEY_LOOKUP[c]
        except KeyError:
            dir = (0, 0)
        return dir


    def prompt_inventory(self, screen, plyr, message = "Which item?", cat = None):
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



