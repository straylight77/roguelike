import textwrap
import random

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




#------------------------- helper functions ---------------------------------
def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points




#-------------------------------------------------------------------------
class GameObject():

    def __init__(self, char, x=0, y=0, color=0):
        self.char = char
        self.color = color
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance_from(self, dest_x, dest_y):
        dx = dest_x - self.x
        dy = dest_y - self.y
        distance = ( dx**2 + dy**2 ) ** 0.5
        return distance

    def direction_to(self, dest_x, dest_y):
        dx = 0
        if dest_x < self.x: dx = -1
        if dest_x > self.x: dx = 1

        dy = 0
        if dest_y < self.y: dy = -1
        if dest_y > self.y: dy = 1

        return (dx, dy)


#-------------------------------------------------------------------------
class MessageQueue():
    def __init__(self, wrap_width=80):
        self.messages = [ ]
        self.history = [ ]
        self.wrap_width = wrap_width
        self.wrap = textwrap.TextWrapper(wrap_width)

    def add(self, m):
        if m is None:
            return
        self.messages.append(m)
        self.history.append(m)

    def extend(self, m_list):
        self.messages.extend(m_list)
        self.history.extend(m_list)

    def clear(self):
        self.messages.clear()

    def get_string(self):
        str = ""
        for s in self.messages:
            str += s + " "
        return self.wrap.fill(str)

    def __len__(self):
        return len(self.messages)

    def __str__(self):
        return self.get_string()

    def __iadd__(self, m):
        self.add(m)


#-------------------------------------------------------------------------
class Rect():

    def __init__(self, tl=(0,0), width=0, height=0):
        self._tl = tl
        self.width = width
        self.height = height

    def __str__(self):
        return f"{self.tl},{self.br}"

    def __repr__(self):
        return f"Rect:{self}"

    def get_br(self):
        return ( self._tl[0] + (self.width-1), self._tl[1] + (self.height-1) )

    def set_br(self, pos):
        self._tl = ( pos[0] - (self.width-1), pos[1] - (self.height-1) )

    def get_tl(self):
        return self._tl

    def set_tl(self, pos):
        self._tl = pos

    br = property(get_br, set_br)
    tl = property(get_tl, set_tl)

    def get_top(self):
        return self.tl[1]

    def get_bottom(self):
        return self.br[1]

    def get_left(self):
        return self.tl[0]

    def get_right(self):
        return self.br[0]

    top = property(get_top)
    bottom = property(get_bottom)
    left = property(get_left)
    right = property(get_right)

    def get_center(self):
        return (
            self._tl[0] + self.width // 2,
            self._tl[1] + self.height // 2
        )

    def set_center(self, pos):
        x = pos[0] - (self.width // 2)
        y = pos[1] - (self.height // 2)
        self.tl = (x, y)

    center = property(get_center, set_center)

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def get_corners(self, padding = 0):
        tl = (self.tl[0] - padding , self.tl[1] - padding)
        br = (self.br[0] + padding , self.br[1] + padding)
        tr = (self.right + padding , self.top - padding)
        bl = (self.left - padding  , self.bottom + padding)

        return [ tl, br, tr, bl ]


    def contains(self, pt):
        x, y = pt
        if (self.left <= x <= self.right) and (self.top <= y <= self.bottom):
            ret_val = True
        else:
            ret_val = False
        return ret_val


    def overlaps_with(self, rect, padding = 0):
        for x in range(self.left-padding, self.right+1+padding):
            for y in range(self.top-padding, self.bottom+1+padding):
                if rect.contains((x,y)):
                    return True
        return False


    def random_point_on_edge(self, direction):
        if direction in ('top', 'N'):
            r = random.randint(1, self.width-2)
            coord = (self.tl[0] + r, self.top)

        elif direction in ('bottom', 'S'):
            r = random.randint(1, self.width-2)
            coord = (self.tl[0] + r, self.bottom)

        elif direction in ('right', 'E'):
            r = random.randint(1, self.height-2)
            coord = (self.right, self.tl[1]+r)

        elif direction in ('left', 'W'):
            r = random.randint(1, self.height-2)
            coord = (self.left, self.tl[1]+r)

        else:
            raise ValueError

        return coord


    def closest_neighbour(self, rect_list):
        best_distance = 100
        ret_rect = None
        for r in rect_list:
            x2, y2 = r.center
            x1, y1 = self.center
            distance = ((x2-x1)**2 + (y2-y1)**2 )**0.5
            if distance < best_distance and distance > 0:
                best_distance = distance
                ret_rect = r

        return ret_rect


#-------------------------------------------------------------------------
class LineSeg():

    def __init__(self, start, direction, length):
        self.start = start
        self.direction = direction
        self.length = length

    def __str__(self):
        return f"{self.start},{self.get_endpoint()}"

    def __repr__(self):
        return f"LineSeg:{self}"

    def get_endpoint(self):
        if self.direction in ('up', 'N'):
            x = self.start[0]
            y = self.start[1] - (self.length-1)

        elif self.direction in ('down', 'S'):
            x = self.start[0]
            y = self.start[1] + (self.length-1)

        elif self.direction in ('right', 'E'):
            x = self.start[0] + (self.length-1)
            y = self.start[1]

        elif self.direction in ('left', 'W'):
            x = self.start[0] - (self.length-1)
            y = self.start[1]

        else:
            raise ValueError

        return (x, y)


    def overlaps_with_rect(self, rect):
        x1, y1 = self.start
        x2, y2 = self.get_endpoint()

        for x in range(min(x1, x2), max(x1,x2)+1):
            for y in range(min(y1, y2), max(y1,y2)+1):
                if rect.contains((x,y)):
                    return True
        return False


    def overlaps_with_edge(self, rect):
        x1, y1 = self.start
        #x2, y2 = self.get_endpoint()

        if not self.overlaps_with_rect(rect):
            return False

        if self.direction in ('E', 'W'):
            return y1 == rect.top or y1 == rect.bottom
        else:
            return x1 == rect.left or x1 == rect.right


    def check_empty_space(self, floor):
        x2, y2 = self.get_endpoint()
        x1, y1 = self.start

        allow_list = [ "empty", "vwall", "hwall" ]

        for x in range(min(x1, x2), max(x1,x2)+1):
            for y in range(min(y1, y2), max(y1,y2)+1):
                #floor.tiles[x][y].set_type("fountain")
                try:
                    if not floor.tiles[x][y].type in allow_list:
                        return False
                except IndexError:
                    return False
        return True



