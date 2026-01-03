from collections import deque
import pgzero
import pygame
from pgzero.clock import clock
import random
import pgzrun
screen : pgzero.screen.Screen
keyboard : pgzero.keyboard.Keyboard
Actor : pgzero.actor.Actor

# constants
WIDTH = 800
HEIGHT = 600
CAVEHEIGHT = 150
INFO_HEIGHT = 40


class HighScore:
    def __init__(self, height):
        self.height = height
        self.score = 0
    
    def add_distance(self, dist):
        self.score += dist

    def draw(self):
        screen.draw.text(f"Score: {self.score}", topleft=(0, 0), fontsize=INFO_HEIGHT, color='white')

class Rocks:
    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.top_rocks = deque()
        self.bottom_rocks = deque()
        self.rock_color = 'red'
        self.add_slice(int(height/3), 0, width)
        self.add_more_rocks()

    def initial_ship_position(self):
        shipH = self.top_rocks[0].bottom + int(CAVEHEIGHT/2)
        return WIDTH/4, shipH

    def draw(self):
        for rock in self.top_rocks:
            screen.draw.filled_rect(rock, self.rock_color)
        for rock in self.bottom_rocks:
            screen.draw.filled_rect(rock, self.rock_color)

    def update(self):
        # add new rocks, move them all and remove offscreen ones
        self.add_more_rocks()
        for rect in self.top_rocks:
            rect.move_ip(-self.speed, 0)
        for rect in self.bottom_rocks:
            rect.move_ip(-self.speed, 0)
        self.remove_old_rocks()

    def hit_by(self, actor):
        return actor.collidelist(self.top_rocks) != -1 or actor.collidelist(self.bottom_rocks) != -1

    def flip(self):
        self.rock_color = 'green' if self.rock_color == 'red' else 'red'

    def add_more_rocks(self):
        while (self.top_rocks[-1].right < self.width):
            self.add_slice(self.top_rocks[-1].bottom, self.top_rocks[-1].right)

    def add_slice(self, prevheight, prevright, width=None):
            newRect = self.new_top_rock(prevheight, width)
            newRect.left = prevright
            self.top_rocks.append(newRect)
            bottomRect = pygame.Rect(newRect.left, newRect.bottom + CAVEHEIGHT, newRect.width, self.height - (newRect.bottom + CAVEHEIGHT))
            self.bottom_rocks.append(bottomRect)

    def remove_old_rocks(self):
        while (self.top_rocks[0].right < 0):
            self.top_rocks.popleft()
        while (self.bottom_rocks[0].right < 0):
            self.bottom_rocks.popleft()

    def new_top_rock(self, prevheight, width=None):
        return pygame.Rect(0, INFO_HEIGHT, width or self.new_rock_width(), self.new_top_height(prevheight) - INFO_HEIGHT)

    def new_rock_width(self):
        return random.randint(0, int(self.width/20) - 5) + 5

    def new_top_height(self, prevheight):
        while True:
            range = random.randint(-30, 30)
            if random.randint(0,1) > 0.5:
                range = -range
            if (prevheight + range) > self.height * 0.25 and (prevheight + range) < self.height * 0.75 - CAVEHEIGHT:
                break
        return prevheight + range

class Ship:
    def __init__(self, move_by = 2):
        self.move_by = move_by
        self.actor = Actor('ship')

    def set_position(self, pos):
        self.actor.center = pos
    
    def draw(self):
        self.actor.draw()

    def update(self):
        if keyboard.up:
            self.actor.y -= self.move_by
        if keyboard.down:
            self.actor.y += self.move_by
        if keyboard.right:
            self.actor.x += self.move_by
        if keyboard.left:
            self.actor.x -= self.move_by

    def flip(self):
        self.move_by = -self.move_by

class Game:
    def __init__(self, speed = 3):
        self.score = HighScore(INFO_HEIGHT)
        self.rocks = Rocks(WIDTH, HEIGHT, speed)
        self.ship = Ship()
        self.speed = speed
        self.crashed = False
        self.show_fliptext = False
        self.ship.set_position(self.rocks.initial_ship_position())
        clock.schedule_interval(self.flip, 10.0)

    def draw(self):
        screen.clear()
        # draw objects
        self.score.draw()
        self.rocks.draw()
        self.ship.draw()
        # draw text
        if self.crashed:
            screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2), fontsize=64, color='white')
        elif self.show_fliptext:
            screen.draw.text("FLIP!", center=(WIDTH/2, HEIGHT/2), fontsize=64, color='yellow')

    def update(self):
        if self.crashed:
            return
        self.rocks.update()
        # move ship if need be
        self.ship.update()
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


game = Game()

def draw():
    game.draw()

def update():
    game.update()

def on_mouse_down():
    global game
    if not game.crashed:
        return
    game = Game()

pgzrun.go()