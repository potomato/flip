from collections import deque
import pgzero.screen
import pygame
import random

class Rocks:
    def __init__(self, width, height, score_height, speed, gap_height = 150):
        self.width = width
        self.height = height
        self.score_height = score_height
        self.speed = speed
        self.gap_height = gap_height
        self.top_rocks = deque()
        self.bottom_rocks = deque()
        self.rock_color = 'red'
        self.add_slice(int(height/3), 0, width)
        self.add_more_rocks()

    def initial_ship_position(self):
        shipH = self.top_rocks[0].bottom + int(self.gap_height/2)
        return self.width/4, shipH

    def draw(self, screen: pgzero.screen.Screen):
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
            bottomRect = pygame.Rect(newRect.left, newRect.bottom + self.gap_height, newRect.width, self.height - (newRect.bottom + self.gap_height))
            self.bottom_rocks.append(bottomRect)

    def remove_old_rocks(self):
        while (self.top_rocks[0].right < 0):
            self.top_rocks.popleft()
        while (self.bottom_rocks[0].right < 0):
            self.bottom_rocks.popleft()

    def new_top_rock(self, prevheight, width=None):
        return pygame.Rect(0, self.score_height, width or self.new_rock_width(), self.new_top_height(prevheight) - self.score_height)

    def new_rock_width(self):
        return random.randint(0, int(self.width/20) - 5) + 5

    def new_top_height(self, prevheight):
        while True:
            range = random.randint(-30, 30)
            if random.randint(0,1) > 0.5:
                range = -range
            if (prevheight + range) > self.height * 0.25 and (prevheight + range) < self.height * 0.75 - self.gap_height:
                break
        return prevheight + range
