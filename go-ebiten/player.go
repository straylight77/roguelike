package main

type Player struct {
	X, Y int
}

// -----------------------------------------------------------------------
func (p *Player) SetPos(x, y int) {
	p.X = x
	p.Y = y
}
