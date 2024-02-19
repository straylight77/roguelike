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
	T_WALL    = 637
	T_PATH    = 2
	T_FLOOR   = 0
	T_DOOR_OP = 447
	T_DOOR_CL = 444
	T_UP      = 297
	T_DOWN    = 296
	T_HERO    = 27
	T_A       = 917
	T_B       = 918
	T_C       = 919
	T_D       = 920
	T_E       = 921
	T_F       = 922
	T_G       = 923
	T_H       = 924
	T_I       = 925
	T_J       = 926
	T_K       = 927
	T_L       = 928
	T_M       = 929
	T_N       = 966
	T_POTION  = 671
	T_SCROLL  = 769
	T_RING    = 337
	T_WEAPON  = 0
	T_ARMOR   = 0
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
