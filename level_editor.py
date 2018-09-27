import pygame
from pygame.locals import *

import pickle
import sys
import os
import shutil
import json
import threading

from level import *
from rect import Rect
from vec import Vec
from entities import *

file = "levels/"+(len(sys.argv)>=2 and sys.argv[1]) or input("Filename? > ")

pygame.init()
window = pygame.display.set_mode((500,500))
pygame.mouse.set_visible(False)

level = None
data = None

def open_file():
    global file,level,data
    if os.path.exists(file):
        with open(file,'rb') as f:
            level = pickle.load(f)
    else:
        level = Level()
        shutil.copyfile("levels/default.json",file+".json")
    with open(file+".json",'rb') as f:
        data = json.load(f)

def save_file():
    with open(file,'wb') as f:
        pickle.dump(level,f)
    with open(file+".json",'w') as f:
        json.dump(data,f)

open_file()

tile_place = 1

def processIO():
    print("Command syntax: ")
    print("modify_data [attribute] = \"[new value]\"")
    print("spawn_entity [entity class] [argument list]")
    print("del_ents")
    while True:
        command = input("> ")
        if "modify_data" in command:
            attribute = command.split(" ")[1]
            nv = command.split("\"")[1]
            data[attribute] = nv
        elif "spawn_entity" in command:
            x = pygame.mouse.get_pos()[0]
            y = 500-pygame.mouse.get_pos()[1]
            args = command.split(" ")[2:]
            level.add_entity(eval(command.split()[1]).spawn(x,y,*args))
        elif "del_ents" in command:
            level.entities = []
ioThread = threading.Thread(target=processIO,args=())
ioThread.daemon = True
ioThread.start()

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
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            save_file()
            quit()
        if event.type == KEYDOWN:
            nf = None
            if event.key == K_UP:
                nf = data["trans_north"]
            elif event.key == K_RIGHT:
                nf = data["trans_east"]
            elif event.key == K_LEFT:
                nf = data["trans_west"]
            elif event.key == K_DOWN:
                nf = data["trans_south"]
            if nf != None:
                if "goto" in nf:
                    nf = nf.split(" ")[1]
                    save_file()
                    file = "levels/"+nf
                    open_file()
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
