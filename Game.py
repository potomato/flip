from HighScore import HighScore
from Ship import Ship
from Rocks import Rocks
from pgzero.clock import clock
import pgzero.screen
import pgzero.keyboard
import random

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score_height = 40
        self.speed = 3
        self.crashed = False
        self.show_fliptext = False
        self.score = HighScore(self.score_height)
        self.rocks = Rocks(self.width, self.height, self.score_height, self.speed)
        self.ship = Ship()
        self.ship.set_position(self.rocks.initial_ship_position())
        clock.schedule_interval(self.flip, 10.0)

    def draw(self, screen : pgzero.screen.Screen):
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

    def update(self, keyboard: pgzero.keyboard.Keyboard):
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
