import pygame as pg
import heapq
import random
from settings import *
#from main import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

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
def distanceDictionary():
    Dict={}
    Dict[vec2int(vec(1, 0))]=10
    Dict[vec2int(vec(0, 1))]=10
    Dict[vec2int(vec(-1, 0))]=10
    Dict[vec2int(vec(0, -1))]=10
    Dict[vec2int(vec(1, 1))]=14
    Dict[vec2int(vec(-1, 1))]=14
    Dict[vec2int(vec(1, -1))]=14
    Dict[vec2int(vec(-1, -1))]=14
    return Dict

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        # spritecollide(sprite, group, dokill, collided = None) -> Sprite_list
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
class PriorityQueue:
    def __init__(self):
        self.nodes = []
    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost,node))
    def get(self):
        return heapq.heappop(self.nodes)[1]
    def empty(self):
        return len(self.nodes)==0

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        # prostokat dla wykrywania kolizji, rozmiar jest stały, niezależny od prostokąta z obrazu
        # srodkiem tego prostokata jest polozenie srodka naszego zwyklego prostokata
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        # get_pressed czyli tak dlugo jak jest wcisniety
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # cofamy się wolniej niż idziemy do przodu
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        # ustalamy wymiary prostokata
        self.rect = self.image.get_rect()
        # ustalamy srodek (x,y) prostokata
        self.rect.center = self.pos
        #self.game.dt - używamy dzięki czemu mamy frame-independent movement
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        #print(pg.time.get_ticks()//1000)
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.path_distance_translator=distanceDictionary()
        self.is_busy=0
        self.orders={}
        self.waiting_orders=0
        self.collecting_orders_mode=1
    def ManhattanDistance(self,item1,item2):
        return (abs(item1[0]-item2[0])+abs(item1[1]-item2[1]))
    def returnOptimizedOrders(self):
        heap=[]
        for i,value in self.orders.items():
            if value==1:
                heapq.heappush(heap,(self.ManhattanDistance(self.game.start,i),i))
        if heap:
            return (heapq.heappop(heap)[1])
    def getOrders(self):
        for key, value in self.game.client_agent.order_agents.items():
            if key not in self.orders:
                #active
                self.orders[key]=1
                self.waiting_orders+=1
            else:
                #stolik obsluzony kiedys
                if self.orders[key]==0:
                    self.orders[key]=1
                    self.waiting_orders+=1
    def defineGoal(self):
        #bierzemy 'na chama' pierwszy lepszy element z zamowien, lepiej to zoptymalizowac pod katem odleglosci
        if (self.is_busy==0 and self.waiting_orders>0):
            '''next_goal=vec()
            it=0
            while True:
                if (self.orders[list(self.orders)[it]]==1):
                    self.game.goal=vec(list(self.orders)[it])
                    break
                else:
                    it+=1'''
            self.game.goal=vec(self.returnOptimizedOrders())
            self.game.path=a_star_search(self.game,self.game.goal,self.game.start)
            self.is_busy=1
    def goalAchieved(self):
        if (self.is_busy==1 and (abs(self.game.goal[0] - self.pos[0]//TILESIZE)+ abs(self.game.goal[1] - self.pos[1]//TILESIZE)<=1)):
            self.is_busy=0
            self.waiting_orders-=1
            self.orders[(self.game.goal[0],self.game.goal[1])]=2
            #ZMIENIAMY WYGLAD STOLIKA
            self.game.walls_obj[self.game.goal[0],self.game.goal[1]][1].image = self.game.table_img[2]

    def update(self):
        #mpos=vec(pg.mouse.get_pos())
        #mpos-=self.game.camera.camera.topleft
        #self.rot = (self.game.kitchen_pos - self.pos).angle_to(vec(1, 0))

        #calculates the angle to a given vector in degrees.
        #angle_to(Vector2) -> float
        #Returns the angle between self and the given vector.
        if (self.collecting_orders_mode==1):
            self.getOrders()
            self.defineGoal()
            self.goalAchieved()
        if (self.game.start != self.game.goal):
            self.rot = (self.game.path[vec2int(self.pos // TILESIZE)]).angle_to(vec(1, 0))
        #POZYCJA w hexaxh
        #print(self.pos // TILESIZE)
        #print (self.rot)
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        #self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.vel = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.pos += self.vel * self.game.dt
        #self.acc += self.vel * -1
        #self.vel += self.acc * self.game.dt
        #self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.hit_rect.centerx = self.pos.x
        # wykrywanie kolizji
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        #print(self.game.client_agent.order_agents)
        #print(type(self.game.path[(7,3)]))
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Kitchen(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.kitchen_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
class Table(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.img_num=0
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.table_img[self.img_num]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #self.rect.centerx-=TILESIZE/2
        #self.rect.centery-=TILESIZE/2
        #self.rect.width=40
        #self.rect.height=40
