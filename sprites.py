import pygame as pg
import numpy as np
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
        self.waiting_for_order=0
        self.orders_to_kitchen=0
        self.waiting_for_delivery=0
        self.waiting_for_food_prep=0
        self.eating_food=0
        #collecting_mode=0 -> zbieram zamowienia, =1 dostarczam do kuchni
        self.collecting_mode=0
        self.last_goal=self.game.goal
        self.all_tables_count=len(self.game.tables_coord)
        self.delay_mode=0
        self.basic_timer=pg.time.get_ticks()/1000
        self.nothintodo=0
        self.wait=0
        self.eating_timers={}
    def arrangeTimers(self):
        #print("im here")
        for key, value in self.orders.items():
            if value==4:
                if key not in self.eating_timers:
                    self.eating_timers[key]=[pg.time.get_ticks()/1000,pg.time.get_ticks()/1000+np.random.poisson(FOOD_EATING_MEAN,1)+FOOD_EATING_ADD]
                else:
                    self.eating_timers[key][0]=pg.time.get_ticks()/1000
                    if self.eating_timers[key][0]>self.eating_timers[key][1]:
                        self.orders[key]=0
                        self.eating_food-=1
                        self.game.walls_obj[key][1].image = self.game.table_img[0]
                        self.game.client_agent.order_agents.pop(key)
                        self.game.client_agent.ammount_of_taken_tables-=1

                        #if (len(self.game.client_agent.free_tables)>0):
                        #    self.game.client_agent.free_tables.append(key)
                        #else:
                        #    self.game.client_agent.free_tables=[key]
                        if (len(self.game.client_agent.free_tables)==0):
                            self.game.client_agent.free_tables=np.array([key])
                        else:
                            self.game.client_agent.free_tables=np.insert(self.game.client_agent.free_tables,[0],np.array(key),axis=0)
                        self.eating_timers.pop(key)
                        self.game.client_agent.tableeFree()
                        print("from sprites",key,type(key),type([key[0],key[1]]),type(np.array(key)),type(self.game.client_agent.free_tables))
                        print(self.game.client_agent.free_tables)
    def ManhattanDistance(self,item1,item2):
        return (abs(item1[0]-item2[0])+abs(item1[1]-item2[1]))
    def returnOptimizedOrders(self,mod):
        heap=[]
        for i,value in self.orders.items():
            if value==mod:
                heapq.heappush(heap,(self.ManhattanDistance(self.game.start,i),i))
        if heap:
            return (heapq.heappop(heap)[1])
        else:
            print("WAITING ERROR")
    def getOrders(self):
        for key, value in self.game.client_agent.order_agents.items():
            if key not in self.orders:
                #active
                self.orders[key]=1
                self.waiting_for_order+=1
            else:
                #stolik obsluzony kiedys
                if self.orders[key]==0:
                    self.orders[key]=1
                    self.waiting_for_order+=1
    def defineGoal(self):
        #bierzemy 'na chama' pierwszy lepszy element z zamowien, lepiej to zoptymalizowac pod katem odleglosci
        if (self.is_busy==0 and self.delay_mode!=1 and self.wait!=1):
            goal_changed=0
            if (self.collecting_mode==0 and self.waiting_for_order>0):
                #podejdz do stolika po zamowienie
                self.game.goal=vec(self.returnOptimizedOrders(1))
                goal_changed=1
            elif (self.collecting_mode==1):
                #podejdz do kuchni
                self.game.goal=self.game.kitchen_pos
                goal_changed=1
            elif (self.collecting_mode==2 and self.waiting_for_delivery>0):
                #podejdz do kuchni odebrac zamowienie
                self.game.goal=vec(self.returnOptimizedOrders(3))
                goal_changed=1
            if (goal_changed==1):
                self.game.path=a_star_search(self.game,self.game.goal,self.game.start)
                self.last_goal=self.game.goal
                self.is_busy=1
    def goalAchieved(self):
        if (self.delay_mode!=1 and self.is_busy==1 and (abs(self.game.goal[0] - self.pos[0]//TILESIZE)+ abs(self.game.goal[1] - self.pos[1]//TILESIZE)<=1) and self.last_goal==self.game.goal):
            self.is_busy=0
            if (self.collecting_mode==0):
                #jeżeli czeka na podejscie kelnera i chce zlozyc zamowienie
                if (self.orders[(self.game.goal[0], self.game.goal[1])]==1):
                    self.waiting_for_order-=1
                    # = 2 czyli czeka na przygotowanie danie
                    self.orders[(self.game.goal[0],self.game.goal[1])]=2
                    #ZMIENIAMY WYGLAD STOLIKA
                    self.game.walls_obj[self.game.goal[0],self.game.goal[1]][1].image = self.game.table_img[2]
                    #DODAJEMY 1 do liczby oczekujacych na jedzonko
                    self.orders_to_kitchen+=1
            if (self.collecting_mode==2):
                if (self.orders[(self.game.goal[0], self.game.goal[1])]==3):
                    #print("delivered and eating coords->",(self.game.goal[0], self.game.goal[1]))
                    self.waiting_for_delivery-=1
                    #print(self.waiting_for_delivery,self.waiting_for_order)
                    #eating
                    self.orders[(self.game.goal[0], self.game.goal[1])]=4
                    self.eating_food+=1
                    self.game.walls_obj[self.game.goal[0],self.game.goal[1]][1].image = self.game.table_img[4]
            if (self.collecting_mode==1):
                if (self.orders_to_kitchen>0):
                    self.game.kitchen.takeOrders()
                    self.waiting_for_food_prep+=self.orders_to_kitchen
                    self.orders_to_kitchen=0
                if (self.game.kitchen.orders_ready>0):
                    self.game.kitchen.orders_ready=0
                    to_remove=[]
                    for i in self.game.kitchen.orders_prepared.keys():
                        if i in self.orders:
                            if self.orders[i]==2:
                                self.orders[i]=3
                                self.waiting_for_delivery+=1
                                self.waiting_for_food_prep-=1
                                self.game.walls_obj[i][1].image = self.game.table_img[3]
                                to_remove.append(i)
                    for i in to_remove:
                        self.game.kitchen.orders_prepared.pop(i)
                if (self.nothintodo):
                    self.wait=1
    def manualGoalChange(self):
        if self.delay_mode!=1 and self.is_busy==1 and self.last_goal!=self.game.goal:
            self.delay_mode = 1
            self.timer1=pg.time.get_ticks()/1000
            print("manual")
        if self.delay_mode==1 and pg.time.get_ticks()/1000 - self.timer1 >0.5:
            self.game.goal=self.last_goal
            self.game.path=a_star_search(self.game,self.game.goal,self.game.start)
            self.delay_mode=0
            print("manual")
        #zmiana zachowania, dostarczanie zamowien do kuchni, prosta wersja
    def updateCollectingMode(self):
        # Kiedy kelner ma isc do kuchni zlozyc zamowienia
        # collecting = 0 -> zbieramy zamowienia od klientow
        # collecting =1 -> idziemy do kuchni zlozyc zamowienia/odebrac potrawy
        # colecting =2 -> roznosimy potrawy
        #self.waiting_for_order= czekaja az podejdzie kelner po zamowienie
        #self.orders_to_kitchen= po odebraniu zamowienia zwieksza sie o 1, zeruje sie przy zdeponowaniu zamowien
        #self.waiting_for_delivery= zwieksza sie gdy kelner podejdzie do kuchni i beda dostepne posilki
        #self.waiting_for_food_prep= zwieksza sie gdy kelner doniesie zamowienie
        #self.eating_food= maja jedzenie i sa happy
        self.nothintodo=(self.waiting_for_delivery+self.game.kitchen.orders_ready+self.waiting_for_order+self.orders_to_kitchen+self.waiting_for_food_prep==0 and pg.time.get_ticks()/1000 > 5)
        if (not self.nothintodo):
            self.wait=0
        if (self.is_busy==0 and self.delay_mode!=1):

            kuchenne = self.game.kitchen.orders_ready+self.orders_to_kitchen>0
            test=len(self.game.tables_coord) < 2* self.orders_to_kitchen

            test2=self.game.client_agent.ammount_of_taken_tables==self.all_tables_count

            #test odleglosci od kuchni
            test3=(abs(self.game.kitchen_pos[0] - self.pos[0]//TILESIZE)+ abs(self.game.kitchen_pos[1] - self.pos[1]//TILESIZE)<=5)

            if ((test and  (self.collecting_mode==0) or (self.waiting_for_delivery==0 and self.game.kitchen.orders_ready>0)) or (test3 and kuchenne and self.collecting_mode!=2) or self.nothintodo):
                self.collecting_mode=1
            elif (self.waiting_for_delivery>0):
                self.collecting_mode=2
            elif (self.waiting_for_order>self.waiting_for_delivery and self.collecting_mode!=2):
                self.collecting_mode=0
            elif ( self.waiting_for_order==0 and  (self.game.kitchen.orders_ready>0 or self.orders_to_kitchen>0 or ( self.collecting_mode==2 and self.waiting_for_delivery==0))):
                self.collecting_mode=1
            else:
                self.collecting_mode=0
        # kiedy ma isc do kuchni odebrac zamowienia

    def update(self):
        #mpos=vec(pg.mouse.get_pos())
        #mpos-=self.game.camera.camera.topleft
        #self.rot = (self.game.kitchen_pos - self.pos).angle_to(vec(1, 0))

        #calculates the angle to a given vector in degrees.
        #angle_to(Vector2) -> float

        #collecting_mode=0 -> zbieramy zamowienia ze stolow

        self.getOrders()
        self.updateCollectingMode()
        self.defineGoal()
        self.goalAchieved()
        self.manualGoalChange()
        if (self.eating_food>0):
            self.arrangeTimers()
        if (pg.time.get_ticks()/1000 - self.basic_timer > 3):
            self.basic_timer=pg.time.get_ticks()/1000
            #print("MOD=",self.collecting_mode,"Is_busy=",self.is_busy,"\nZamawiajacy=",self.waiting_for_order,
            #"Zamowienia do kuchni=",self.orders_to_kitchen,"\nCzekajacy na zarcie=",self.waiting_for_delivery, "EATING=",self.eating_food,"\nZamowienie w kuchni",self.game.kitchen.orders_ready)

        #PORUSZANIE SIĘ
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
        self.orders={}
        self.orders_prepared={}
        self.orders_to_be_prepared=0
        self.preparing_food=0
        self.order_preparation=0
        self.orders_ready=0
    def update(self):
        if (self.preparing_food==0 and self.orders_to_be_prepared>0):
            self.preparing_food=1
        if (self.preparing_food==1 and self.orders_to_be_prepared<1):
            self.preparing_food=0
        if (self.preparing_food==1):
            self.prepareFood()
            #print(self.orders,self.game.client_agent.order_agents[8,10].order_list,self.game.client_agent.order_agents[14,8].order_list)
    def totalPrepTime(self,foodList,key):
        preptime=0
        for i in foodList:
            #[foodname,preptime,difficulty,price]
            preptime += i[1]
        return preptime
    # wez pierwsze lepsze zamowienie
    def pickOrder(self):
        for i in self.orders.keys():
            # sprawdzamy czy zamowienie jest oczekujace
            if self.orders[i][0]==1:
                #zmieniamy jego status na w trakcie realizacji
                self.orders[i]=(2,self.orders[i][1])
                return i
    def prepareFood(self):
        if (self.order_preparation==0 and self.orders_to_be_prepared>0):
            self.current_order_key=self.pickOrder()
            self.food_prep_begin=pg.time.get_ticks()/1000
            self.order_preparation=1
        #print(self.order_preparation,"Timer begin ",self.food_prep_begin," current time ",pg.time.get_ticks()/1000," how high difference is needed ", self.orders[self.current_order_key][1]/KITCHEN_FOOD_PREPARING_SPEED," difference ",self.order_preparation==1 and pg.time.get_ticks()/1000 - self.food_prep_begin)
        if (self.order_preparation==1 and pg.time.get_ticks()/1000 - self.food_prep_begin > self.orders[self.current_order_key][1]/KITCHEN_FOOD_PREPARING_SPEED):
            # status zamowienia zmieniamy na do odbioru
            self.orders_prepared[self.current_order_key]=self.orders[self.current_order_key]
            self.orders.pop(self.current_order_key)
            self.order_preparation=0
            self.orders_to_be_prepared -= 1
            self.orders_ready+=1
            #self.orders[self.current_order_key]=(3,self.orders[self.current_order_key][1])
            #print("order ",self.current_order_key, " ready!")
    def takeOrders(self):
        for key,value in self.game.mob.orders.items():
            if key not in self.orders and value==2:
                #potrawa do przygotowania
                self.orders[key]=(1,self.totalPrepTime(self.game.client_agent.order_agents[key].order_list,key))
                self.orders_to_be_prepared += 1
            if key in self.orders and self.orders[key][0]==3 and value==0:
                pass
                self.orders[key]=(1,self.totalPrepTime(self.game.client_agent.order_agents[key].order_list,key))
                self.orders_to_be_prepared += 1
        #print (self.game.mob.orders.values())
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
