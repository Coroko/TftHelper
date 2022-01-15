import keys
import requests
import time

apiURL = "euw1.api.riotgames.com"

def getUser(name):
    response= requests.get("https://{api}/tft/summoner/v1/summoners/by-name/{name}?api_key={apiKey}".format(api=apiURL,name=name, apiKey=keys.developmentApiKey))
    response = response.json()
    print("Sleeping for 2 seconds...")
    time.sleep(2)
    return(response)
def getUserByPuuid(PUUID):
    response= requests.get("https://{api}/tft/summoner/v1/summoners/by-puuid/{puuid}?api_key={apiKey}".format(api=apiURL,puuid=PUUID, apiKey=keys.developmentApiKey))
    print("Sleeping for 2 seconds...")
    time.sleep(2)
    response = response.json()
    return(response)
def getAllMatches(PUUID):
    response= requests.get("https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=6&api_key={apiKey}".format(puuid=PUUID, apiKey=keys.developmentApiKey))
    print("Sleeping for 2 seconds...")
    time.sleep(2)
    response = response.json()
    return(response)
def getMatchById(matchID):
    response= requests.get("https://europe.api.riotgames.com/tft/match/v1/matches/{matchID}?api_key={apiKey}".format(matchID=matchID, apiKey=keys.developmentApiKey))
    print("Sleeping for 2 seconds...")
    time.sleep(2)
    response = response.json()
    return(response)
def getRank(summID):
    response= requests.get("https://{api}/tft/entries/by-summoner/{summID}?api_key={apiKey}".format(api=apiURL,summID=summID, apiKey=keys.developmentApiKey))
    print("Sleeping for 2 seconds...")
    time.sleep(2) 
    response = response.json()
    return(response)