import simplejson as json
GLOBALSTATS = {
    "derpWins":0,
    "pyroWins":0,
    "drawsNormal":0,
    "players":0,
    "groups":0,
      
    "survivorsTotal":0,
    "killedTotal":0,
    
    #firstName, username, survival / death rate
    "bestSurvivor":["Donny","",0],
    "bestMinion":["Donny","",0],

    "mostDmgAmtNormal":["name",0],
    "mostDmgFFA":["name",0],
    "mostHealedAmt":["name",0],
    "mostShieldAmt":["name",0],
      
    "mostPplResurrected":["name",0],
    "mostPplHealed":["name",0],
    "mostPplKilled":["name",0],
    "mostPowUps":["name",0],

    #stored as [no. of games, game length]
    "aveNormGameLength":[0,0],
    "aveFfaGameLenggth":[0,0]
    }

GRPID = {
    "grpID": {
      "title":"a",
      "minPlayers":3,
      "maxPlayers":20,
      "lang":"EN",
  }
}

with open('globalStats.txt','w') as outfile:
        json.dump(GLOBALSTATS,outfile)
