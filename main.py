#!/usr/bin/env python3
import pygame
from pygame.locals import *
from rect import Rect
from vec import Vec
from body import Body
from player import Player
from level import *
import pickle

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((500,500))
        self.clock = pygame.time.Clock()

        self.player = Player(Body(Rect(Vec(30,479),20,20)))
        self.load_level("test_level.lvl")
        self.respawn_timer = 0
    def load_level(self,lvl):
        self.level = Level.load("levels/"+lvl)
        self.level_save = pickle.dumps(self.level)
        self.player_save = pickle.dumps(self.player)
    def respawn_player(self):
        self.player = pickle.loads(self.player_save)
        self.level = pickle.loads(self.level_save)
        self.player.check_keys()
    def go(self):
        t = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    self.player.keydown(event.key)
                elif event.type == KEYUP:
                    self.player.keyup(event.key)

            dt = (pygame.time.get_ticks()-t)/1000
            t = pygame.time.get_ticks()

            if self.player.dead:
                if self.respawn_timer < .5:
                    self.respawn_timer += dt
                else:
                    self.respawn_timer = 0
                    self.respawn_player()
            else:
                self.player.update(self,dt)

            self.level.update(self,dt)
            if self.player.oob_dir != None:
                result = self.level.transitions[self.player.oob_dir]
                if result == "kill":
                    self.kill_player()
                elif result == "wrap":
                    self.player.wrap()
                elif result == "block":
                    pass
                elif "goto" in result:
                    to = result.split()[1]
                    self.player.wrap()
                    self.load_level(to)
                self.player.oob_dir = None

            self.window.fill((255,255,255))
            self.level.draw(self.window)
            if not self.player.dead:
                self.player.draw(self.window)
            pygame.display.update()

            self.clock.tick(45)
Game().go()
