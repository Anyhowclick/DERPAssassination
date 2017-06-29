#TO BLOCK SPAMMERS
import asyncio
import telepot
import telepot.aio
import time
from Messages import send_message, EN
import Globals

PENALTY = {0:0,1:10,2:60,3:300,4:600,5:900,6:1800,7:3600,8:43200,9:86400,10:259200,11:999999999999} #Penalty time to ignore in seconds
GRPS = [(-198106155,'<a href = "https://t.me/joinchat/AAAAAEGpbgIRVICT8IRpHg">'), #FOR TESTING
        (-1001101622786,'<a href = "https://t.me/joinchat/AAAAAEGpbgIRVICT8IRpHg">'),
        (-1001090679151,'<a href="https://t.me/joinchat/AAAAAEECcW8ICTmNpWQgVQ">'),
        (-1001117357538, '<a href="https://t.me/joinchat/AAAAAEKZheLEzw0_JFj81Q">'),
        (-1001103517150, '<a href="https://t.me/joinchat/AAAAAEHGVd5xynxQ-I3KbQ">'),
        (-1001149281548, '<a href="https://t.me/derpassasinindo">')] #Groups for people to join
GRPS_INFO = {} #Eventually will be a list, not dict, after auto_update is run (function below)
GRPS_TIME = 0 #The last time GRPS was updated. Will be done hourly.
#Get threshold limit of spam
def get_threshold(num):
    if num <= 3:
        return 0.75
    elif num <= 8:
        return 0.7
    else:
        return 0.6
    
#Return true if user is in blocked list
async def check_spam(handler,msg):
    userID = msg['from']['id']
    #All info is stored as such: ID:(pastTime,average,strike,blockedStatus,blockTime)
    
    #pastTIme: The last query received from the person
    #average: The average of time differences
    #strike: The no. of violations of the threshold, ie. how many times the person spammed...
    #blockedStatus: 1 if blocked, 0 otherwise
    #blockedTime: The start time of person's penalty
    try:
        person = Globals.SPAM[userID] #If person already in DB, then load preferences
        #First check if person is to be ignored
        if person[3]:
            timeDiff = person[4] #retrieve the 'past' penalty
            timeDiff = time.time()-timeDiff #get difference
            if timeDiff >= PENALTY[person[2]]:
                Globals.SPAM[userID] = (round(time.time(),3),person[1],person[2],0,0) #can listen to person again for queries
                return False
            else:
                #Continue to ignore person
                return True

        try:
            Globals.LANG[userID]
        except KeyError:
            Globals.LANG[userID] = EN

        #Check if person is spamming
        timeDiff = round(time.time() - person[0],3) #Calculate current timeDiff
        average,strike = person[1],person[2] #Retrieve past average and no. of strikes person has
        average = 0.78/timeDiff + 0.22*average #Take weighted average
        threshold = get_threshold(strike)
        if average > threshold: #VIOLATE THRESHOLD
            strike = min(strike+1,8)
            await send_message(handler.bot,userID,Globals.LANG[userID]['spam'][1]%(PENALTY[strike]/60),parse_mode='HTML')
            #Store back into Globals.SPAM database
            Globals.SPAM[userID] = (round(time.time(),3),average,strike,1,round(time.time(),3))
            return True
        Globals.SPAM[userID] = (round(time.time(),3),0,strike,0,0)
        return False

    #Person not in Globals.SPAM database
    except KeyError:
        Globals.SPAM[userID] = (round(time.time(),3),0,0,0,0)
        return False
    
async def auto_update(bot):
    #Retrieve information of groups
    global GRPS, GRPS_INFO, GRPS_TIME
    for chatID,link in GRPS:
        #Update group member count and group title
        #Stored in GRPS_INFO using chatID as the key: {chatID: {'title':GrpTitle,'link':link,'members':memberCount}}
        try:
            result = await bot.getChat(chatID)
        except telepot.exception.TelegramError:
            continue
        result = result['title'] #Obtain group title
        try:
            GRPS_INFO[chatID]['title'] = result
        except KeyError:
            GRPS_INFO[chatID] = {}
            GRPS_INFO[chatID]['title'] = result
            
        GRPS_INFO[chatID]['link'] = link
        
        result = await bot.getChatMembersCount(chatID)
        GRPS_INFO[chatID]['members'] = result
    #Convert to a list for sorting
    GRPS_INFO = sorted(GRPS_INFO.items(),key=lambda x:x[0])
    GRPS_INFO.sort(key=lambda y:y[1]['members'],reverse=True)
    GRPS_TIME = time.time() #Update the time
    return

async def check_admin(bot,chatID,userID): #Check if user is admin based on userID
    admins = await bot.getChatAdministrators(chatID) #admins are in a list
    for member in admins:
        if userID == member['user']['id']:
            return True
    return False

#Maintenance variable to determine if bot is to be repaired
def toggle_maintenance():
    Globals.MAINTENANCE = not Globals.MAINTENANCE
    return

def get_maintenance():
    return Globals.MAINTENANCE

#Returns a list of groups with info below
#Each item in grps is a tuple as follows: (grpID,{'memberCount':members,'title':GrpTitle,'link':inviteLink})
async def get_grp_info(bot):
    global GRPS_INFO, GRPS_TIME
    if time.time() - GRPS_TIME > 3600: #Last update was 1 hour ago
        await auto_update(bot)
    return GRPS_INFO
                
