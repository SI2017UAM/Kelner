import pygame as pg
import sys
import heapq
from os import path
from settings import *
from sprites import *
from tilemap import *
from collections import deque
vec = pg.math.Vector2

class PriorityQueue:
    def __init__(self):
        self.nodes = []
    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost,node))
    def get(self):
        return heapq.heappop(self.nodes)[1]
    def empty(self):
        return len(self.nodes)==0
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
        self.goal = vec(20,20)
        self.path = {}

    def load_data(self):
        game_folder = path.dirname("__file__")
        img_folder = path.join(game_folder, 'imgs')
        self.map = Map(path.join(game_folder, 'map1.txt'))
        ## load(fileobj, namehint=””) -> Surface, load zwraca obiekt pygame Surface
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        self.kitchen_img = pg.image.load(path.join(img_folder, KITCHEN_IMG)).convert_alpha()
        self.kitchen_img  = pg.transform.scale(self.kitchen_img, (TILESIZE,TILESIZE))
        self.table_img = pg.image.load(path.join(img_folder, TABLE_IMG)).convert_alpha()
        #pygame.transform.scale() :: (Surface, (width, height), DestSurface = None) -> Surface
        self.table_img = pg.transform.scale(self.table_img, (TILESIZE,TILESIZE))
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
        # DO PRZECHOWYWANIA OBIEKTOW LEPIEJ UZYC MAPY/TABLICY HASHUJACEJ, (x,y,OBIEKT)
        self.walls_obj={}
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
                    self.kitchen_pos=vec(col,row)*TILESIZE
                if tile == 't':
                    self.walls_obj[col,row]=('table', Table(self, col, row))
        self.camera = Camera(self.map.width, self.map.height)
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
        self.all_sprites.update()
        #updatujemy polozenie kamery na pozycję gracza
        #self.camera.update(self.player)
        self.camera.update(self.mob)
        self.start = vec(self.mob.pos // TILESIZE)
        self.startPOS = vec(self.mob.pos / TILESIZE)
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
        self.draw_grid()
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
        self.goal_center = (self.startPOS.x * TILESIZE + TILESIZE / 2, self.startPOS.y * TILESIZE + TILESIZE / 2)
        self.screen.blit(self.cross_img, self.cross_img.get_rect(center=self.goal_center).move(self.camera.camera.topleft))
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

def bfs(graph, start, end):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vec2int(start)] = None
    while len(frontier) > 0 :
        current = frontier.popleft()
        if current==end:
            break
        for next in graph.find_neighbors(current):
            if vec2int(next) not in path:
                frontier.append(next)
                path[vec2int(next)]=current - next
    return path
def heuristic(node1,node2):
    #manhattan distance
    return ((abs(node1.x-node2.x)+ abs(node1.y-node2.y)))*10
def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        #dzieki zakomentowaniu robimy path dla calej planszy, dzieki czemu
        #mozemy rysowac strzalki gdziekolwiek chcemy, a nie tylko w miejscach ktore odwiedzilismy
        #if current == end:
        #    break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path

def a_star_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        #dzieki zakomentowaniu robimy path dla calej planszy, dzieki czemu
        #mozemy rysowac strzalki gdziekolwiek chcemy, a nie tylko w miejscach ktore odwiedzilismy
        #if current == end:
        #    break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost + heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    #path[node] - > connections, path wskaqzuje na kierunek w ktorym mamy sie poruszac
    return path

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
