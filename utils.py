import pygame
import numpy as np
from point import P

"""
Utilities: Contains global settings and constants
"""

############## Settings ##############
NUM_TEAM = 7
PLAYER_SPEED = 3
BALL_SPEED = 5
W = 1024
H = 568
BALL_RADIUS = 10
BALL_CENTER = P(BALL_RADIUS, BALL_RADIUS)
BALL_OFFSET = P(3, 1.5)
PLAYER_RADIUS = 30
PLAYER_CENTER = P(PLAYER_RADIUS, PLAYER_RADIUS)
GOAL_POS = [0.3,0.7] # goalpost positions in percentage
LINE_WIDTH = 2
ASSET_DIR = './assets/' # Path to where the images are stored
ANIM_NUM = 7 # Number of images used for running animation
WALK_DELAY = 3 # Change walking sprite after X presses
######################################



############## Functions ##############
def recolor(surface, color=(255,128,0)):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            val = surface.get_at((x, y))
            surface.set_at((x, y), pygame.Color(r, g, b, val[3]))

############## Images ##############
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(ASSET_DIR + "field.png"), (W, H))
FOOTBALL_IMG = pygame.transform.scale(pygame.image.load(ASSET_DIR + "football.png"), (2*BALL_RADIUS, 2*BALL_RADIUS))
RUN = {
    1: {
        'L': { i: pygame.transform.scale(pygame.image.load(ASSET_DIR + f'running/l{i}.png'), (2*PLAYER_RADIUS, 2*PLAYER_RADIUS)) for i in range(7) },
        'R': { i: pygame.transform.scale(pygame.image.load(ASSET_DIR + f'running/r{i}.png'), (2*PLAYER_RADIUS, 2*PLAYER_RADIUS)) for i in range(7) },
    },
    2: {
        'L': { i: pygame.transform.scale(pygame.image.load(ASSET_DIR + f'running/l{i}.png'), (2*PLAYER_RADIUS, 2*PLAYER_RADIUS)) for i in range(7) },
        'R': { i: pygame.transform.scale(pygame.image.load(ASSET_DIR + f'running/r{i}.png'), (2*PLAYER_RADIUS, 2*PLAYER_RADIUS)) for i in range(7) },
    },
}
######################################



############## Custom types ##############

# actions that can be performed by a plyer at any given time
ACT = { 'NOTHING': 0,
        'MOVE_U': (0,-1), 'MOVE_D': (0,1), 'MOVE_L': (-1,0), 'MOVE_R': (1,0),
        'SHOOT_Q': (-1,-1), 'SHOOT_W': (0,-1), 'SHOOT_E': (1,-1), 'SHOOT_A': (-1,0),
        'SHOOT_D': (1,0), 'SHOOT_Z': (-1,1), 'SHOOT_X': (0,1), 'SHOOT_C': (1,1) }

# Possible team formations
FORM = {
    'default-right': [P(50,H//2), P(W//4,H//5), P(W//4, H//2), P(W//4, 4*H//5), P(W//2,H//3), P(W//2, 2*H//3), P(3*W//4,H//2)],
    'default-left': [P(W-50,H//2), P(3*W//4,H//5), P(3*W//4, H//2), P(3*W//4, 4*H//5), P(W//2,H//3), P(W//2, 2*H//3), P(W//4,H//2)],
}

#pl_type = { 'GK': 0, 'DEF': 1, 'MID': 2, 'ATK': 3 }
######################################
