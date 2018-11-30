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
        pygame.draw.rect(window,(255,0,0),self.body.rect.show())
    def update(self,game,dt):
        self.body.update(dt)
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
            self.bullet_v = Vec(0,300)
        elif direction == "east":
            self.bullet_v = Vec(300,0)
        elif direction == "south":
            self.bullet_v = Vec(0,-300)
        elif direction == "west":
            self.bullet_v = Vec(-300,0)
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
    def __init__(self,x,y,w,h,movement_sequence):
        self.body = Body(Rect(Vec(x,y),w,h))
        self.hit = False
        self.movement_timer = 0
        self.movement_pos = -1
        self.movement_sequence = movement_sequence
    @staticmethod
    def spawn(x,y,w,h,motions):
        motionSequence = []
        for i in motions.split(";"):
            data = list(map(int,i.split(",")))
            motionSequence.append((Vec(data[0],data[1]),data[2]))
        return MovingPlatform(int(x),int(y),int(w),int(h),motionSequence)
    def draw(self,window):
        pygame.draw.rect(window,(0,0,0),self.body.rect.show())
    def update(self,game,dt):
        if self.movement_timer <= 0:
            self.movement_pos += 1
            self.movement_pos %= len(self.movement_sequence)
            self.movement_timer = self.movement_sequence[self.movement_pos][1]
            self.body.v = self.movement_sequence[self.movement_pos][0]
        else:
            self.movement_timer -= dt
        self.body.begin_update()
        self.body.update(dt)
        if self.body.rect.collides(game.player.body.rect):
            self.body.reset_x()
            self.body.reset_y()
            self.body.linked_body = game.player.body
            self.body.update(dt)

    def check_collision(self,rect):
        if self.body.rect.collides(rect):
            return Collision.Hit
        return Collision.Null


class PeriodicPlatform:
    @staticmethod
    def spawn(x,y,w,h,delta,period):
        delta = delta.split(",")
        delta = Vec(int(delta[0]),int(delta[1]))
        period = int(period)
        movement = [(delta/period,period),(-delta/period,period)]
        return MovingPlatform(int(x),int(y),int(w),int(h),movement)
