package main

import "math"

type MonsterTemplate struct {
	Name   string
	TileID int
	HP     string
	AC     int
}

var MonsterLib = []MonsterTemplate{
	{"goblin", T_GOBLIN, "1d4", 11},
	{"stirge", T_STIRGE, "1", 12},
}

/*************************************************************************
 *                                MONSTER                                *
 *************************************************************************/

type Monster struct {
	X, Y   int
	Name   string
	TileID int
	HP     int
	AC     int
	toHit  int
}

// -----------------------------------------------------------------------
func NewMonster(id int) *Monster {

	mt := MonsterLib[id]

	m := &Monster{
		Name:   mt.Name,
		TileID: mt.TileID,
	}
	return m
}

// -----------------------------------------------------------------------
func (m *Monster) Move(destX, destY int) {
	m.X = destX
	m.Y = destY
}

/*************************************************************************
 *                           MONSTER LAYER                               *
 *************************************************************************/

type MonsterLayer []*Monster

// -----------------------------------------------------------------------
func (ml *MonsterLayer) Add(m *Monster, x, y int) {
	m.X, m.Y = x, y
	*ml = append(*ml, m)
}

// -----------------------------------------------------------------------
func (ml *MonsterLayer) Remove(idx int) {
	*ml = append((*ml)[:idx], (*ml)[idx+1:]...)
}

// -----------------------------------------------------------------------
func (ml *MonsterLayer) Clear() {
	*ml = nil
}

// -----------------------------------------------------------------------
func (ml MonsterLayer) MonsterAt(x, y int) *Monster {
	for _, m := range ml {
		if m.X == x && m.Y == y {
			return m
		}
	}
	return nil
}

func calculateDistance(x1, y1, x2, y2 int) float64 {
	dx := float64(x2 - x1)
	dy := float64(y2 - y1)
	return math.Sqrt(dx*dx + dy*dy)
}
