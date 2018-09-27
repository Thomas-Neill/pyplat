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
        self.body.update(dt)
        if game.level.check_collision(self.body.rect) != Collision.Null:
            game.level.remove_entity(self)
        if self.body.rect.collides(game.player.body.rect):
            game.player.dead = True


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
        if self.spawn_timer > 0.5:
            self.spawn_timer -= 0.5
            delta = game.player.body.rect.center() - self.body.rect.center()
            game.level.add_entity(Bullet(self.body.rect.center(),delta*100/delta.magnitude()))
