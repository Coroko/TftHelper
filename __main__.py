import apiConnection    as api
import sqliteTFT        as sql
import redneuronal      as ai

def populate_db():
    sql.start_db()
    conexion=sql.openConnection()
    cur= conexion.cursor()
    user= ["Corokoo","harry32xd","CazadorDeMinitas","infernixx","ReventXz v2"]
    for name in user :
        data=api.getUser(name)
        sql.insertIntoTablePlayers(cur,data)
    cur.execute('''select puuid from players''')
    for row in cur.fetchall():
        puuidofplayer = ''.join(row)
        data=api.getAllMatches(puuidofplayer)
        for matchid in data :
            game_hash=sql.createGameHash(puuidofplayer,matchid)
            gamedata=api.getMatchById(matchid)
            for participant in gamedata["info"]["participants"]:
                sql.insertIntoTableGames(cur,participant,game_hash,matchid)
                puuid=participant["puuid"]
                for units in participant["units"]:
                    sql.insertIntoTableUnits(cur,units,game_hash,puuid)
                for traits in participant["traits"]:
                    sql.insertIntoTableTraits(cur,traits,game_hash,participant["puuid"])
                
    sql.closeConnection(cur)
    conexion.commit()     

def start_cnn():
        
def main():
    populate_db()

if __name__=='__main__':
    main()