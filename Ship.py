import pgzero.keyboard
from pgzero.actor import Actor

class Ship:
    def __init__(self, move_by = 2):
        self.move_by = move_by
        self.actor = Actor('ship')

    def set_position(self, pos):
        self.actor.center = pos
    
    def draw(self):
        self.actor.draw()

    def update(self, keyboard: pgzero.keyboard.Keyboard):
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

