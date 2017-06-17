from Messages import ZH, IN, EN, send_message
import simplejson as json
import time
import asyncio
DBP, DBG, LANG, LOCALID, GRPID, GLOBAL_STATS, SPAM = {},{},{},{},{},{},{}
QUEUE = asyncio.Queue() #Item placed is of format: (dictionary,key,value)
MIN_PLAYERS = 2
MAX_PLAYERS = 20
lastUpdate = 0
'''
DBP will be used to store queries and info from PERSONS
DBG will be used to store group game instances
LOCALID and GRPID stores personal and group statistics respectively
GLOBAL_STATS stores global statistics
LANG will store languages used by people / group (object)
QUEUE is a global queue to handle writing into different python dicts (thread safety)
Refer to StatsFormat for the type of statistics stored for GLOBALSTATS
The rest are sort of stated below.
'''

async def update_dict():
    while True:
        dicty,key,value = await QUEUE.get()
        dicty[key] = value

STATS = {
    "pplHealed":0,
    "pplKilled":0,
    "healAmt":0,
    "dmg":0,
    }
        
#Initialise stats for new person
async def add_new_person(ID,msg):
    #Retrieve firstname
    firstName = msg['from']['first_name']

    #Retrieve username, if any
    try:
        username = msg['from']['username']
    except KeyError:
        username = None
    
    toStore = {
        "firstName":firstName,
        "username":username,
        "lang":"EN",

        "gold":0,
        "diamond":0,
      
        "mostPplHealed": 0,
        "mostPplKilled": 0,
        "mostHealedAmt": 0,
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
    
    global LOCALID
    await QUEUE.put((LOCALID,ID,toStore))
    Messages = await save_lang(ID,'EN') #Set default to English
    autosave()
    return Messages

#Initialise stats for new group
async def add_new_group(ID,msg):
    toStore = {
        "title":msg['chat']['title'],
        "powerUps":True,
        "gamesPlayed":0,
        "gamesCompleted":0,
        "lang":"EN",
        }
    
    await QUEUE.put((GRPID,ID,toStore))
    Messages = await save_lang(ID,'EN')
    autosave()
    return Messages

#Save statistics every 5 mins
def autosave():
    global lastUpdate
    if time.time() - lastUpdate >= 300:
        save_database()
        lastUpdate = time.time()
    return

#To load the files
def load_database():
    global LOCALID, GRPID, GLOBAL_STATS,LANG
    LOCALID = json.loads(open('localStats.txt').read())
    #Convert all string keys to int
    LOCALID = {int(k):v for k,v in LOCALID.items()}
    GRPID = json.loads(open('grpStats.txt').read())
    #Convert all string keys to int
    GRPID = {int(k):v for k,v in GRPID.items()}
    GLOBAL_STATS = json.loads(open('globalStats.txt').read())
    #Codes are gotten from ISO standard
    langs = {'ZH':ZH,'IN':IN,'EN':EN}
    for person in list(LOCALID.keys()):
        #This doesn't require use of global queue, because it only runs after bot is restarted
        LANG[person] = langs[LOCALID[person]['lang']]
    print('Database loaded!')
    return

#Save the data!
def save_database():
    with open('localStats.txt','w') as outfile:
        json.dump(LOCALID,outfile)
    with open('grpStats.txt','w') as outfile:
        json.dump(GRPID,outfile)
    with open('globalStats.txt','w') as outfile:
        json.dump(GLOBAL_STATS,outfile)
    return

async def save_lang(ID,choice):
    global LOCALID, GRPID
    ID = int(ID)
    #Save preference in LANG database
    langs = {'ZH':ZH,'IN':IN,'EN':EN}
    #Not using global queue, because... it caused problems (KeyErrors, due to CallbackHandlers?)
    LANG[ID] = langs[choice]
    await asyncio.sleep(0.1)
    #To save lang codes in resp IDs
    if ID < 0:
        await QUEUE.put((GRPID[ID],'lang',choice))
    else:
        await QUEUE.put((LOCALID[ID],'lang',choice))
    autosave()
    return LANG[ID]
