package main

const (
	NORTH = iota
	EAST
	SOUTH
	WEST
)

//TODO add Tile struct with fields for IsVisibile, Walkable, Visited, etc.

type DungeonLayer [MapMaxX][MapMaxY]int

// -----------------------------------------------------------------------
func (dl *DungeonLayer) SetTile(x, y int, id int) {
	dl[x][y] = id
}

// -----------------------------------------------------------------------
func (dl *DungeonLayer) TileAt(x, y int) int {
	return dl[x][y]
}

// -----------------------------------------------------------------------
func (dl *DungeonLayer) Clear() {
	for x, col := range dl {
		for y := range col {
			dl[x][y] = 0
		}
	}
}

// -----------------------------------------------------------------------
func (dl *DungeonLayer) CreateRoom(x1, y1, dx, dy int) {
	// horizontal walls
	for x := x1; x < x1+dx; x++ {
		dl[x][y1] = T_WALL
		dl[x][y1+dy-1] = T_WALL
	}
	// vertical walls
	for y := y1; y < y1+dy; y++ {
		dl[x1][y] = T_WALL
		dl[x1+dx-1][y] = T_WALL
	}
	// floor
	for x := x1 + 1; x < x1+dx-1; x++ {
		for y := y1 + 1; y < y1+dy-1; y++ {
			dl[x][y] = T_FLOOR
		}
	}
}

// -----------------------------------------------------------------------
func (dl *DungeonLayer) CreatePath(x1, y1 int, dir int, length int) {
	dx, dy := getDirectionCoords(dir)
	x, y := x1, y1
	for i := length; i > 0; i-- {
		dl[x][y] = T_PATH
		x += dx
		y += dy
	}
}

// -----------------------------------------------------------------------
func (dl *DungeonLayer) Generate() (int, int) {
	dl.CreateRoom(3, 3, 8, 6)
	dl.CreatePath(7, 9, SOUTH, 5)
	dl.CreatePath(7, 13, EAST, 5)
	dl.CreateRoom(12, 10, 10, 10)
	dl.SetTile(7, 8, T_DOOR_OP)
	dl.SetTile(12, 13, T_DOOR_OP)
	dl.SetTile(10, 5, T_DOOR_CL)
	return 5, 5
}

func getDirectionCoords(dir int) (int, int) {
	dx, dy := 0, 0
	switch dir {
	case NORTH:
		dy = -1
	case SOUTH:
		dy = 1
	case EAST:
		dx = 1
	case WEST:
		dx = -1
	}
	return dx, dy
}
