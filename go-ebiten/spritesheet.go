package main

import (
	"image"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

// wall:		637
// open door:   447
// closed door: 444
// player:		1021 (or 27)
// stairs up:   297
// stairs down: 296
// path:		2
// per row = 49

const (
	T_WALL       = 637
	T_PATH       = 2
	T_FLOOR      = 0
	T_DOOR_OP    = 447
	T_DOOR_CL    = 444
	T_UP         = 297
	T_DOWN       = 296
	T_HERO       = 27
	T_A          = 917
	T_B          = 918
	T_C          = 919
	T_D          = 920
	T_E          = 921
	T_F          = 922
	T_G          = 923
	T_H          = 924
	T_I          = 925
	T_J          = 926
	T_K          = 927
	T_L          = 928
	T_M          = 929
	T_N          = 966
	T_O          = 967
	T_P          = 968
	T_Q          = 969
	T_R          = 970
	T_S          = 971
	T_T          = 972
	T_U          = 973
	T_V          = 974
	T_W          = 975
	T_X          = 976
	T_Y          = 977
	T_Z          = 978
	T_POTION     = 671
	T_SCROLL     = 769
	T_RING       = 337
	T_WEAPON     = 0
	T_ARMOR      = 0
	T_RUSTMON    = 269
	T_STIRGE     = 418
	T_ANKHEG     = 275
	T_DRAGON     = 421
	T_WORG       = 374
	T_ROPER      = 417
	T_CHIMERA    = 272
	T_HOBGOBLIN  = 126
	T_COCKATRICE = 369
	T_PURPLEWORM = 420
	T_GOBLIN     = 177
	T_LEPRECHAUN = 467
	T_UNMBERHULK = 324
	T_NYMPH      = 276
	T_ORC        = 466
	T_INVSTALKER = 416
	T_QUASIT     = 127
	T_SPIDER     = 273
	T_JELLY      = 419
	T_TROLL      = 322
	T_XORN       = 270
	T_MAGE       = 122
	T_WRAITH     = 367
	T_MIMIC      = 485
	T_GOLEM      = 325
	T_ZOMBIE     = 323
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
	//id = id - 1 // tile nubmers start at 1
	sx := (id % s.TileXCount) * s.TileSize
	sy := (id / s.TileXCount) * s.TileSize
	rect := image.Rect(sx, sy, sx+s.TileSize, sy+s.TileSize)
	return s.Img.SubImage(rect).(*ebiten.Image)
}
