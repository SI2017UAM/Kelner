import pygame as pg
from settings import *

# zwraca prosto
def collide_hit_rect(one, two):
    # zwraca true lub false (0/1)
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    # ustawiamy polozenie grafiki obiektu (tylko rect!!, czyli grafikę)
    def apply(self, entity):
        #print (self.camera.topleft)
        #self.camera.topleft to wektor (x,y)
        return entity.rect.move(self.camera.topleft)

    # update parametrów kamry na podstawie celu (target)
    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
