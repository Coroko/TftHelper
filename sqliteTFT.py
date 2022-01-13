import sqlite3
import hashlib
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
    print("Conexion cerrado")
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
    print("Anadiendo unidad "+data["character_id"]+" de (puuid): "+puuid)
    cur.execute('''INSERT INTO UNITS VALUES('{game_hash}','{unit_name}','{rarity}','{tier}','{items}','{player}') '''.format(game_hash=game_hash
                                                                                                  ,unit_name=data['character_id']
                                                                                                  ,rarity=data['rarity']
                                                                                                  ,tier=data ['tier']
                                                                                                  ,items=data ['items'],
                                                                                                  player= puuid))
def insertIntoTableTraits(cur,data,game_hash,puuid):
    print("Anadiendo trait "+data["name"]+" de (puuid): "+puuid)
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