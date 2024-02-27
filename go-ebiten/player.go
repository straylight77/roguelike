package main

import "fmt"

type Player struct {
	X, Y  int
	HP    int
	AC    int
	toHit int
}

// -----------------------------------------------------------------------
func (p *Player) SetPos(x, y int) {
	p.X = x
	p.Y = y
}

// -----------------------------------------------------------------------
func (p *Player) Attack(m *Monster) string {

	dmg := 1
	m.HP -= dmg
	msg := fmt.Sprintf(
		"You attack the %v and hit for %d damage (%d remaining).",
		m.Name,
		dmg,
		m.HP,
	)
	return msg
}

// -----------------------------------------------------------------------
func (p *Player) InfoPanelString() []string {
	// draw the info text side panel
	info := []string{
		fmt.Sprintf("Name:  Rodney"),
		fmt.Sprintf("Str:   16 / 16"),
		fmt.Sprintf("HP:    %d / 20", p.HP),
		fmt.Sprintf("Exp:    2 / 14"),
		"\n",
		fmt.Sprintf("Gold:  4"),
		fmt.Sprintf("Depth: 1"),
		fmt.Sprintf("Pos:   %d,%d", p.X, p.Y),
	}
	return info
}
