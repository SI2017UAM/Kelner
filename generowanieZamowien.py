import numpy as np
import random
import sys
import csv

from os import path

def logika(names,medprep,medprice,meanprep,meanprice):
    '''min_count=min(list(set.values))
    for key in np.shuffle(list(set.keys())):
        if min_count==set[key]:
            min_fdname=key
    max_count=max(list(set.values))
    for key in np.shuffle(list(set.keys())):
        if max_count==set[key]:
            max_fdname=key'''
    #kebab,lody,ciasto,rollokebs,piwo,napoje,spaghetti,kawa/herbata,zupa,pizza,frytki,zapiekanka
    if meanprice<20.5:
        if meanprep<13.5:
            chosen="drogie/czasochlonne"
        else:
            chosen="drogie/proste"
    else:
        if meanprep<13.5:
            chosen="tanie/czasochlonne"
        else:
            chosen="tanie/proste"
    return chosen;


liczba_cykli=50
mean_order_count=400
per_level=100
menu=[]
order_list=[]

game_folder = path.dirname("__file__")
txt_folder = path.join(game_folder, 'txt_files')
with open(path.join(txt_folder,"menu.csv")) as menu_file:
    reader = csv.reader(menu_file,delimiter=";")
    print(next(reader))
    for row in reader:
        menu.append(row)

food_counter={}
names=[]
focus_strength=1
for item in menu:
    food_counter[item[0]]=0
    names.append(item[0])

order_num=[]

food_counter={}
focus_strength=1
for item in menu:
    food_counter[item[0]]=0
j=8
while(j<mean_order_count):
    j+=5
    order_num=np.concatenate((np.random.poisson(j,per_level),order_num),axis=0)
f = open('workfile.csv', 'w')
for i in names:
    f.write(str(i)+",")
f.write("mean_prep, mean_difficulty, mean_price, dodaj\n")
total_diffs=[]
total_price=[]
total_prep=[]
for i in np.arange(len(order_num)):
    #random_focus1=np.random.randint(0,len(menu))
    #random_focus2=np.random.randint(0,len(menu))
    current_preps=[]
    current_diffs=[]
    current_prices=[]
    food_counter=dict.fromkeys(food_counter,0)
    rnder=np.random.randint(0,len(menu))
    random_focus=[]
    for i in np.random.choice(len(menu),rnder,replace=False):
        random_focus.append(i)
    for j in np.arange(order_num[i]):
        rnd=np.random.randint(0,len(menu))
        b=False
        for t in np.arange(focus_strength):
            if rnd not in random_focus:
                rnd=np.random.randint(0,len(menu))
        foodname=menu[rnd][0]
        preptime=np.random.randint(int(menu[rnd][1]),int(menu[rnd][2])+1)
        difficulty=np.random.randint(int(menu[rnd][3]),int(menu[rnd][4])+1)
        price=np.random.randint(int(menu[rnd][5]),int(menu[rnd][6])+1)
        #order_list.append([foodname,preptime,difficulty,price])
        current_preps.append(preptime)
        current_diffs.append(difficulty)
        current_prices.append(price)
        food_counter[foodname]+=1
        total_prep.append(preptime)
        total_diffs.append(difficulty)
        total_price.append(price)
    medprep=np.median(current_preps)
    meddiff=np.median(current_diffs)
    medprice=np.median(current_prices)
    meanprice=np.mean(current_prices)
    meanprep=np.mean(current_preps)
    meandiff=np.mean(current_diffs)
    wynik=logika(names,medprep,medprice,meanprep,meanprice)
    for i in names:
        f.write(str(food_counter[i])+",")
    f.write(str(meanprep)+","+str(meandiff)+","+str(meanprice)+","+str(wynik)+"\n")
print("\nPrice Mean,Median",np.mean(total_price),np.median(total_price),"\n")
print("Diffs Mean,Median",np.mean(total_diffs),np.median(total_diffs),"\n")
print("Prep Mean,Median",np.mean(total_prep),np.median(total_prep),"\n")
