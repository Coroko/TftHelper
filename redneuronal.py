
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import pandas as pd
import sqliteTFT as sql
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pydot
from keras.losses import CategoricalCrossentropy

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
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
                                                        ,tiempo     float
                                                        ,units      varchar)''')
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
        temp_unit=",".join(temp_unit)
        units.append(temp_unit)
    for index in range(len(units)):
        sql.insertIntoTableDataSet(cur,round[index],placement[index],time[index],units[index])
    sql.closeConnection(cur)
    con.commit()  

def model(preprocessing_head, inputs):
    body = tf.keras.Sequential([
    
    layers.Dense(32,activation='relu'),
    layers.Dense(20,activation='relu'),
    layers.Dense(10, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(5, activation='sigmoid'),
    layers.Dense(3, activation='sigmoid'),
    layers.Dense(1)
    ])
    preprocessed_inputs = preprocessing_head(inputs)
    result = body(preprocessed_inputs)
    model = tf.keras.Model(inputs, result)
    model.compile(loss='logcosh',
                    optimizer=tf.optimizers.Adam())
    return model

def create_model():
    con=sql.openConnection()  
    inputs = {}
    tft= pd.read_sql_query("SELECT * FROM DATASET", con,dtype={"ronda": int,"pos": int,"tiempo":float })
    tft_features = tft.copy()
    tft_labels = tft_features.pop('pos')
    for name, column in tft_features.items():
        dtype = column.dtype
        if dtype == object:
            dtype =tf.string
        else:
            dtype = tf.float32
        inputs[name] = tf.keras.Input(shape=(1,), name=name, dtype=dtype)
    numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}
    x = layers.Concatenate()(list(numeric_inputs.values()))
    norm = layers.Normalization()
    norm.adapt(np.array(tft[numeric_inputs.keys()]))
    all_numeric_inputs = norm(x)
    preprocessed_inputs = [all_numeric_inputs]
    for name, input in inputs.items():
      if input.dtype == tf.float32:
        continue

    lookup = layers.StringLookup(vocabulary=np.unique(tft_features[name]))
    one_hot = layers.CategoryEncoding(max_tokens=lookup.vocab_size())

    x = lookup(input)
    x = one_hot(x)
    preprocessed_inputs.append(x)
    preprocessed_inputs_cat = layers.Concatenate()(preprocessed_inputs)
    tft_preprocessing = tf.keras.Model(inputs, preprocessed_inputs_cat)
    tft_features_dict = {name: np.array(value) 
                         for name, value in tft_features.items()}
    features_dict = {name:values[:1] for name, values in tft_features_dict.items()}
    tft_preprocessing(features_dict)
    tft_model = model(tft_preprocessing, inputs)

    tft_model.fit(x=tft_features_dict, y=tft_labels, epochs=10)#para la cantidad de datos que tenemos estos epoch seran suficientes.
    return tft_model