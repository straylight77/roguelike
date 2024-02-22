package main

import (
	"fmt"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

const (
	ScreenMaxX, ScreenMaxY = 1280, 720
	MapMaxX, MapMaxY       = 80, 25
)

var sheet *Spritesheet

type Pos struct {
	x, y int
}

type Game struct {
	keys    []ebiten.Key
	dungeon *DungeonLevel
	player  Pos
}

// -----------------------------------------------------------------------
func NewGame() *Game {
	dungeon := NewDungeonLevel()
	dungeon.CreateRoom(3, 3, 8, 6)
	dungeon.CreatePath(7, 9, SOUTH, 5)
	dungeon.CreatePath(7, 13, EAST, 5)
	dungeon.CreateRoom(12, 10, 10, 10)
	dungeon.SetTile(7, 8, T_DOOR_OP)
	dungeon.SetTile(12, 13, T_DOOR_OP)
	dungeon.SetTile(10, 5, T_DOOR_CL)
	player_pos := Pos{5, 5}

	g := &Game{
		dungeon: dungeon,
		player:  player_pos,
	}
	return g
}

// -----------------------------------------------------------------------
func MovePlayer(p *Pos, d *DungeonLevel, dx, dy int) {
	switch id := d.Tile(p.x+dx, p.y+dy); id {
	case 0:
		return
	case T_WALL:
		return
	case T_DOOR_CL:
		d.SetTile(p.x+dx, p.y+dy, T_DOOR_OP)
	default:
		p.x += dx
		p.y += dy
	}
}

// -----------------------------------------------------------------------
func (g *Game) Update() error {
	g.keys = inpututil.AppendJustPressedKeys(g.keys[:0])

	for _, p := range g.keys {
		switch p {
		case ebiten.KeyEscape:
			return ebiten.Termination
		case ebiten.KeyLeft:
			MovePlayer(&g.player, g.dungeon, -1, 0)
		case ebiten.KeyRight:
			MovePlayer(&g.player, g.dungeon, 1, 0)
		case ebiten.KeyUp:
			MovePlayer(&g.player, g.dungeon, 0, -1)
		case ebiten.KeyDown:
			MovePlayer(&g.player, g.dungeon, 0, 1)
		default:
			fmt.Println(p)
		}
	}
	return nil
}

// -----------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {

	// draw dungeon tiles
	for x, col := range g.dungeon {
		for y, id := range col {
			DrawTile(screen, sheet.Tile(id), x, y)
		}
	}

	// draw player
	DrawTile(screen, sheet.Tile(T_HERO), g.player.x, g.player.y)
}

// -----------------------------------------------------------------------
func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	return ScreenMaxX, ScreenMaxY
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
	ebiten.SetWindowSize(ScreenMaxX, ScreenMaxY)
	ebiten.SetWindowTitle("1-Bit Rogue")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
