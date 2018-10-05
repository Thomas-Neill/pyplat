from body import *
from rect import *
from vec import *
from level import *

import pygame

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
            if coll != Collision.Null:
                game.level.remove_entity(self)
                return
    def check_collision(self,rect):
        if self.body.rect.collides(rect):
            return Collision.Kill
        return Collision.Null

class Turret:
    def __init__(self,x,y):
        self.spawn_timer = 0
        self.body = Body(Rect(Vec(x,y),20,20))
    @staticmethod
    def spawn(x,y):
        return Turret(int(x),int(y))
    def draw(self,window):
        pygame.draw.rect(window,(0,255,0),self.body.rect.show())
    def update(self,game,dt):
        self.spawn_timer += dt
        if self.spawn_timer > 0.1:
            self.spawn_timer -= 0.1
            delta = game.player.body.rect.center() - self.body.rect.center()
            game.level.add_entity(Bullet(self.body.rect.center(),delta*500/delta.magnitude()))
    def check_collision(self,rect):
        return Collision.Null

class Platform:
    def __init__(self,x,y,w,h):
        self.body = Body(Rect(Vec(x,y),w,h))
    @staticmethod
    def spawn(x,y,w,h):
        return Platform(int(x),int(y),int(w),int(h))
    def draw(self,window):
        pygame.draw.rect(window,(0,0,0),self.body.rect.show())
    def update(self,game,dt):
        pass
    def check_collision(self,rect):
        if self.body.rect.collides(rect):
            return Collision.Hit
        return Collision.Null
