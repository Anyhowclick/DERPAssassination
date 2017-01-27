#TO BLOCK SPAMMERS
import asyncio
import telepot
import telepot.aio
import time
from Messages import Messages, send_message
from Database import DB,SPAM,STRIKE,BLOCKED

THRESHOLD = {0:0.75, 1:0.7, 2:0.7, 3:0.6, 4:0.6, 5:0.6, 6:0.6, 7:0.6, 8:0.6}
PENALTY = {0:0,1:10,2:60,3:900,4:3600,5:86400,6:259200, 7:999999999999} #Penalty time to ignore in seconds
MAINTENANCE = False

#Return true if user is in blocked list
async def check_spam(handler,msg):
    userID = msg['from']['id']
    if userID in BLOCKED: #first check if user has been ignored
        timeDiff = BLOCKED[userID] #retrieve the 'past' time stored
        timeDiff = time.time()-timeDiff #get difference
        if timeDiff > PENALTY[STRIKE[userID]]:
            del BLOCKED[userID] #can listen to person again for queries
            SPAM[userID] = (round(time.time(),3),0) 
            return False
        return True
    
    elif userID not in SPAM:
        #first variable is to store current time rounded to 3dp
        #last is to store average queries per second, starting with 0.5
        SPAM[userID] = (round(time.time(),3),0.5) 
        STRIKE[userID] = 0 #store no. of times person violated threshold
        return False
    
    pastTime,average = SPAM[userID]
    timeDiff = round(time.time()-pastTime,3)
    average = 0.78/timeDiff + 0.22*average #Take weighted average
    SPAM[userID] = (round(time.time(),3),average)
    strike = STRIKE[userID]
    if average > THRESHOLD[strike]: #VIOLATE THRESHOLD
        strike += 1
        STRIKE[userID] = strike 
        BLOCKED[userID] = round(time.time(),3) #store current time
        await send_message(handler.bot,userID,Messages['spam'][strike],parse_mode='HTML')
        return True
    return False

def start_spam():
    while True:
        SPAM={}
        time.sleep(900)

async def check_admin(bot,chatID,userID): #Check if user is admin based on userID
    admins = await bot.getChatAdministrators(chatID) #admins are in a list
    for member in admins:
        if userID == member['user']['id']:
            return True
    return False

def on_maintenance():
    global MAINTENANCE
    MAINTENANCE = True
    return

def get_maintenance():
    global MAINTENANCE
    return MAINTENANCE
                
