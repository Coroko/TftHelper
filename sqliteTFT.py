import sqlite3
import hashlib
import apiConnection as api

def start_db():
    print("Iniciando base de datos...")
    con = sqlite3.connect('tft.sqlite')
    cur= con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS PLAYERS (
                PUUID               VARCHAR NOT NULL PRIMARY KEY ,
                level               INT,
                ID                  VARCHAR,
                player_ID           VARCHAR,
                name                VARCHAR SECONDARY KEY)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS GAMES (
                level_in_game       INT,
                placement           INT,
                gold                INT,
                last_round          INT,
                time_eliminated     FLOAT,
                game_id             VARCHAR,
                game_hash           VARCHAR,
                PUUID               VARCHAR,
                FOREIGN KEY (PUUID) REFERENCES PLAYERS (PUUID))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS UNITS (
                game_hash           varchar,
                unit_name           varchar,
                rarity              INT,
                tier                INT,
                items               varchar,
                player_puuid        varchar)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS TRAITS (
                game_hash           varchar,
                trait_name          varchar,
                num_unit            INT,
                style               INT,
                tier_current        INT,
                tier_total          FLOAT,
                player_puuid        varchar)''')
    cur.close()
    con.commit()
def openConnection():
    con = sqlite3.connect('tft.sqlite')
    print("Conexion abierta")
    return(con)
def closeConnection(cur):
    print("Conexion cerrada")
    cur.close()
    
def insertIntoTablePlayers(cur,data):
    print("Anadiendo Jugador "+data["name"])
    cur.execute('''INSERT INTO PLAYERS VALUES('{puuid}','{level}','{id}','{player_ID}','{name}') '''.format(puuid=data['puuid']
                                                                                                  ,level=data['summonerLevel']
                                                                                                  ,id=data['id']
                                                                                                  ,player_ID=data['accountId']
                                                                                                  ,name=data['name']))
def insertIntoTableGames(cur,data,game_hash,match_id):
    print("Anadiendo partida "+match_id+" de (puuid): "+data["puuid"])
    cur.execute('''INSERT INTO GAMES VALUES('{level_in_game}','{placement}'
                                        ,'{gold}','{last_round}','{time_eliminated}'
                                        ,'{game_id}','{hash}','{puuid}') '''.format(puuid=data['puuid']
                                                                            ,level_in_game=data['level']
                                                                            ,placement=data['placement']
                                                                            ,gold=data['gold_left']
                                                                            ,last_round=data['last_round']
                                                                            ,time_eliminated=data['time_eliminated']
                                                                            ,game_id=match_id
                                                                            ,hash=game_hash
                                                                            ))
def insertIntoTableUnits(cur,data,game_hash,puuid):
    cur.execute('''INSERT INTO UNITS VALUES('{game_hash}','{unit_name}','{rarity}','{tier}','{items}','{player}') '''.format(game_hash=game_hash
                                                                                                  ,unit_name=data['character_id']
                                                                                                  ,rarity=data['rarity']
                                                                                                  ,tier=data ['tier']
                                                                                                  ,items=data ['items'],
                                                                                                  player= puuid))
def insertIntoTableTraits(cur,data,game_hash,puuid):
    cur.execute('''INSERT INTO TRAITS VALUES('{game_hash}','{trait_name}','{num_unit}','{style}','{tier_Current}','{tier_total}','{player}') '''.format(game_hash=game_hash,
                                                                                                                                trait_name=data['name'],
                                                                                                                                num_unit=data['num_units'],
                                                                                                                                style=data['style'],
                                                                                                                                tier_Current=data['tier_current'],
                                                                                                                                tier_total=data['tier_total'],
                                                                                                                                player= puuid))
def createGameHash(puuid,game_id):
    game_hash =hashlib.sha256(puuid.encode()+game_id.encode()).hexdigest()
    return (game_hash)

def insertIntoTableDataSet(cur,ronda,pos,tiempo,personajes):
    cur.execute('''INSERT INTO DATASET VALUES('{ronda}','{pos}','{tiempo}','{personajes}') '''.format(ronda=ronda,pos=pos,tiempo=tiempo,personajes=personajes))
    
def populate_db():
    start_db()
    conexion=openConnection()
    cur= conexion.cursor()
    user= ["Corokoo","Undefined CEO","aidennnnn","harry32xd","covilla 19","CazadorDeMinitas","infernixx","ReventXz v2",
           "SNG Lev Trotskij","Lorus","AGO Lelouch","simplyw0jtek","ArmaTruc","BALOTELLI777","OGiii"] #jugadores analizar
    for name in user :
        data=api.getUser(name)
        insertIntoTablePlayers(cur,data)
    cur.execute('''select puuid from players''') #Una vez añadidos para no hacer tantas llamadas a la api, cojemos los puuid del sqlite
    for row in cur.fetchall():
        puuidofplayer = ''.join(row)
        data=api.getAllMatches(puuidofplayer)
        for matchid in data : #Obtenidas todas las partidas, procederemos a sacar todos los puntos importantes de ellas
            gamedata=api.getMatchById(matchid)
            for participant in gamedata["info"]["participants"]: 
                puuid=participant["puuid"]
                game_hash=createGameHash(puuid,matchid)
                insertIntoTableGames(cur,participant,game_hash,matchid)
                for units in participant["units"]:
                    insertIntoTableUnits(cur,units,game_hash,puuid)
                for traits in participant["traits"]:
                    insertIntoTableTraits(cur,traits,game_hash,puuid)
                #tras haber hecho esto obtrendemos una base de datos bastante consolidada, con un total entre todas
                #sus filas al rededor de los 3000 datos, y esto solo con 5 jugadores y 4 partidas con cada uno.
    closeConnection(cur)
    conexion.commit()
    