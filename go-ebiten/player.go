package main

import "fmt"

type Player struct {
	X, Y int
}

// -----------------------------------------------------------------------
func (p *Player) SetPos(x, y int) {
	p.X = x
	p.Y = y
}

// -----------------------------------------------------------------------
func (p *Player) InfoPanelString() []string {
	// draw the info text side panel
	info := []string{
		fmt.Sprintf("Name:  Rodney"),
		fmt.Sprintf("Str:   16 / 16"),
		fmt.Sprintf("HP:    14 / 20"),
		fmt.Sprintf("Exp:    2 / 14"),
		"\n",
		fmt.Sprintf("Gold:  4"),
		fmt.Sprintf("Depth: 1"),
		fmt.Sprintf("Pos:   %d,%d", p.X, p.Y),
	}
	return info
}
