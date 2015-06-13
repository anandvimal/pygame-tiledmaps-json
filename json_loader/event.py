__author__ = 'craig'

import pygame, sys
from controller import *
# code specific to running games on Android

'''
try:
    import android
except ImportError:
    android = None
'''
android = None

class Event():
    def __init__(self, initial):
        self.direction = "stop"
        self.initial = initial
        self.virtual_game_controller = GameController(initial)
        self.jump = False
        self.fall = False

    def update(self):
        # check for android pause event

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"
                elif event.key == pygame.K_SPACE:
                    self.jump = True
