
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

    
    cur.execute('''CREATE TABLE IF NOT EXISTS DATASET ( ronda       int
                                                        ,pos        int
                                                        ,tiempo     float)''')
    cur.execute('''SELECT PUUID FROM GAMES ''')
    for puuid in cur.fetchall():
        cur.execute('''SELECT placement from Games where PUUID = "{puuid}" '''.format(puuid=player))  
        for data in cur.fetchall():
            placement.append(data[0])
        cur.execute('''SELECT last_round from Games where PUUID = "{puuid}" '''.format(puuid=player))  
        for data in cur.fetchall():
            round.append(data[0])
        cur.execute('''SELECT time_eliminated from Games where PUUID = "{puuid}" '''.format(puuid=player))  
        for data in cur.fetchall():
            time.append(data[0])
    print(time)
    print(placement)
    print(round)
 
        


dataset_creation()