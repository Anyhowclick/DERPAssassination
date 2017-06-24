from Messages import ZH, IN, EN, send_message
import simplejson as json
import time
import asyncio
import Globals
'''
Used to store and update stats
'''

async def update_dict():
    while True:
        dicty,key,value = await Globals.QUEUE.get()
        if dicty is Globals.DBG:
            try:
                lst = dicty[key]
                if value:
                    lst.append(value)
                    dicty[key] = lst
                else:
                    dicty[key] = value
            except KeyError:
                dicty[key] = value
        else:
            dicty[key] = value
        
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
    
    await Globals.QUEUE.put((Globals.LOCALID,ID,toStore))
    Messages = await save_lang(ID,'EN') #Set default to English
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
    
    await Globals.QUEUE.put((Globals.GRPID,ID,toStore))
    Messages = await save_lang(ID,'EN')
    return Messages

#Save statistics and update global stats every 10 mins
async def auto_save_update():
    while True:
        save_database()
        print('Database saved.')
        await update_global_stats()
        print('Global stats updated.')
        await asyncio.sleep(600)

def update_stat(person,key,variable):
    if person[key] > variable['rate']:
        variable = {'name':person['firstName'],'rate':person[key]}
    return variable


    
#Compute and update global statistics. Mode is to load up the relevant stats
async def update_global_stats():
    #Update total no. of ppl and no. of groups
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"players",len(Globals.LOCALID)))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"groups",len(Globals.GRPID)))
        #Load up current stats
    normalSurvivor = Globals.GLOBAL_STATS['normalSurvivor']
    ffaKing = Globals.GLOBAL_STATS['ffaKing']
    mostDmgNormal = Globals.GLOBAL_STATS['mostDmgNormal']
    mostDmgFFA = Globals.GLOBAL_STATS['mostDmgFFA']
    mostHealAmt = Globals.GLOBAL_STATS['mostHealAmt']
    mostPplHealed = Globals.GLOBAL_STATS['mostPplHealed']
    mostPplKilled = Globals.GLOBAL_STATS['mostPplKilled']
        
    #Compute individual stats, update accordingly
    for person in list(Globals.LOCALID.values()):
        #Compute / update survival rate
        try:
            survivalRate = person['normalGamesSurvived'] / person['normalGamesPlayed'] #Round to 3dp
        except ZeroDivisionError:
            survivalRate = 0
        survivalRate = round(survivalRate,3)
        if survivalRate > normalSurvivor['rate']:
            normalSurvivor = {'name':person['firstName'],'rate':survivalRate}

        #Compute / update FFAKing (most no. of FFA Wins) 
        ffaKing = update_stat(person,'ffaWins',ffaKing)
        
        #Stats below are in a single game
        #Compute / update mostDmgNormal
        mostDmgNormal = update_stat(person,'mostDmgNormal',mostDmgNormal)
        #Compute / update mostDmgFFA
        mostDmgFFA = update_stat(person,'mostDmgFFA',mostDmgFFA)
        #Compute / update mostHealAmt
        mostHealAmt = update_stat(person,'mostHealAmt',mostHealAmt)

        #Stats below are accumulative
        #Compute / update most people healed
        mostPplHealed = update_stat(person,'mostPplHealed',mostPplHealed)
        #Compute / update mostDmgNormal
        mostPplKilled = update_stat(person,'mostPplKilled',mostPplKilled)
            
    #Finally, update in Global stats
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"normalSurvivor",normalSurvivor))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"ffaKing",ffaKing))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"mostDmgNormal",mostDmgNormal))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"mostDmgFFA",mostDmgFFA))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"mostHealAmt",mostHealAmt))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"mostPplHealed",mostPplHealed))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"mostPplKilled",mostPplKilled))
    await Globals.QUEUE.put((Globals.GLOBAL_STATS,"lastUpdated",time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())))
    return

#To load the files
def load_database():
    Globals.LOCALID = json.loads(open('localStats.txt').read())
    #Convert all string keys to int
    Globals.LOCALID = {int(k):v for k,v in Globals.LOCALID.items()}
    Globals.GRPID = json.loads(open('grpStats.txt').read())
    #Convert all string keys to int
    Globals.GRPID = {int(k):v for k,v in Globals.GRPID.items()}
    Globals.GLOBAL_STATS = json.loads(open('globalStats.txt').read())
    #Codes are gotten from ISO standard
    langs = {'ZH':ZH,'IN':IN,'EN':EN}
    for person in list(Globals.LOCALID.keys()):
        #This doesn't require use of global queue, because it only runs after bot is restarted
        Globals.LANG[person] = langs[Globals.LOCALID[person]['lang']]
    print('Database loaded!')
    return

#Save the data!
def save_database():
    with open('localStats.txt','w') as outfile:
        json.dump(Globals.LOCALID,outfile)
    with open('grpStats.txt','w') as outfile:
        json.dump(Globals.GRPID,outfile)
    with open('globalStats.txt','w') as outfile:
        json.dump(Globals.GLOBAL_STATS,outfile)
    return

async def save_lang(ID,choice):
    ID = int(ID)
    #Save preference in Globals.LANG database
    langs = {'ZH':ZH,'IN':IN,'EN':EN}
    #Not using global queue, because... it caused problems (KeyErrors, due to CallbackHandlers?)
    Globals.LANG[ID] = langs[choice]
    await asyncio.sleep(0.1)
    #To save lang codes in resp IDs
    if ID < 0:
        await Globals.QUEUE.put((Globals.GRPID[ID],'lang',choice))
    else:
        await Globals.QUEUE.put((Globals.LOCALID[ID],'lang',choice))
    return Globals.LANG[ID]
