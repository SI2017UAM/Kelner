import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN=(126, 95, 0)

# game settings
# ustawienia dla okna gry, podzielne przez TILESIZE
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
# jak wiele razy na sekundę robimy update na obiektach w grze
FPS = 60

TITLE = "Kelner"
BGCOLOR = BROWN

# wielkosc bloku
TILESIZE = 32
# wielkosc mapy w blokach
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 250.0
PLAYER_IMG = 'hitman1_hold.png'
#PLAYER_HIT_RECT = pg.Rect(0, 0, 60, 90)
PLAYER_HIT_RECT = pg.Rect(0, 0, 38, 38)

MOB_SPEED = 200.0
MOB_ROT_SPEED = 200.0
SEEK_FORCE = 0.8
MOB_IMG = 'manOld_hold.png'
#PLAYER_HIT_RECT = pg.Rect(0, 0, 60, 90)
MOB_HIT_RECT = pg.Rect(0, 0, 1, 1)

#Wall settings
WALL_IMG='block_05.png'
#Kitchen settings
KITCHEN_IMG='crate_24.png'
#Table settings
TABLE_IMG='crate_12.png'
