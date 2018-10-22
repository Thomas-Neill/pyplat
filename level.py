import pygame
import pickle
import json
from rect import Rect
from vec import Vec
from functools import total_ordering

null,block_black,block_blue,block_red_kill,n_tiles = range(5)

LEVEL_H = 500
LEVEL_W = 500

@total_ordering
class Collision:
    Null = 0
    Hit = 2
    Kill = 1
    OOB_N = 3
    OOB_E = 4
    OOB_S = 5
    OOB_W = 6
    def __init__(self,type):
        self.type = type
        self.entity = None
    def __lt__(self,other):
        return self.type < other.type
    def __eq__(self,other):
        return self.type == other.type
    @staticmethod
    def with_entity(type,ent):
        result = Collision(type)
        result.entity = ent
        return result
    @staticmethod
    def is_oob(coll):
        return Collision.OOB_N <= coll <= Collision.OOB_W
collisionTypes = [Collision.Null,Collision.Hit,Collision.Hit,Collision.Kill]
def draw_tile(window,tile,rect):
    if tile == block_black:
        pygame.draw.rect(window,(0,0,0),rect.show())
    elif tile == block_blue:
        pygame.draw.rect(window,(0,0,255),rect.show())
    elif tile == block_red_kill:
        pygame.draw.rect(window,(255,0,0),rect.show())

class Level:
    def __init__(self):
        self.tiles = [[0 for i in range(25)] for j in range(25)]
        self.entities = []
    @staticmethod
    def load(filename):
        try:
            with open(filename,'rb') as f:
                result = pickle.load(f)
                with open(filename+".json") as f:
                    result.data = json.load(f)
                    result.transitions = {
                        Collision.OOB_N:result.data["trans_north"],
                        Collision.OOB_E:result.data["trans_east"],
                        Collision.OOB_S:result.data["trans_south"],
                        Collision.OOB_W:result.data["trans_west"]}
                    result.file = filename
                return result
        except:
            print(f"Bad filename: {filename}")
            raise
    def add_entity(self,ent):
        self.entities.append(ent)
    def remove_entity(self,ent):
        self.entities = [i for i in self.entities if i != ent]
    def draw(self,window):
        rect = Rect(Vec(0,0),20,20)
        for y in range(25):
            for x in range(25):
                draw_tile(window,self.tiles[x][y],rect)
                rect.pos.x += 20
            rect.pos.x = 0
            rect.pos.y += 20
        for ent in self.entities:
            ent.draw(window)
    def update(self,game,dt):
        for ent in self.entities:
            ent.update(game,dt)
    def level_collision(self,rect):
        results = []
        for point in rect.points():
            ix = int(point.x//20)
            iy = int(point.y//20)
            coll = None
            if iy < 0: coll = Collision.OOB_S
            elif ix >= 25: coll = Collision.OOB_E
            elif iy >= 25: coll = Collision.OOB_N
            elif ix < 0: coll = Collision.OOB_W
            else: coll = collisionTypes[self.tiles[ix][iy]]
            results.append(coll)
        result = Collision.Null
        for i in results:
            result = max(result,i)
        return Collision(result)
    def check_collision(self,rect):
        results = []
        for ent in self.entities:
            results.append(Collision.with_entity(ent.check_collision(rect),ent))
        result = self.level_collision(rect)
        for i in results:
            result = max(result,i)
        return result
