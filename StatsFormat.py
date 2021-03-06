import simplejson as json
GLOBAL_STATS = {
    "derpWins":0,
    "pyroWins":0,
    "drawsNormal":0,
    "ffaGames":0,
    "players":0,
    "groups":0,
    
    #name is firstName
    "bestNormalAgent":{ #Best win ratio for normal games
        "name":"Unknown",
        "rate":0},
    
    "derpNormalWins":{ #Most no. of Derp wins
        "name":"name",
        "rate":0},

    "pyroNormalWins":{ #Most no. of Pyro wins
        "name":"Unknown",
        "rate":0},
    
    "normalSurvivor":{
        "name":"Unknown",
        "rate":0}, #Best survival rate in normal mode
    
    "ffaKing":{
        "name":"name",
        "rate":0}, #Most FFA Wins

    "mostDmgNormal":{
        "name":"name",
        "rate":0},
    
    "mostDmgFFA":{
        "name":"name",
        "rate":0},
    
    "mostHealAmt": {
        "name":"name",
        "rate":0},
      
    "mostPplHealed":{
        "name":"name",
        "rate":0},
    
    "mostPplKilled":{
        "name":"name",
        "rate":0},

    "lastUpdated":0,
    }

GRPID = {
    "grpID": {
      "title":"a",
      "powerUps":True,
      "gamesPlayed":0,
      "gamesCompleted":0,
      "waiting":{
            "username":'',
            "noUsername":[],
            },
      "lang":"EN",
  }
}

LOCALID = {
    "localID": {
        "firstName":'firstName',
        "username":'username',
        "lang":"EN",

        "gold":0,
        "diamond":0,
      
        "mostPplHealed": 0,
        "mostPplKilled": 0,
        "mostHealAmt": 0,
        "mostDmgNormal" :0,
        "mostDmgFFA": 0,

        "normalGamesPlayed": 0,
        "normalGamesSurvived": 0,
        "pyroNormalWins": 0,
        "drawsNormal": 0,
        "derpNormalWins": 0,
        "ffaWins": 0,
        "ffaGamesPlayed": 0,
        }
    }

with open('globalStats.txt','w') as outfile:
        json.dump(GLOBAL_STATS,outfile)
