import apiConnection as con
import sqliteTFT    as sql
import time
def populate_db():
    sql.start_db()
    conexion=sql.openConnection()
    cur= conexion.cursor()
    user= ["Corokoo","Yosta","harry32xd","CazadorDeMinitas","infernixx","AGO traviscwat","ReventXz v2"]
    for name in user :
        data=con.getUser(name)
        sql.insertIntoTablePlayers(cur,data)
        for row in cur.execute('''select puuid from players'''):
            puuid = ''.join(row)
            data=con.getAllMatches(puuid)
            player =con.getUserByPuuid(puuid)
            print(player["name"])
            for matchid in data :
                game_hash=sql.createGameHash(puuid,matchid)
                gamedata=con.getMatchById(matchid)
                for participant in gamedata["info"]["participants"]:
                    sql.insertIntoTableGames(cur,participant,game_hash,matchid)
    sql.closeConnection(cur)
    conexion.commit()

           
             

populate_db()

