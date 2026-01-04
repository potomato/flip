from collections import deque
import pgzero
import pygame
from pgzero.clock import clock
import random
import pgzrun

from HighScore import HighScore
from Ship import Ship
from Rocks import Rocks
screen : pgzero.screen.Screen
keyboard : pgzero.keyboard.Keyboard
Actor : pgzero.actor.Actor

# constants
WIDTH = 800
HEIGHT = 600


class Game:
    def __init__(self, width, height, score_height, speed = 3):
        self.width = width
        self.height = height
        self.score_height = score_height
        self.speed = speed
        self.crashed = False
        self.show_fliptext = False
        self.score = HighScore(self.score_height)
        self.rocks = Rocks(self.width, self.height, self.score_height, self.speed)
        self.ship = Ship()
        self.ship.set_position(self.rocks.initial_ship_position())
        clock.schedule_interval(self.flip, 10.0)

    def draw(self):
        screen.clear()
        # draw objects
        self.score.draw(screen)
        self.rocks.draw(screen)
        self.ship.draw()
        # draw text
        if self.crashed:
            screen.draw.text("GAME OVER", center=(self.width/2, self.height/2), fontsize=64, color='white')
        elif self.show_fliptext:
            screen.draw.text("FLIP!", center=(self.width/2, self.height/2), fontsize=64, color='yellow')

    def update(self):
        if self.crashed:
            return
        self.rocks.update()
        # move ship if need be
        self.ship.update(keyboard)
        # check for crash
        if self.rocks.hit_by(self.ship.actor):
            self.crashed = True
            clock.unschedule(self.hide_fliptext)
            clock.unschedule(self.flip)
        else:
            self.score.add_distance(self.speed)

    def flip(self):
        if self.crashed:
            return
        self.rocks.flip()
        self.ship.flip()
        self.show_fliptext = True
        clock.schedule_unique(self.hide_fliptext, 1.0)
        next_flip = random.random() * 8 + 4
        clock.schedule_unique(self.flip, next_flip)

    def hide_fliptext(self):
        self.show_fliptext = False


game = Game(WIDTH, HEIGHT, 40)

def draw():
    game.draw()

def update():
    game.update()

def on_mouse_down():
    global game
    if not game.crashed:
        return
    game = Game(WIDTH, HEIGHT, 40)

pgzrun.go()