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
	MapMaxX, MapMaxY       = 50, 40
	FontSize               = 16
	TileSize               = 16
)

//go:embed assets/*
var assets embed.FS

var sheet *Spritesheet
var font1 font.Face

/*************************************************************************
 *                             GAME OBJECT                               *
 *************************************************************************/

type Game struct {
	keys     []ebiten.Key
	messages MessageQueue
	player   Player
	dungeon  DungeonLayer
	monsters MonsterLayer
}

// -----------------------------------------------------------------------
func NewGame() *Game {

	g := &Game{}

	playerX, playerY := g.dungeon.Generate()
	g.player.SetPos(playerX, playerY)

	g.monsters.Add(NewMonster(0), 14, 12)
	g.monsters.Add(NewMonster(1), 7, 5)

	//g.messages.Add("---------1---------2---------3---------4---------5---------6---------7---------8---------9")
	g.messages.Add("Hello Rodney, welcome to the Dungeons of Doom!")

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
			g.MovePlayer(-1, 0)
		case ebiten.KeyRight:
			g.MovePlayer(1, 0)
		case ebiten.KeyUp:
			g.MovePlayer(0, -1)
		case ebiten.KeyDown:
			g.MovePlayer(0, 1)
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
		fmt.Sprintf("Gold:  4"),
		fmt.Sprintf("Depth: 1"),
		fmt.Sprintf("Pos:   %d,%d", g.player.X, g.player.Y),
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

	// draw monsters
	for _, m := range g.monsters {
		DrawTile(screen, sheet.Tile(m.TileID), m.X, m.Y)
	}

	// draw player
	DrawTile(screen, sheet.Tile(T_HERO), g.player.X, g.player.Y)

	// draw the message queue panel
	for i, m := range g.messages.Tail(5) {
		text.Draw(screen, m, font1, 0, MapMaxY*TileSize+FontSize+i*(FontSize+3), color.White)
	}

	// draw the info panel
	for i, s := range g.InfoPanelString() {
		text.Draw(screen, s, font1, MapMaxX*TileSize, FontSize+i*(FontSize+5), color.White)
	}
}

// -----------------------------------------------------------------------
func (g *Game) Layout(outsideW, outsideH int) (screenWidth, screenHeight int) {
	return ScreenMaxX, ScreenMaxY
}

// -----------------------------------------------------------------------
func (g *Game) MovePlayer(dx, dy int) {

	destX, destY := g.player.X+dx, g.player.Y+dy

	// check for monsters
	if m := g.monsters.MonsterAt(destX, destY); m != nil {
		g.messages.Add(fmt.Sprintf("You attack the %v.", m.Name))
		return
	}

	// check dungeon tile
	id := g.dungeon.Tile(destX, destY)
	switch id {
	case 0,
		T_WALL:
		g.messages.Add("That way is blocked!")
		return
	case T_DOOR_CL:
		g.dungeon.SetTile(g.player.X+dx, g.player.Y+dy, T_DOOR_OP)
		g.messages.Add("You open the door.")
	default:
		g.player.X += dx
		g.player.Y += dy
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
	font1 = loadFont("assets/fantasquesansmono-regular.otf", FontSize)
	g := NewGame()
	ebiten.SetWindowSize(ScreenMaxX, ScreenMaxY)
	ebiten.SetWindowTitle("Rogue Redux")

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
