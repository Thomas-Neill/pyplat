import pygame
import math
from pygame.locals import *
from level import *

class Player:
    def __init__(self,body):
        self.body = body
        self.jump_timer = 0
        self.can_jump = False
        self.oob_dir = None
        self.dead = False
    def draw(self,window):
        color = (125,125,125)
        pygame.draw.rect(window,color,self.body.rect.show())
    def check_keys(self):
        if pygame.key.get_pressed()[K_LEFT]:
            self.body.v.x -= 200
        elif pygame.key.get_pressed()[K_RIGHT]:
            self.body.v.x += 200
    def keydown(self,key):
        if key == K_LEFT:
            self.body.v.x -= 200
        elif key == K_RIGHT:
            self.body.v.x += 200
        elif key == K_SPACE and self.can_jump:
            self.body.v.y = 250
            self.jump_timer = 12
            self.can_jump = False
    def keyup(self,key):
        if key == K_LEFT:
            self.body.v.x += 200
        elif key == K_RIGHT:
            self.body.v.x -= 200
        elif key == K_SPACE:
            self.jump_timer = 0
    def wrap(self):
        if self.oob_dir == Collision.OOB_S:
            self.body.rect.pos.y = 500 - self.body.rect.h - 1
        elif self.oob_dir == Collision.OOB_N:
            self.body.rect.pos.y = 0
        elif self.oob_dir == Collision.OOB_E:
            self.body.rect.pos.x = 0
        elif self.oob_dir == Collision.OOB_W:
            self.body.rect.pos.x = 500 - self.body.rect.w - 1
    def update(self,game,dt):
        self.body.begin_update()
        self.can_jump = False
        for i in range(5):
            self.body.update_y(dt/5)
            coll = game.level.check_collision(self.body.rect)
            if coll != Collision.Null:
                if Collision.is_oob(coll):
                    self.oob_dir = coll
                else:
                    if coll == Collision.Kill:
                        self.dead = True
                    while game.level.check_collision(self.body.rect) != Collision.Null:
                        self.body.rect.pos.y -= math.copysign(1,self.body.v.y)
                    if self.body.v.y < 0:
                        self.can_jump = True
                    self.body.v.y = 0
                break
        if self.jump_timer > 0:
            self.jump_timer -= 1
            self.body.v.y += 0
            self.body.v.y = min(self.body.v.y,275)
        else:
            self.body.v.y -= 50
            self.body.v.y = max(self.body.v.y,-350)
        for i in range(10):
            self.body.update_x(dt/10)
            coll = game.level.check_collision(self.body.rect)
            if coll != Collision.Null:
                if Collision.is_oob(coll):
                    self.oob_dir = coll
                self.body.reset_x()
