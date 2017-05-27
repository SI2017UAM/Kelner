import pygame as pg
import random
import sys
import csv

from os import path
import numpy as np
from settings import *
from sprites import *
from tilemap import *
from collections import deque
vec = pg.math.Vector2


class OrderRequest(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups=game.order_agents
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        self.status=0
        self.groups=self.game.order_agents
        self.cords=vec(x,y)
        self.order_list=[]
        self.food_ammount=np.random.poisson(2,1)+1
        if (self.food_ammount > 5):
            self.food_ammount-=1
        self.menu_orders=np.random.choice(self.game.menu_size,self.food_ammount,0)
        self.create_order()
        self.game.walls_obj[x,y][1].image = self.game.table_img[1]
        #print(self.order_list)
    def create_order(self):
        for i in self.menu_orders:
            foodname=self.game.menu[i][0]
            preptime=np.random.randint(int(self.game.menu[i][1]),int(self.game.menu[i][2])+1)
            difficulty=np.random.randint(int(self.game.menu[i][3]),int(self.game.menu[i][4])+1)
            price=np.random.randint(int(self.game.menu[i][5]),int(self.game.menu[i][6])+1)
            self.order_list.append([foodname,preptime,difficulty,price])
class ClientAgent(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups=game.order_agents
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        self.spawn_timer=np.random.poisson(1,1)
        self.timer_sec=pg.time.get_ticks()//1000
        self.last_spawned=self.timer_sec
        self.ammount_of_taken_tables=0
        self.free_tables=self.game.tables_coord
        self.order_agents={}
        self.bonus=0
    def tableeFree(self):
        self.last_spawned=pg.time.get_ticks()//1000
        #jak duzo stolikow na raz staje sie znowu aktywnym mozemy sie tutaj zatkac, stad bonus
        self.bonus+=1
    def update(self):
        #print(pg.time.get_ticks()//1000)
        self.timer_sec=pg.time.get_ticks()//1000
        #print(self.spawn_timer,self.timer_sec,self.last_spawned)
        if (len(self.free_tables)>0 and self.timer_sec-self.spawn_timer + self.bonus>self.last_spawned):
            self.last_spawned=self.timer_sec
            self.spawn_timer=np.random.poisson(1,1)
            self.bonus=0
            shuffled_tables=np.random.permutation(self.free_tables)

            self.free_tables=shuffled_tables
            #print(self.free_tables)
            new_coord=self.free_tables[-1]
            self.order_agents[new_coord[0],new_coord[1]]=OrderRequest(self.game,new_coord[0],new_coord[1])
            self.ammount_of_taken_tables+=1
            if (len(self.free_tables)>1):
                self.free_tables=self.free_tables[:-1]
            else:
                self.free_tables=[]
            print("from main ",new_coord,type(new_coord))
    def print_orders(self):
        for key,value in self.order_agents.items():
            print("cord->",key," order->",value.order_list)
class Game:
    # każdy obiekt musi miec funkcję _init__
    def __init__(self):
        #inicjujemy pygame
        pg.init()
        pg.mixer.init()
        # ustalamy okno gry
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        #create an object to help track time
        self.clock = pg.time.Clock()
        self.load_data()
        self.connections = [vec(1,0),vec(-1,0),vec(0,1),vec(0,-1),vec(1,1),vec(-1,1),vec(-1,-1),vec(1,-1)]
        self.weights = {}
        self.start = vec(5,5)
        self.goal = vec(10,5)
        self.path = {}
    def load_data(self):
        game_folder = path.dirname("__file__")
        img_folder = path.join(game_folder, 'imgs')
        txt_folder = path.join(game_folder, 'txt_files')
        self.map = Map(path.join(txt_folder, 'map2.txt'))
        #txt_file=open(path.join(txt_folder,"menu.txt"))
        #self.menu=txt_file.read().split('\n')
        self.menu=[]
        with open(path.join(txt_folder,"menu.csv")) as menu_file:
            reader = csv.reader(menu_file,delimiter=";")
            print(next(reader))
            for row in reader:
                self.menu.append(row)
            print(self.menu)
        self.menu_size=len(self.menu)
        ## load(fileobj, namehint=””) -> Surface, load zwraca obiekt pygame Surface
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        self.kitchen_img = pg.image.load(path.join(img_folder, KITCHEN_IMG)).convert_alpha()
        self.kitchen_img  = pg.transform.scale(self.kitchen_img, (TILESIZE,TILESIZE))
        self.table_img = {}

        self.table_img[0] = pg.image.load(path.join(img_folder, TABLE_IMG0)).convert_alpha()
        self.table_img[0] = pg.transform.scale(self.table_img[0], (TILESIZE,TILESIZE))
        self.table_img[1] = pg.image.load(path.join(img_folder, TABLE_IMG1)).convert_alpha()
        self.table_img[1] = pg.transform.scale(self.table_img[1], (TILESIZE,TILESIZE))
        self.table_img[2] = pg.image.load(path.join(img_folder, TABLE_IMG2)).convert_alpha()
        self.table_img[2] = pg.transform.scale(self.table_img[2], (TILESIZE,TILESIZE))
        self.table_img[3] = pg.image.load(path.join(img_folder, TABLE_IMG3)).convert_alpha()
        self.table_img[3] = pg.transform.scale(self.table_img[3], (TILESIZE,TILESIZE))
        self.table_img[4] = pg.image.load(path.join(img_folder, TABLE_IMG4)).convert_alpha()
        self.table_img[4] = pg.transform.scale(self.table_img[4], (TILESIZE,TILESIZE))
        self.table_img[5] = pg.image.load(path.join(img_folder, TABLE_IMG5)).convert_alpha()
        self.table_img[5] = pg.transform.scale(self.table_img[5], (TILESIZE,TILESIZE))
        ##
        self.home_img = pg.image.load(path.join(img_folder, 'home1.png')).convert_alpha()
        self.home_img = pg.transform.scale(self.home_img, (TILESIZE, TILESIZE))
        self.home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
        self.cross_img = pg.image.load(path.join(img_folder, 'target.png')).convert_alpha()
        self.cross_img = pg.transform.scale(self.cross_img, (TILESIZE, TILESIZE))
        self.cross_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
        self.arrows={}
        self.arrow_img = pg.image.load(path.join(img_folder, 'arrowRight.png')).convert_alpha()
        self.arrow_img = pg.transform.scale(self.arrow_img, (TILESIZE-5, TILESIZE-5))
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1),(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            self.arrows[dir] = pg.transform.rotate(self.arrow_img, vec(dir).angle_to(vec(1, 0)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.order_agents=pg.sprite.Group()
        # DO PRZECHOWYWANIA OBIEKTOW LEPIEJ UZYC MAPY/TABLICY HASHUJACEJ, (x,y,OBIEKT)
        self.walls_obj={}
        self.tables_coord=[]
        # >enumerate(['a','b','c'])
        # [(0,'a'), (1,'b'), (2,'c')]
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.walls_obj[col,row]=('wall', Wall(self, col, row))
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    self.mob=Mob(self, col, row)
                if tile == 'k':
                    self.walls_obj[col,row]=('kitchen', Kitchen(self, col, row))
                    self.kitchen_pos=vec(col,row)
                    self.kitchen=self.walls_obj[col,row][1]
                if tile == 't':
                    self.tables_coord.append([col,row])
                    self.walls_obj[col,row]=('table', Table(self, col, row))
        self.camera = Camera(self.map.width, self.map.height)
        self.client_agent=ClientAgent(self)
        #self.find_neighbors(vec(0,0))
        #self.find_neighbors(vec(0,1))
        #self.find_neighbors(vec(1,1))
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            # pygame.time.Clock.tick(framerate=0) milliseconds
            # ustalamy jak szybko ma powtarzac się cała pętla
            # This method should be called once per frame.
            # It will compute how many milliseconds have passed since the previous call.
            self.dt = self.clock.tick(FPS) / 1000.0
            #dt ma wartosc okolo 0.017 (1/6) przy 60 FPSach
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # updatujemy sprite'y z grupy all_sprites
        self.order_agents.update()
        self.all_sprites.update()
        #updatujemy polozenie kamery na pozycję gracza
        #self.camera.update(self.player)
        self.camera.update(self.mob)
        self.start = vec(self.mob.pos // TILESIZE)
        #self.startPOS = vec(self.mob.pos / TILESIZE)
    # tworzy siatkę na ekranie
    def draw_grid(self):
        # line(Surface, color, start_pos, end_pos, width=1)
        # linie pionowe
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        # linie poziome
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        #*double buffering, pokazujemy nowe, zaktualizowane obiekty
        #
        # JEzeli start znajduje sie
        if (self.start!=self.goal):
            current = self.start + self.path[vec2int(self.start)]
            while current != self.goal:
                x = current.x * TILESIZE + TILESIZE / 2
                y = current.y * TILESIZE + TILESIZE / 2
                img = self.arrows[vec2int(self.path[(current.x, current.y)])]
                r = img.get_rect(center=(x, y))
                self.screen.blit(img, r.move(self.camera.camera.topleft))
                # find next in path
                current = current + self.path[vec2int(current)]
        self.start_center = (self.goal.x * TILESIZE + TILESIZE / 2, self.goal.y * TILESIZE + TILESIZE / 2)
        self.screen.blit(self.home_img, self.home_img.get_rect(center=self.start_center).move(self.camera.camera.topleft))
        #self.goal_center = (self.startPOS.x * TILESIZE + TILESIZE / 2, self.startPOS.y * TILESIZE + TILESIZE / 2)
        #self.screen.blit(self.cross_img, self.cross_img.get_rect(center=self.goal_center).move(self.camera.camera.topleft))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #wyjście z gry
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    #równieżwyjście z gry
                    self.quit()
                if event.key == pg.K_m:
                    self.client_agent.print_orders()
            if event.type == pg.MOUSEBUTTONDOWN:
                mpos=(vec(pg.mouse.get_pos()) - self.camera.camera.topleft) // TILESIZE
                #mpos-=self.camera.camera.topleft
                if event.button == 1:#left
                    self.goal = mpos
                    self.path = a_star_search(self,self.goal,self.start)
                if event.button == 3:#right
                    #self.start = mpos
                    pass

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14
    def show_start_screen(self):
        #game start screen
        pass

    def show_go_screen(self):
        #game over screen
        pass

    def in_bounds(self, node):
        return 0<= node.x < self.map.tilewidth and 0 <= node.y < self.map.tileheight

    def passable(self,node):
        return vec2int(node) not in self.walls_obj

    def find_neighbors (self, node):
        neighbors = [node + connection for connection in self.connections]
        #if (node.x + node.y) % 2:
        #    neighbors.reverse()
        neighbors=filter(self.in_bounds, neighbors)
        neighbors=filter(self.passable, neighbors)
        return neighbors
def vec2int(v):
    return (int(v.x), int(v.y))


# create the game object
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.path = a_star_search(g,g.goal,g.start)
    #print(g.path)
    #vec(self.mob.pos/TILESIZE)
    g.run()
    g.show_go_screen()
