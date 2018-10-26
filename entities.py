from body import *
from rect import *
from vec import *
from level import *

import pygame
import math

'''
A 'entity' is expected to implement:

static spawn(x,y, (determined by class)) -> Cls

draw(window)

update(game,dt)

check_collision(rect)

'''


class Bullet:
    def __init__(self,pos,v):
        self.body = Body(Rect(pos,5,5))
        self.body.v = v
    @staticmethod
    def spawn(x,y,dx,dy):
        return Bullet(Vec(int(x),int(y)),Vec(int(dx),int(dy)))
    def draw(self,window):
        pygame.draw.rect(window,(0,0,0),self.body.rect.show())
    def update(self,game,dt):
        for i in range(10):
            self.body.update(dt/10)
            coll = game.level.check_collision(self.body.rect)
            if coll.type != Collision.Null:
                game.level.remove_entity(self)
                return
    def check_collision(self,rect):
        if self.body.rect.collides(rect):
            return Collision.Kill
        return Collision.Null

class Turret:
    def __init__(self,x,y,direction):
        self.spawn_timer = 0
        self.body = Body(Rect(Vec(x,y),20,20))
        if direction == "north":
            self.bullet_v = Vec(0,500)
        elif direction == "east":
            self.bullet_v = Vec(500,0)
        elif direction == "south":
            self.bullet_v = Vec(0,-500)
        elif direction == "west":
            self.bullet_v = Vec(-500,0)
    @staticmethod
    def spawn(x,y,direction):
        return Turret(int(x),int(y),direction)
    def draw(self,window):
        pygame.draw.rect(window,(0,255,0),self.body.rect.show())
    def update(self,game,dt):
        self.spawn_timer += dt
        if self.spawn_timer > .5:
            self.spawn_timer -= .5
            game.level.add_entity(Bullet(self.body.rect.center(),self.bullet_v))
    def check_collision(self,rect):
        return Collision.Null

class MovingPlatform:
    def __init__(self,x,y,w,h):
        self.body = Body(Rect(Vec(x,y),w,h))
        self.body.v.x = 100
        self.hit = False
    @staticmethod
    def spawn(x,y,w,h):
        return MovingPlatform(int(x),int(y),int(w),int(h))
    def draw(self,window):
        pygame.draw.rect(window,(0,0,0),self.body.rect.show())
    def update(self,game,dt):
        '''self.body.update_x(dt)
        while self.body.rect.collides(game.player.body.rect):
            game.player.body.rect.pos.x += math.copysign(1,self.body.v.x)
        if self.body.rect.pos.x > 300:
            self.body.v.x = -100
        elif self.body.rect.pos.x < 100:
            self.body.v.x = 100'''
        self.body.v.x = 0
        self.body.update_y(dt)
        if self.body.rect.pos.y > 300:
            self.body.v.y = -100
        elif self.body.rect.pos.y < 50:
            self.body.v.y = 100

    def check_collision(self,rect):
        if self.body.rect.collides(rect):
            return Collision.Hit
        return Collision.Null
