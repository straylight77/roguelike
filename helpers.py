import textwrap

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




