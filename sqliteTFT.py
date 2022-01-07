import sqlite3
import hashlib
con = sqlite3.connect('tft.sqlite')
cur= con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS PLAYERS (
            PUUID               VARCHAR NOT NULL PRIMARY KEY ,
            level               INT,
            ID                  VARCHAR,
            player_ID           VARCHAR
            name                VARCHAR SECONDARY KEY)''')
cur.execute('''CREATE TABLE IF NOT EXISTS GAMES (
            level_in_game       INT,
            placement           INT,
            gold                INT,
            last_round          INT,
            time_eliminated     FLOAT,
            game_id             VARCHAR,
            game_hash           VARCHAR PRIMARY KEY,
            PUUID               VARCHAR,
            FOREIGN KEY (PUUID) REFERENCES PLAYERS (PUUID))''')
cur.execute('''CREATE TABLE IF NOT EXISTS UNITS (
            game_hash           varchar PRIMARY KEY,
            unit_name           varchar,
            rarity              INT,
            tier                INT,
            items               varchar,
            FOREIGN KEY (game_hash) REFERENCES GAMES (game_hash))''')
cur.execute('''CREATE TABLE IF NOT EXISTS TRAITS (
            game_hash           varchar PRIMARY KEY,
            trait_name          varchar,
            num_unit            INT,
            style               INT,
            tier_current        INT,
            tier_total          FLOAT,
            FOREIGN KEY (game_hash) REFERENCES GAMES (game_hash))''')


def insertIntoTablePlayers(cur,data):
    cur.execute('''INSERT INTO PLAYERS VALUES({puuid},{level},{id},{player_ID},{name}) '''.format(puuid=data['puuid']
                                                                                                  ,level=data['level']
                                                                                                  ,id=data['id']
                                                                                                  ,player_ID=data['player_ID']
                                                                                                  ,name=data['name']))
def insertIntoTableGames(cur,data):
    cur.execute('''INSERT INTO GAMES VALUES({puuid},{level_in_game},{placement}
                                        ,{gold},{last_round},{time_eliminated}
                                        ,{game_id},{game_hash}) '''.format(puuid=data['puuid']
                                                                            ,level=data['level']
                                                                            ,placement=data['placement']
                                                                            ,gold=data['gold']
                                                                            ,last_round=data['last_round']
                                                                            ,time_eliminated=data['time_eliminated']
                                                                            ,game_id=data['game_id']
                                                                            ,game_hash=hashlib.sha256(data['puuid'].encode()+data['game_id'].encode).hexdigest()
                                                                            ))