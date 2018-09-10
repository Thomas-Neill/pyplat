import pygame
from pygame.locals import *
from rect import Rect
from vec import Vec
from body import Body
from player import Player
from level import *

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((500,500))
        self.clock = pygame.time.Clock()

        self.player = Player(Body(Rect(Vec(10,479),20,20)))
        self.level = Level.load("levels/test_level.lvl")
    def go(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    self.player.keydown(event.key)
                elif event.type == KEYUP:
                    self.player.keyup(event.key)

            self.player.update(self,1/60)

            self.window.fill((255,255,255))
            self.level.draw(self.window)
            self.player.draw(self.window)
            pygame.display.update()

            self.clock.tick(60)
Game().go()
