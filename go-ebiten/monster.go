package main

type Monster struct {
	Name   string
	TileID int
	HP     int
	AC     int
}

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

func NewMonster(id int) *Monster {

	mt := MonsterLib[id]

	m := &Monster{
		Name:   mt.Name,
		TileID: mt.TileID,
	}
	return m
}
