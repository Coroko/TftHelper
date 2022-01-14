
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import pandas as pd
import sqliteTFT as sql

def dataset_creation():
    #objetivo ronda,pos,tiempo,personajes
    con=sql.openConnection()  
    cur=con.cursor()
    round=[]
    placement=[]
    time=[]
    units=[]
    cur.execute('''CREATE TABLE IF NOT EXISTS DATASET ( ronda       int
                                                        ,pos        int
                                                        ,tiempo     float)''')
    cur.execute('''SELECT game_hash FROM GAMES ''')
    for game_hash in cur.fetchall():
        temp_unit=[]
        game_hash=game_hash[0]
        cur.execute('''SELECT placement from Games where game_hash = "{game_hash}" '''.format(game_hash=game_hash))  
        for data in cur.fetchall():
            placement.append(data[0])
        cur.execute('''SELECT last_round from Games where game_hash = "{game_hash}" '''.format(game_hash=game_hash))  
        for data in cur.fetchall():
            round.append(data[0])
        cur.execute('''SELECT time_eliminated from Games where game_hash = "{game_hash}" '''.format(game_hash=game_hash))  
        for data in cur.fetchall():
            time.append(data[0])
        cur.execute('''SELECT unit_name from units where game_hash = "{game_hash}" '''.format(game_hash=game_hash))  
        for data in cur.fetchall():
          temp_unit.append(data[0]) 
        units.append(temp_unit)
        temp_unit.clear()
    print(time)
    print(placement)
    print(round)
    print(units)
 
        


dataset_creation()