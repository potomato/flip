from collections import deque
import pgzero
import pygame
from pgzero.clock import clock
import random
import pgzrun
screen : pgzero.screen.Screen
keyboard : pgzero.keyboard.Keyboard

WIDTH = 800
HEIGHT = 600
VGAP = 150
toprecs = None
bottomrecs = None
shiprect = None
speed = 3
moveby = 2
rock_color = 'red'
show_flip = False

def draw():
    global speed
    screen.clear()
    for toprec in toprecs:
        screen.draw.filled_rect(toprec, rock_color)
    for bottomrec in bottomrecs:
        screen.draw.filled_rect(bottomrec, rock_color)
    screen.draw.filled_rect(shiprect, 'blue')
    if shiprect.collidelist(toprecs) != -1 or shiprect.collidelist(bottomrecs) != -1:
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2), fontsize=64, color='white')
        speed = 0
        clock.unschedule(hide_flip)
        clock.unschedule(flip)
    elif show_flip:
        screen.draw.text("FLIP!", center=(WIDTH/2, HEIGHT/2), fontsize=64, color='yellow')

def update():
    fill()
    trim_offscreen()
    for rect in toprecs:
        rect.move_ip(-speed, 0)
    for rect in bottomrecs:
        rect.move_ip(-speed, 0)
    if keyboard.up:
        shiprect.move_ip(0, -moveby)
    if keyboard.down:
        shiprect.move_ip(0, moveby)
    if keyboard.right:
        shiprect.move_ip(moveby, 0)
    if keyboard.left:
        shiprect.move_ip(-moveby, 0)

def new_toprect(prevheight, width=None):
    return pygame.Rect(0, 0, width or new_width(), new_topheight(prevheight))

def new_width():
    return random.randint(0, int(WIDTH/20) - 5) + 5

def new_topheight(prevheight):
    while True:
        range = random.randint(-30, 30)
        if random.randint(0,1) > 0.5:
            range = -range
        if (prevheight + range) > HEIGHT * 0.25 and (prevheight + range) < HEIGHT * 0.75 - VGAP:
            break
    return prevheight + range

def fill():
    while (toprecs[-1].right < WIDTH):
        add_slice(toprecs[-1].bottom, toprecs[-1].right)

def add_slice(prevheight, prevright, width=None):
        newRect = new_toprect(prevheight, width)
        newRect.left = prevright
        toprecs.append(newRect)
        bottomRect = pygame.Rect(newRect.left, newRect.bottom + VGAP, newRect.width, HEIGHT - (newRect.bottom + VGAP))
        bottomrecs.append(bottomRect)

def trim_offscreen():
    while (toprecs[0].right < 0):
        toprecs.popleft()
    while (bottomrecs[0].right < 0):
        bottomrecs.popleft()

def flip():
    if speed == 0:
        return
    global rock_color, moveby, show_flip
    rock_color = 'green' if rock_color == 'red' else 'red'
    moveby = -moveby
    show_flip = True
    clock.schedule_unique(hide_flip, 1.0)
    next_flip = random.random() * 8 + 4
    clock.schedule_unique(flip, next_flip)

def hide_flip():
    global show_flip
    show_flip = False

def setup():
    global shiprect, toprecs, bottomrecs, speed, moveby, rock_color, show_flip
    toprecs = deque()
    bottomrecs = deque()
    speed = 3
    moveby = 2
    rock_color = 'red'
    show_flip = False
    add_slice(int(HEIGHT/3), 0, WIDTH)
    shipH = toprecs[0].bottom + int(VGAP/2)
    shiprect = pygame.Rect(0, 0, 20, 20)
    shiprect.center = (WIDTH/4, shipH)
    clock.schedule_interval(flip, 10.0)

def on_mouse_down():
    if speed != 0:
        return
    setup()

setup()
pgzrun.go()