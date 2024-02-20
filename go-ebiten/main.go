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

	//max_x, max_y := 5, 5
	//dungeon := []int{
	//	T_WALL, T_WALL, T_WALL, T_WALL, T_WALL,
	//	T_WALL, T_FLOOR, T_FLOOR, T_UP, T_WALL,
	//	T_WALL, T_FLOOR, T_FLOOR, T_FLOOR, T_DOOR_CL,
	//	T_WALL, T_RING, T_FLOOR, T_FLOOR, T_WALL,
	//	T_WALL, T_WALL, T_DOOR_OP, T_WALL, T_WALL,
	//}

	max_x, max_y := 26, 2
	dungeon := []int{
		T_A, T_B, T_C, T_D, T_E, T_F, T_G, T_H, T_I, T_J, T_K, T_L, T_M,
		T_N, T_O, T_P, T_Q, T_R, T_S, T_T, T_U, T_V, T_W, T_X, T_Y, T_Z,
		269, 418, 275, 421, 374, 417, 272, 126, 369, 420, 177, 467, 324,
		276, 466, 416, 127, 273, 419, 322, 270, 122, 367, 485, 325, 323,
	}
	for x := 0; x < max_x; x++ {
		for y := 0; y < max_y; y++ {
			DrawTile(screen, sheet.Tile(dungeon[x+(max_x*y)]), x, y)
		}
	}

	//DrawTile(screen, sheet.Tile(T_HERO), 3, 3)
	//DrawTile(screen, sheet.Tile(T_PATH), 3, 6)
	//DrawTile(screen, sheet.Tile(T_PATH), 3, 7)
	//DrawTile(screen, sheet.Tile(T_PATH), 4, 7)
}

// -----------------------------------------------------------------------
func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	return 640, 240
	//return 640, 480
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
	ebiten.SetWindowSize(1280, 480)
	ebiten.SetWindowTitle("1-Bit Rogue")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
