package main

import (
	"embed"
	"fmt"
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	"github.com/hajimehoshi/ebiten/v2/text"
	"golang.org/x/image/font"
)

const (
	ScreenMaxX, ScreenMaxY = 1024, 768
	MapMaxX, MapMaxY       = 45, 40
	FontSize               = 16
	TileSize               = 16
)

//go:embed assets/*
var assets embed.FS

var sheet *Spritesheet

type Pos struct {
	x, y int
}

/*************************************************************************
 *                             GAME OBJECT                               *
 *************************************************************************/

type Game struct {
	keys     []ebiten.Key
	font     font.Face
	dungeon  *DungeonLevel
	player   Pos
	messages MessageQueue
}

// -----------------------------------------------------------------------
func NewGame() *Game {
	dungeon := NewDungeonLevel()
	player_pos := dungeon.Generate()

	font := loadFont("assets/fantasquesansmono-regular.otf", FontSize)

	mq := MessageQueue{}
	//mq.Add("---------1---------2---------3---------4---------5---------6---------7---------8---------9")
	mq.Add("Hello Rodney, welcome to the Dungeons of Doom!")

	g := &Game{
		dungeon:  dungeon,
		player:   player_pos,
		font:     font,
		messages: mq,
	}
	return g
}

// -----------------------------------------------------------------------
func (g *Game) Update() error {
	g.keys = inpututil.AppendJustPressedKeys(g.keys[:0])

	for _, p := range g.keys {
		switch p {
		case ebiten.KeyEscape,
			ebiten.KeyQ:
			return ebiten.Termination
		case ebiten.KeyLeft:
			MovePlayer(g, -1, 0)
		case ebiten.KeyRight:
			MovePlayer(g, 1, 0)
		case ebiten.KeyUp:
			MovePlayer(g, 0, -1)
		case ebiten.KeyDown:
			MovePlayer(g, 0, 1)
		default:
			g.messages.Add(fmt.Sprintf("I don't know that command (%v)", p))
		}
	}
	return nil
}

// -----------------------------------------------------------------------
func (g *Game) InfoPanelString() []string {
	// draw the info text side panel
	info := []string{
		fmt.Sprintf("Name:  Rodney"),
		fmt.Sprintf("Str:   16 / 16"),
		fmt.Sprintf("HP:    14 / 20"),
		fmt.Sprintf("Exp:    2 / 14"),
		"\n",
		fmt.Sprintf("Pos:   %d,%d", g.player.x, g.player.y),
		fmt.Sprintf("Depth: 1"),
		fmt.Sprintf("Gold:  4"),
	}
	return info
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

	// draw the message queue panel
	for i, m := range g.messages.Tail(5) {
		text.Draw(screen, m, g.font, 0, MapMaxY*TileSize+FontSize+i*(FontSize+3), color.White)
	}

	// draw the info panel
	for i, s := range g.InfoPanelString() {
		text.Draw(screen, s, g.font, MapMaxX*TileSize, FontSize+i*(FontSize+5), color.White)
	}

}

// -----------------------------------------------------------------------
func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	return ScreenMaxX, ScreenMaxY
}

// -----------------------------------------------------------------------
func MovePlayer(g *Game, dx, dy int) {
	id := g.dungeon.Tile(g.player.x+dx, g.player.y+dy)
	switch id {
	case 0,
		T_WALL:
		g.messages.Add("That way is blocked!")
		return
	case T_DOOR_CL:
		g.dungeon.SetTile(g.player.x+dx, g.player.y+dy, T_DOOR_OP)
		g.messages.Add("You open the door.")
	default:
		g.player.x += dx
		g.player.y += dy
	}
}

/*************************************************************************
 *                          HELPER FUNCTIONS                             *
 *************************************************************************/

// -----------------------------------------------------------------------
func DrawTile(screen *ebiten.Image, img *ebiten.Image, x int, y int) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(float64(x*sheet.TileSize), float64(y*sheet.TileSize))
	screen.DrawImage(img, op)
}

// -----------------------------------------------------------------------
func main() {
	sheet = NewSpritesheet("colored_packed.png", TileSize)
	g := NewGame()
	ebiten.SetWindowSize(ScreenMaxX, ScreenMaxY)
	ebiten.SetWindowTitle("Rogue Redux")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
