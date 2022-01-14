import apiConnection    as api
import sqliteTFT        as sql
import redneuronal      as ai

def populate_db():
    sql.start_db()
    conexion=sql.openConnection()
    cur= conexion.cursor()
    user= ["Corokoo","harry32xd","CazadorDeMinitas","infernixx","ReventXz v2"] #jugadores analizar
    for name in user :
        data=api.getUser(name)
        sql.insertIntoTablePlayers(cur,data)
    cur.execute('''select puuid from players''') #Una vez añadidos para no hacer tantas llamadas a la api, cojemos los puuid del sqlite
    for row in cur.fetchall():
        puuidofplayer = ''.join(row)
        data=api.getAllMatches(puuidofplayer)
        for matchid in data : #Obtenidas todas las partidas, procederemos a sacar todos los puntos importantes de ellas
            gamedata=api.getMatchById(matchid)
            for participant in gamedata["info"]["participants"]: 
                puuid=participant["puuid"]
                print(puuid)
                game_hash=sql.createGameHash(puuid,matchid)
                sql.insertIntoTableGames(cur,participant,game_hash,matchid)
                for units in participant["units"]:
                    sql.insertIntoTableUnits(cur,units,game_hash,puuid)
                for traits in participant["traits"]:
                    sql.insertIntoTableTraits(cur,traits,game_hash,puuid)
                #tras haber hecho esto obtrendemos una base de datos bastante consolidada, con un total entre todas
                #sus filas al rededor de los 3000 datos, y esto solo con 5 jugadores y 4 partidas con cada uno.
    sql.closeConnection(cur)
    conexion.commit()     

       
def main():
    populate_db()
    #start_cnn()

if __name__=='__main__':
    main()