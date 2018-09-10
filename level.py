import pygame
import pickle
from rect import Rect
from vec import Vec
null,block_black,block_blue,n_tiles = range(4)

class Collision:
    Null = 0
    Hit = 1
    OOB = 2
collisionTypes = [Collision.Null,Collision.Hit,Collision.Hit]
def draw_tile(window,tile,rect):
    if tile == block_black:
        pygame.draw.rect(window,(0,0,0),rect.show())
    elif tile == block_blue:
        pygame.draw.rect(window,(0,0,255),rect.show())
class Level:
    def __init__(self):
        self.tiles = [[0 for i in range(25)] for j in range(25)]
    @staticmethod
    def load(filename):
        with open(filename,'rb') as f:
            return pickle.load(f)
    def draw(self,window):
        rect = Rect(Vec(0,0),20,20)
        for y in range(25):
            for x in range(25):
                draw_tile(window,self.tiles[x][y],rect)
                rect.pos.x += 20
            rect.pos.x = 0
            rect.pos.y += 20
    def check_collision(self,rect):
        for i in rect.points():
            if i.x < 0 or i.x >= 500 or i.y < 0 or i.y >=500:
                return Collision.OOB
        results = [self.tiles[int(point.x//20)][int(point.y//20)] for point in rect.points()]
        result = Collision.Null
        for i in results:
            result = result or i
        return result
