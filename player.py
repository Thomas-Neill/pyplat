import pygame
from pygame.locals import *
from level import *

class Player:
    def __init__(self,body):
        self.body = body
        self.jump_timer = 0
    def draw(self,window):
        pygame.draw.rect(window,(255,0,0),self.body.rect.show())
    def keydown(self,key):
        if key == K_LEFT:
            self.body.v.x -= 100
        elif key == K_RIGHT:
            self.body.v.x += 100
        elif key == K_SPACE and self.can_jump:
            self.body.v.y = 100
            self.jump_timer = 12
            self.can_jump = False
    def keyup(self,key):
        if key == K_LEFT:
            self.body.v.x += 100
        elif key == K_RIGHT:
            self.body.v.x -= 100
        elif key == K_SPACE:
            self.jump_timer = 0
    def update(self,game,dt):
        self.body.begin_update()
        for i in range(20):
            self.body.update_y(dt/20)
            if game.level.check_collision(self.body.rect) != Collision.Null:
                self.body.reset_y()
                if self.body.v.y < 0:
                    self.can_jump = True
                self.body.v.y = 0
        if self.jump_timer > 0:
            self.jump_timer -= 1
            self.body.v.y += 15
            self.body.v.y = min(self.body.v.y,325)
        else:
            self.body.v.y -= 25
            self.body.v.y = max(self.body.v.y,-300)
        for i in range(10):
            self.body.update_x(dt/10)
            if game.level.check_collision(self.body.rect) != Collision.Null:
                self.body.reset_x()
