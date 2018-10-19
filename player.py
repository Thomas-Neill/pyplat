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
        self.body.v.x = 0
        if pygame.key.get_pressed()[K_LEFT]:
            self.body.v.x = -200
        elif pygame.key.get_pressed()[K_RIGHT]:
            self.body.v.x = 200
    def keydown(self,key):
        if key == K_LEFT:
            self.body.v.x -= 200
        elif key == K_RIGHT:
            self.body.v.x += 200
        elif key == K_SPACE and self.can_jump:
            self.body.v.y = 210
            self.jump_timer = 0.2
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
    def check_collision(self,game):
        return game.level.check_collision(self.body.rect)
    def handle_collision(self,coll):
        if Collision.is_oob(coll):
            self.oob_dir = coll
        if coll == Collision.Kill:
            self.dead = True
    def update(self,game,dt):
        self.can_jump = False
        for i in range(10):
            self.update_step(game,dt/10)
    def update_step(self,game,dt):
        self.body.begin_update()
        if self.jump_timer > 0:
            self.jump_timer -= dt
        else:
            self.body.v.y -= 1000*dt
            self.body.v.y = max(self.body.v.y,-350)
        self.body.update_y(dt)
        coll = self.check_collision(game)
        if coll != Collision.Null:
            self.handle_collision(coll)
            self.body.reset_y()
            if self.body.v.y < 0:
                self.can_jump = True
            self.body.v.y = 0
        # UPDATE X
        self.body.update_x(dt)
        coll = self.check_collision(game)
        if coll != Collision.Null:
            self.handle_collision(coll)
            self.body.reset_x()
