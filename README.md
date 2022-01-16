# TFT helper application

***T***eam ***F***ight ***T***actics chatbot helper made made with python and _Riot_ Development API.
![pengu](https://static.wikia.nocookie.net/leagueoflegends/images/e/ec/Season_2019_-_Victorious_Pengu_-_Diamond_Emote.png/revision/latest/scale-to-width-down/250?cb=20191106002357)

Esta aplicacion utiliza tensorflow para crear un modelo de ANN en base a datos recogidos en un sqlite.
Todo el data set necesario para el entrenamiento se genera el solo, cogiendo datos directamente de la API de RIOT.

Para iniciar esta aplicacion solo hace falta correr el main como un script de python.
    
    /main.py
Y este generara el solo todos los datos que se necesiten para ejecutarse.

## Que he querido hacer con esta aplicaion:

Gracias a la gran cantidad de datos que genera cualquier juego siempre me ha parecido curioso que todo ello por detras solo sean variables muy simples, en este caso yo he cogido algunas de este juego y he empezado a transformalas para que una inteligecia artificial pueda reconocerlas y pueda trabajar sobre ellas. Ahora comentare los pasos que he seguido para crear la aplicacion y como he recogido toda la informacion

## 1. Recogida de informacion:

Esta parte se encarga el archivo ./apiConnection.py, en el tengo las siguientes funciones:
    
    def getUser(name):
Esta se encarga de que yo al pasarle cualquier id(Europea) de un jugador me devuelva datos importantes como el PUUID, el cual es una clave unica que tiene cada jugador y que permite que haga busquedas dentro de la api.

    def getUserByPuuid(PUUID):
A esta le dare uso mas adelanta ya que hace lo contrario a la anterior.

    def getAllMatches(PUUID):
Para conseguir los datos de todas las partidas primero he de buscar su id el cual consiguo aqui, en esta tuve que limitar las partidas por reglas de rate de la api.

    def getMatchById(matchID):
Esta es la funcion mas importante de recogida de informacion, ya que gracias a ella puedo conseguir los json con toda la informacion de la partida.

    def getRank(summID):
Al igual que getUserByPuuid(PUUID) esta la usare mas adelante.

## 2. Almacenaje de la informacion en una base de datos SQLite:

Para no hacer tantas llamadas a la API y no pasarme del limite he construido una base de datos la cual tiene la siguiente forma
    
 ![bd](./assets/bbdd.png)

las funciones que hacen posible la adicion son las siguientes y se encuentran en sqliteTFT:


    def start_db():
Esta funcion es la responsable de crear la base de datos principal donde dumpeare la informacion de la API    
    
    def openConnection():
 Abre una conexion con sqlite

    def closeConnection(cur):
Cierra la conexion con sqlite

Todas estas funciones insertan datos en la base de datos
    def insertIntoTablePlayers(cur,data):

    def insertIntoTableGames(cur,data,game_hash,match_id):
    
    def insertIntoTableUnits(cur,data,game_hash,puuid):

    def insertIntoTableTraits(cur,data,game_hash,puuid):

    def createGameHash(puuid,game_id):
Para poder usar la base de datos me tuve que crear una funcion que hiciese un has unico para poder pedir datos y que no se repitieran, en esta utilizo un SHA256 de los datos previamente hasheados.

    def insertIntoTableDataSet(cur,ronda,pos,tiempo,personajes):
Esta funcion de insercion es distinta ya que se trata de la funcion que inserta datos en la tabla DATASET que es la que uso para mi modelo de IA

    def populate_db():  
Esta funcion es la que comunica la api con la base de datos e inserta cada uno en su tabla correspondiente.

## 3. Creacion del modelo y ejecucion de este:

Finalmente llegamos a la creacion del modelo y preprocesado datos, aqui tuve varios problemas ya que no todas las entradas de mi modelo eran numeros, sino tambien habia strings en el. Aparte mi modelo se trata de uno sequencial de multiples entradas pero con una sola salida, lo que hace que este sea mas dificil la parte de preprocesamiento de datos que lo que es realmente el el modelo, para crearlo utilice las siguientes funciones.

    def dataset_creation():
Crea la tabla dataset y la puebla con datos los cuales los recoje del sqlite.

    def model(preprocessing_head, inputs):
        body = tf.keras.Sequential([
        
        layers.Dense(32,activation='relu'),
        layers.Dense(15,activation='relu'),
        layers.Dense(9, activation='relu'),
        layers.Dense(5, activation='relu'),
        layers.Dense(1,activation='sigmoid')
        ])
        preprocessed_inputs = preprocessing_head(inputs)
        result = body(preprocessed_inputs)
        model = tf.keras.Model(inputs, result)
        model.compile(loss='logcosh',
                        optimizer=tf.optimizers.Adam())
        return model
Esta funcion es el modelo como tal, y tras mucha prueba y error es la configuracion que mejor me ha funcionado con mi estilo de datos, en ella podemos ver 5 capas de densidad las cuales son las que condensan los datos que reciben de la base de datos, en ella utilice una sigmoide en la ultima capa para que me pusiese los datos entre 1 y -1. La funcion logcosh de perdidas la he utilizado por que lo que he investigado en internet sobre ella es la que mejor se ajusta a mis datos y al estilo que tienen mis datos.

Ahora pondre un ejemplo de una de mis ejecuciones:
    Epoch 1/10
    23/23 [==============================] - 0s 750us/step - loss: 3.3512
    Epoch 2/10
    23/23 [==============================] - 0s 773us/step - loss: 3.3409
    Epoch 3/10
    23/23 [==============================] - 0s 773us/step - loss: 3.3283
    Epoch 4/10
    23/23 [==============================] - 0s 750us/step - loss: 3.2998
    Epoch 5/10
    23/23 [==============================] - 0s 705us/step - loss: 3.2199
    Epoch 6/10
    23/23 [==============================] - 0s 705us/step - loss: 3.0702
    Epoch 7/10
    23/23 [==============================] - 0s 727us/step - loss: 2.9553
    Epoch 8/10
    23/23 [==============================] - 0s 705us/step - loss: 2.9228
    Epoch 9/10
    23/23 [==============================] - 0s 682us/step - loss: 2.9164
    Epoch 10/10
    23/23 [==============================] - 0s 682us/step - loss: 2.9145
Como podemos ver se mantiene hacia el 2.9 y tras probarlo varias veces con distintas configuraciones y con mas pasos, este ha sido el mas bajo que he obtenido

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

Finalmente aqui tenemos la funcion la cual es la responsable del preprocesamiento de la informacion y la ejecucion del modelo. Para preprocesar las imagenes las hemos de dividir entro los dtypes que devuelve pandas de la query qu hace a la base de datos, en este caso utilize el siguiente bucle:

    for name, column in tft_features.items():
            dtype = column.dtype
            if dtype == object:
                dtype =tf.string
            else:
                dtype = tf.float32
            inputs[name] = tf.keras.Input(shape=(1,), name=name, dtype=dtype)

Este es el responsable de diferenciar entre string y floats.

Tras esto tendremos que concatenar los tf.string con los datos numericos, para poder generar nuestro data set.

Finalmente podremos ejecutar nuestro modelo con la lista concatenada de features y los labels en este caso que son enteros, estos son la posicion en la que quedo cada jugador en la partida.


Trabajo realizado por:

Javier Cámara Jabonero 

U-tad 2022 Ingenieria de Software 

Para la clase de Inteligencia artificial.
