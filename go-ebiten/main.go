package main

import (
	"log"

	"github.com/hajimehoshi/ebiten/v2"
)

const (
	SCREEN_MAX_X, SCREEN_MAX_Y = 1280, 720
	MAP_MAX_X, MAP_MAX_Y       = 80, 25
)

var sheet *Spritesheet

type Pos struct {
	x, y int
}

type Game struct {
	dungeon *DungeonLevel
	player  Pos
}

// -----------------------------------------------------------------------
func NewGame() *Game {
	dungeon := NewDungeonLevel()
	dungeon.CreateRoom(3, 3, 8, 6)
	player_pos := Pos{5, 5}
	g := &Game{
		dungeon,
		player_pos,
	}
	return g
}

// -----------------------------------------------------------------------
func (g *Game) Update() error {
	return nil
}

// -----------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {

	for x, row := range g.dungeon {
		for y, id := range row {
			DrawTile(screen, sheet.Tile(id), x, y)
		}
	}

	DrawTile(screen, sheet.Tile(T_HERO), g.player.x, g.player.y)

	//DrawTile(screen, sheet.Tile(T_PATH), 3, 6)
	//DrawTile(screen, sheet.Tile(T_PATH), 3, 7)
	//DrawTile(screen, sheet.Tile(T_PATH), 4, 7)
}

// -----------------------------------------------------------------------
func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	return SCREEN_MAX_X, SCREEN_MAX_Y
}

// -----------------------------------------------------------------------
func DrawTile(screen *ebiten.Image, img *ebiten.Image, x int, y int) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(float64(x*sheet.TileSize), float64(y*sheet.TileSize))
	screen.DrawImage(img, op)
}

// -----------------------------------------------------------------------
func main() {
	sheet = NewSpritesheet("colored_packed.png", 16)
	g := NewGame()
	ebiten.SetWindowSize(SCREEN_MAX_X, SCREEN_MAX_Y)
	ebiten.SetWindowTitle("1-Bit Rogue")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
