import pgzero
import pgzero.screen
import pgzero.keyboard
import pgzrun
from Game import Game

screen : pgzero.screen.Screen
keyboard : pgzero.keyboard.Keyboard

# constants
WIDTH = 800
HEIGHT = 600

def new_game():
    return Game(WIDTH, HEIGHT)

def draw():
    game.draw(screen)

def update():
    game.update(keyboard)

def on_mouse_down():
    global game
    if not game.crashed:
        return
    game = new_game()


game = Game(WIDTH, HEIGHT)

pgzrun.go()