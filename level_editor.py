import pygame
from pygame.locals import *

import pickle
import sys
import os
import json

from level import *
from rect import Rect
from vec import Vec

file = (len(sys.argv)>=2 and sys.argv[1]) or input("Filename? > ")

pygame.init()
window = pygame.display.set_mode((500,500))
pygame.mouse.set_visible(False)
if os.path.exists(file):
    with open(file,'rb') as f:
        level = pickle.load(f)
else:
    level = Level()
try:
    with open(file+".json",'rb') as f:
        data = json.load(f)
except:
    print("JSON file required to edit level.")
    raise

tile_place = 0

while True:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                tile_place -= 1
                if tile_place == 0:
                    tile_place -= 1
                tile_place %= n_tiles
            elif event.button == 5:
                tile_place += 1
                tile_place %= n_tiles
                if tile_place == 0:
                    tile_place += 1
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            quit()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_TAB):
            with open(file,'wb') as f:
                pickle.dump(level,f)
                quit()
    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
        tx = (pygame.mouse.get_pos()[0])//20
        ty = (500-pygame.mouse.get_pos()[1])//20
        if ty < 25:
            if pygame.mouse.get_pressed()[0]:
                level.tiles[tx][ty] = tile_place
            else:
                level.tiles[tx][ty] = null
    window.fill((255,255,255))
    level.draw(window)
    rect = Rect(Vec(pygame.mouse.get_pos()[0],500-pygame.mouse.get_pos()[1]),20,20)
    draw_tile(window,tile_place,rect)
    pygame.draw.rect(window,(125,125,125),rect.show(),1)
    rect.w = 2
    rect.h = 2
    pygame.draw.rect(window,(255,0,0),rect.show())

    pygame.display.update()
