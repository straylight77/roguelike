package main

import (
	"image"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

// per row = 49
// A: 918
// N: 967

const (
	T_WALL       = 638
	T_PATH       = 3
	T_FLOOR      = 1
	T_DOOR_OP    = 448
	T_DOOR_CL    = 445
	T_UP         = 298
	T_DOWN       = 297
	T_HERO       = 28
	T_POTION     = 672
	T_SCROLL     = 770
	T_RING       = 338
	T_WEAPON     = 0
	T_ARMOR      = 0
	T_RUSTMON    = 270
	T_STIRGE     = 419
	T_ANKHEG     = 276
	T_DRAGON     = 422
	T_WORG       = 375
	T_ROPER      = 418
	T_CHIMERA    = 273
	T_HOBGOBLIN  = 127
	T_COCKATRICE = 370
	T_PURPLEWORM = 421
	T_GOBLIN     = 178
	T_LEPRECHAUN = 468
	T_UNMBERHULK = 325
	T_NYMPH      = 277
	T_ORC        = 467
	T_INVSTALKER = 417
	T_QUASIT     = 128
	T_SPIDER     = 274
	T_JELLY      = 420
	T_TROLL      = 323
	T_XORN       = 271
	T_MAGE       = 123
	T_WRAITH     = 368
	T_MIMIC      = 486
	T_GOLEM      = 326
	T_ZOMBIE     = 324
)

type Spritesheet struct {
	TileSize   int
	TileXCount int
	Img        *ebiten.Image
}

// -----------------------------------------------------------------------
func NewSpritesheet(fname string, tileSize int) *Spritesheet {
	img, _, err := ebitenutil.NewImageFromFile("assets/" + fname)
	if err != nil {
		log.Fatal(err)
	}
	width := img.Bounds().Dx() // width in pixels

	s := &Spritesheet{
		tileSize,
		width / tileSize,
		img,
	}
	return s
}

// -----------------------------------------------------------------------
func (s *Spritesheet) Tile(id int) *ebiten.Image {
	id = id - 1 // tile nubmers start at 1
	sx := (id % s.TileXCount) * s.TileSize
	sy := (id / s.TileXCount) * s.TileSize
	rect := image.Rect(sx, sy, sx+s.TileSize, sy+s.TileSize)
	return s.Img.SubImage(rect).(*ebiten.Image)
}
