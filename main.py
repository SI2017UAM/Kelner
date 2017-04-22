import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.connections = [vec(1,0),vec(-1,0),vec(0,1),vec(0,-1)]
        self.weights = {}
    def load_data(self):
        game_folder = path.dirname("__file__")
        img_folder = path.join(game_folder, 'imgs')
        self.map = Map(path.join(game_folder, 'map1.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        self.kitchen_img = pg.image.load(path.join(img_folder, KITCHEN_IMG)).convert_alpha()
        self.kitchen_img  = pg.transform.scale(self.kitchen_img, (TILESIZE,TILESIZE))
        self.table_img = pg.image.load(path.join(img_folder, TABLE_IMG)).convert_alpha()
        self.table_img = pg.transform.scale(self.table_img, (TILESIZE,TILESIZE))
    def wall_existence_check(x,y,self):
        for wall in self.walls:
            if wall.x==x and wall.y==y:
                return True,wall
        return False
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.walls_cords=[]
        self.table_cords=[]
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                    self.walls_cords.append([col,row])
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'k':
                    Kitchen(self, col, row)
                    self.kitchen_pos=vec(col,row)*TILESIZE
                if tile == 't':
                    Table(self, col, row)
                    self.table_cords.append([col,row])
        self.camera = Camera(self.map.width, self.map.height)
        #self.find_neighbors(vec(0,0))
        #self.find_neighbors(vec(0,1))
        #self.find_neighbors(vec(1,1))
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()
    def in_bounds(self, node):
        return 0<= node.x < WIDTH/TILESIZE and 0 <= node.y < HEIGHT/TILESIZE

    def passable(self,node):
        return node not in self.walls_cords

    def find_neighbors (self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors=filter(self.in_bounds, neighbors)
        neighbors=filter(self.passable, neighbors)
        #print(list(neighbors))
        return neighbors
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mpos=vec(pg.mouse.get_pos())// TILESIZE
                if event.button == 1:#left
                    pass
    def cost(self, from_node, to_node):
        if (to_node - from_node).length_squared()==1:
            return self.weights.get(to_node,0)+10
        else:
            return self.weights.get(to_node,0)+14
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
