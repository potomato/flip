from collections import deque
import pgzero
import pygame
from pgzero.clock import clock
import random
import pgzrun
screen : pgzero.screen.Screen
keyboard : pgzero.keyboard.Keyboard

# constants
WIDTH = 800
HEIGHT = 600
CAVEHEIGHT = 150
INFO_HEIGHT = 40

# global variables
top_rocks = None
bottom_rocks = None
ship_box = None
speed = 3
move_by = 2
rock_color = 'red'
show_fliptext = False
score = 0
crashed = False


def draw():
    screen.clear()
    # draw objects
    for rock in top_rocks:
        screen.draw.filled_rect(rock, rock_color)
    for rock in bottom_rocks:
        screen.draw.filled_rect(rock, rock_color)
    screen.draw.filled_rect(ship_box, 'blue')
    # draw text
    screen.draw.text(f"Score: {score}", topleft=(0, 0), fontsize=INFO_HEIGHT, color='white')
    if crashed:
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2), fontsize=64, color='white')
    elif show_fliptext:
        screen.draw.text("FLIP!", center=(WIDTH/2, HEIGHT/2), fontsize=64, color='yellow')

def update():
    global crashed, speed, score
    # add new rocks, move them all and remove offscreen ones
    add_more_rocks()
    for rect in top_rocks:
        rect.move_ip(-speed, 0)
    for rect in bottom_rocks:
        rect.move_ip(-speed, 0)
    remove_old_rocks()
    # move ship if need be
    if keyboard.up:
        ship_box.move_ip(0, -move_by)
    if keyboard.down:
        ship_box.move_ip(0, move_by)
    if keyboard.right:
        ship_box.move_ip(move_by, 0)
    if keyboard.left:
        ship_box.move_ip(-move_by, 0)
    # check for crash
    if ship_box.collidelist(top_rocks) != -1 or ship_box.collidelist(bottom_rocks) != -1:
        crashed = True
        speed = 0
        clock.unschedule(hide_fliptext)
        clock.unschedule(flip)
    else:
        score += speed

def new_top_rock(prevheight, width=None):
    return pygame.Rect(0, INFO_HEIGHT, width or new_rock_width(), new_top_height(prevheight) - INFO_HEIGHT)

def new_rock_width():
    return random.randint(0, int(WIDTH/20) - 5) + 5

def new_top_height(prevheight):
    while True:
        range = random.randint(-30, 30)
        if random.randint(0,1) > 0.5:
            range = -range
        if (prevheight + range) > HEIGHT * 0.25 and (prevheight + range) < HEIGHT * 0.75 - CAVEHEIGHT:
            break
    return prevheight + range

def add_more_rocks():
    while (top_rocks[-1].right < WIDTH):
        add_slice(top_rocks[-1].bottom, top_rocks[-1].right)

def add_slice(prevheight, prevright, width=None):
        newRect = new_top_rock(prevheight, width)
        newRect.left = prevright
        top_rocks.append(newRect)
        bottomRect = pygame.Rect(newRect.left, newRect.bottom + CAVEHEIGHT, newRect.width, HEIGHT - (newRect.bottom + CAVEHEIGHT))
        bottom_rocks.append(bottomRect)

def remove_old_rocks():
    while (top_rocks[0].right < 0):
        top_rocks.popleft()
    while (bottom_rocks[0].right < 0):
        bottom_rocks.popleft()

def flip():
    if crashed:
        return
    global rock_color, move_by, show_fliptext
    rock_color = 'green' if rock_color == 'red' else 'red'
    move_by = -move_by
    show_fliptext = True
    clock.schedule_unique(hide_fliptext, 1.0)
    next_flip = random.random() * 8 + 4
    clock.schedule_unique(flip, next_flip)

def hide_fliptext():
    global show_fliptext
    show_fliptext = False

def setup():
    global ship_box, top_rocks, bottom_rocks, speed, move_by, rock_color, show_fliptext, score, crashed
    top_rocks = deque()
    bottom_rocks = deque()
    speed = 3
    move_by = 2
    rock_color = 'red'
    show_fliptext = False
    score = 0
    crashed = False
    add_slice(int(HEIGHT/3), 0, WIDTH)
    shipH = top_rocks[0].bottom + int(CAVEHEIGHT/2)
    ship_box = pygame.Rect(0, 0, 20, 20)
    ship_box.center = (WIDTH/4, shipH)
    clock.schedule_interval(flip, 10.0)

def on_mouse_down():
    if not crashed:
        return
    setup()

setup()
pgzrun.go()