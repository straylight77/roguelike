package main

import (
	"log"

	"github.com/hajimehoshi/ebiten/v2"
)

var sheet *Spritesheet

type Game struct{}

// -----------------------------------------------------------------------
func NewGame() *Game {
	g := &Game{}
	return g
}

// -----------------------------------------------------------------------
func (g *Game) Update() error {
	return nil
}

// -----------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {

	max_x, max_y := 5, 5
	dungeon := []int{
		T_WALL, T_WALL, T_WALL, T_WALL, T_WALL,
		T_WALL, T_FLOOR, T_FLOOR, T_UP, T_WALL,
		T_WALL, T_FLOOR, T_FLOOR, T_FLOOR, T_DOOR_CL,
		T_WALL, T_RING, T_FLOOR, T_FLOOR, T_WALL,
		T_WALL, T_WALL, T_DOOR_OP, T_WALL, T_WALL,
	}
	for x := 0; x < max_x; x++ {
		for y := 0; y < max_y; y++ {
			DrawTile(screen, sheet.Tile(dungeon[x+(max_x*y)]), x+1, y+1)
		}
	}

	DrawTile(screen, sheet.Tile(T_HERO), 3, 3)
	DrawTile(screen, sheet.Tile(T_PATH), 3, 6)
	DrawTile(screen, sheet.Tile(T_PATH), 3, 7)
	DrawTile(screen, sheet.Tile(T_PATH), 4, 7)
}

// -----------------------------------------------------------------------
func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	//return 320, 240
	return 640, 480
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
	ebiten.SetWindowSize(640, 480)
	ebiten.SetWindowTitle("1-Bit Rogue")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
