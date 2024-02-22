package main

const (
	NORTH = iota
	EAST
	SOUTH
	WEST
)

type DungeonLevel [MapMaxX][MapMaxY]int

// -----------------------------------------------------------------------
func NewDungeonLevel() *DungeonLevel {
	return &DungeonLevel{}
}

func (dl *DungeonLevel) AddCoords() {
}

// -----------------------------------------------------------------------
func (dl *DungeonLevel) SetTile(x, y int, id int) {
	dl[x][y] = id
}

// -----------------------------------------------------------------------
func (dl *DungeonLevel) Clear() {
	for x, col := range dl {
		for y := range col {
			dl[x][y] = 0
		}
	}
}

// -----------------------------------------------------------------------
func (dl *DungeonLevel) CreateRoom(x1, y1, dx, dy int) {
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
	// TODO

}

// -----------------------------------------------------------------------
func (dl *DungeonLevel) CreatePath(x1, y1 int, dir int, length int) {
	dx, dy := getDirectionCoords(dir)
	x, y := x1, y1
	for i := length; i > 0; i-- {
		dl[x][y] = T_PATH
		x += dx
		y += dy
	}
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
