package main

type DungeonLevel [MAP_MAX_X][MAP_MAX_Y]int

// -----------------------------------------------------------------------
func NewDungeonLevel() *DungeonLevel {
	return &DungeonLevel{}
}

func (dl *DungeonLevel) AddCoords() {
}

// -----------------------------------------------------------------------
func (dl *DungeonLevel) Clear() {
	for x, row := range dl {
		for y := range row {
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
