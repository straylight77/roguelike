package main

import (
	"image"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

type Spritesheet struct {
	TileSize   int
	TileXCount int
	Img        *ebiten.Image
}

func NewSpritesheet(fname string, tileSize int) *Spritesheet {
	s := &Spritesheet{}

	var err error
	s.Img, _, err = ebitenutil.NewImageFromFile("assets/" + fname)
	if err != nil {
		log.Fatal(err)
	}

	s.TileSize = tileSize
	w := s.Img.Bounds().Dx()      // width in pixels
	s.TileXCount = w / s.TileSize // width in number of tiles

	return s
}

func (s *Spritesheet) TileImg(id int) *ebiten.Image {
	id = id - 1 // tile nubmers start at 1
	sx := (id % s.TileXCount) * s.TileSize
	sy := (id / s.TileXCount) * s.TileSize
	rect := image.Rect(sx, sy, sx+s.TileSize, sy+s.TileSize)
	return s.Img.SubImage(rect).(*ebiten.Image)
}

// -----------------------------------------------------------------------

var sheet *Spritesheet

type Game struct{}

func NewGame() *Game {
	g := &Game{}
	return g
}

func (g *Game) Update() error {
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {

	max_x, max_y := 5, 5
	dungeon := []int{
		T_WALL, T_WALL, T_WALL, T_WALL, T_WALL,
		T_WALL, T_FLOR, T_FLOR, T_STUP, T_WALL,
		T_WALL, T_FLOR, T_FLOR, T_FLOR, T_DRCL,
		T_WALL, T_FLOR, T_FLOR, T_FLOR, T_WALL,
		T_WALL, T_WALL, T_DROP, T_WALL, T_WALL,
	}
	for x := 0; x < max_x; x++ {
		for y := 0; y < max_y; y++ {
			DrawTile(screen, sheet.TileImg(dungeon[x+(max_x*y)]), x+1, y+1)
		}
	}

	DrawTile(screen, sheet.TileImg(T_HERO), 3, 3)
	//DrawTile(screen, sheet.TileImg(T_PATH), 3, 6)
	//DrawTile(screen, sheet.TileImg(T_PATH), 3, 7)
	//DrawTile(screen, sheet.TileImg(T_PATH), 4, 7)
}

func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	return 320, 240
	//return 640, 480
}

func DrawTile(screen *ebiten.Image, img *ebiten.Image, x int, y int) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(float64(x*sheet.TileSize), float64(y*sheet.TileSize))
	screen.DrawImage(img, op)

}

func main() {
	sheet = NewSpritesheet("colored_packed.png", 16)
	g := NewGame()
	ebiten.SetWindowSize(640, 480)
	ebiten.SetWindowTitle("Rogue Retro")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
