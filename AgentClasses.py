import telepot
from telepot.namedtuple import *
from Agent import Agent
from Messages import Messages, send_message
from Database import DB

#############################
##### GENERATE KEYBOARD #####
#############################

#generate inline keyboard for callback queries
def generate_keyboard(agentName, choice, data):
    #For binary options, callback data is simple, explictly stated below
    if choice == 'ultOption': #Generate binary option
        return [[InlineKeyboardButton(text=Messages['yes'],callback_data="{ULTYES}"),
                InlineKeyboardButton(text=Messages['no'],callback_data="{ULTNO}")]
                ]

    elif choice == '3options': #for healers, when ult is available, can choose to attack, use ability or heal
        return [[InlineKeyboardButton(text=Messages['attHealOption']['att'],callback_data="{ATTACK}"),
                InlineKeyboardButton(text=Messages['attHealOption']['heal'],callback_data="{HEAL}"),
                 InlineKeyboardButton(text=Messages['attHealOption']['ult'],callback_data="{ULTYES}")]
                ]

    elif choice == 'attHeal':
        return [[InlineKeyboardButton(text=Messages['attHealOption']['att'],callback_data="{ATTACK}"),
                InlineKeyboardButton(text=Messages['attHealOption']['heal'],callback_data="{HEAL}")]
                ]

    #For other options, callback data has the data structure: agentName{|targetAgentName|option|}
    elif choice not in ('attack', 'heal', 'ult') and 'ult' not in choice:
        choice = 'Error'
    
    result = []        
    for agent in data:
        result.append([InlineKeyboardButton(text=agent.get_idty(),
                                            callback_data=agentName+"{|"+agent.agentName+"|"+choice+"|}")])
    return result

######################
##### SEND QUERY #####
######################

#Each class will have its own predefined send_query method, but these are customised alternatives
#depending on hero requirements

async def send_query(self,bot,data,players,mode):
    #self refers to hero object
    #mode will be 1 of the following: single or multi
    #single: select 1 target
    #multi: select multiple targets
    #data = callback data, players = list of agents
    if data == 'startQuery':
        if isinstance(self,Healer):
            if self.ultAvail:
                message = Messages['query']['doWhat']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'3options',players))
            else:
                message = Messages['query']['doWhat']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'attHeal',players))
        else:
            if self.ultAvail:
                message = Messages['query']['canUlt']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'ultOption',players))
            else:
                message = Messages['query']['attack']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'attack',players))

    elif data =='healerOptionsAfterUlt':
        message = Messages['query']['doWhatNext']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'attHeal',players))
        
    elif data == 'heal':
        message = Messages['query']['heal']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'heal',players))
        
    elif 'ult' in data:
        if mode == 'single':
            message = Messages['query']['ult'][self.agentName]
            markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'ult',players))

        elif mode == 'multi': #Ult data will be (ult,%d) where %d is the nth target to use his ability on
            num = int(data[1])
            message = Messages['query']['select'][min(4,num)]%(num) + Messages['query']['ult'][self.agentName]
            keyboard = generate_keyboard(self.agentName,'ult|'+str(num),players)
            if num > 1: #Add a 'I'm done' option
                keyboard.append([InlineKeyboardButton(text=Messages['none'],callback_data='{NONE}')])
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    else:
        message = Messages['query']['attack']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(self.agentName,'attack',players))
            
    sent = await bot.sendMessage(self.userID,message,reply_markup=markup)
    self.editor = telepot.aio.helper.Editor(bot,telepot.message_identifier(sent))
    return

###################
## PROCESS QUERY ##
###################

# Data structure is of the form "agentName{|targetAgentName|option|date|}"
async def process_query_default(self,game,queryData):
    if 'ULTYES' in queryData:
        date = queryData.split('|')[1]
        DB[game.chatID].append((int(date),self.agentName,self.agentName,'ult')) #target and agent is self
        if self.attackAfterUlt: #still able to attack after ability activation
            if isinstance(self,Healer):
                await self.send_query(game.bot,'healerOptionsAfterUlt',list(game.get_alive_all().values()))
            else:
                await self.send_query(game.bot,'attack',list(game.get_alive_all().values()))
        return

    elif queryData in ('{ULTNO}','{ATTACK}'):
        await self.send_query(game.bot,'attack',list(game.get_alive_all().values()))
        return

    elif '{HEAL}' == queryData:
        await self.send_query(game.bot,'heal',list(game.get_alive_all().values()))
        return
    
    #Reformat data to become a tuple (date,agent,targetAgent,option)
    agent = queryData.split('{')[0]
    queryData = queryData.split('|')
    target, option, date = queryData[1], queryData[2], int(queryData[3])
    DB[game.chatID].append((date,agent,target,option))
    return

# Data structure is of the form "agentName{|targetAgentName|option|date|}"
async def process_query_single(self,game,queryData):
    if 'ULTYES' in queryData:
        await self.send_query(game.bot,'ult',list(game.get_alive_all().values()))
        return
    #Everything else below is almost the same as the default process_query
    elif queryData in ('{ULTNO}','{ATTACK}'):
        await self.send_query(game.bot,'attack',list(game.get_alive_all().values()))
        return

    elif '{HEAL}' == queryData:
        await self.send_query(game.bot,'heal',list(game.get_alive_all().values()))
        return
    
    elif 'ult' in queryData and self.attackAfterUlt:
        #To cover the case where we need to send attack query after player chose target to use ability on
        if isinstance(self,Healer):
            await self.send_query(game.bot,'healerOptionsAfterUlt',list(game.get_alive_all().values()))
        else:
            await self.send_query(game.bot,'attack',list(game.get_alive_all().values()))
        
    #Reformat data to become a tuple (date,agent,targetAgent,option)
    agent = queryData.split('{')[0]
    queryData = queryData.split('|')
    target, option, date = queryData[1], queryData[2], int(queryData[3])
    DB[game.chatID].append((date,agent,target,option))
    return

# Data structure is of the form "agentName{|targetAgentName|option|num|date|}"
async def process_query_multi(self,game,queryData,limit): #limit = max no. of selections
    if 'ULTYES' in queryData:
        await self.send_query(game.bot,('ult',1),list(game.get_alive_all().values()))
        #For abilities affecting multiple targets, agents won't be able to attack after ability activation (subject to change)
        return
    
    elif queryData in ('{ULTNO}','{ATTACK}'):
        await self.send_query(game.bot,'attack',list(game.get_alive_all().values()))
        return

    elif '{HEAL}' == queryData:
        await self.send_query(game.bot,'heal',list(game.get_alive_all().values()))
        return    
    
    agent = queryData.split('{')[0]
    queryData = queryData.split('|')
    #After split, becomes [agentName{, targetAgentName, option, num <--(avail only if option == ult), date, '}']
    target,option = queryData[1], queryData[2]
    if 'ult' in queryData:
        num, date = int(queryData[3]), int(queryData[4])
        self.selected.append(target) #add name to selected options
        num += 1
        if num <= limit: #send another query
            #remove selected options
            players = [x for x in list(game.get_alive_all().values()) if x.agentName not in self.selected]
            if players:
                await self.send_query(game.bot,('ult',num),players)
    else:
        date = int(queryData[3])
    DB[game.chatID].append((date,agent,target,option))
    return
    
#####################
###### OFFENSE ######
#####################

#Offense heroes can have their ults powered up, except for 2 (Taiji & Saitami)
class Offense(Agent):
    def __init__(self, agentName, userID, username, firstName,
                 baseHealth=None, baseDmg=25, baseUltCD=None, baseUltDmg=0, ultDmg=None,
                 alive=True,health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=True, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None,
                 ):
        
        #set ult default damage for Offense Class
        self.baseUltDmg = baseUltDmg
        self.ultDmg = ultDmg if ultDmg else self.baseUltDmg
        
        super().__init__(agentName, userID, username, firstName,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    def reset_ult_dmg(self):
        self.ultDmg = self.baseUltDmg

    def add_ult_dmg(self,dmg): #dmg > 0 = add, dmg < 0 = reduce
        self.ultDmg += dmg

    def reset_next_round(self):
        super().reset_next_round()
        self.reset_ult_dmg()


    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'default')


    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_default(self,game,queryData)
        return
    
        
####################
####### TANK #######
####################
        
class Tank(Agent):
    def __init__(self, agentName, userID, username, firstName,
                 baseHealth=130, baseDmg=20, baseUltCD=3,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=0.02, protector=None
                 ):
        
        super().__init__(agentName, userID, username, firstName,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'default')


    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_default(self,game,queryData)
        return
    

####################
###### HEALER ######
####################

# Note that Healers have extra attributes: baseHealAmt and healAmt, and thus, have extra methods too

class Healer(Agent):
    def __init__(self, agentName, userID, username, firstName,
                 baseHealth=90, baseDmg=17, baseUltCD=3, baseHealAmt=10,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, healAmt=None, attackAfterUlt=False,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=0.1, protector=None
                 ):
        #set defaults for baseHealAmt and healAmt
        self.baseHealAmt = baseHealAmt
        self.healAmt = self.baseHealAmt
        self.canHeal = True

        super().__init__(agentName, userID, username, firstName,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    def reset_heal_amt(self):
        self.healAmt = self.baseHealAmt

    def reset_can_heal(self):
        self.canHeal = True
    
    def heal(self,ally,amt=0):
        amt = amt if amt else self.healAmt
        
        if self == ally:
            if self.canHeal and self.canBeHealed:
                self.add_health(0.5*amt)
                return Messages['combat']['selfHeal']%(self.get_idty(),self.health)
            else:
                return Messages['combat']['failHealSelf']%(self.get_idty())
            
        elif self.canHeal and ally.canBeHealed:
            ally.add_health(amt)
            return Messages['combat']['heal']%(ally.get_idty(),ally.health,self.get_idty())
        return Messages['combat']['failHeal']%(self.get_idty(),ally.get_idty())

    def add_heal_amt(self,amt):
        self.healAmt += amt

    def reset_next_round(self):
        super().reset_next_round()
        self.reset_heal_amt()
        self.reset_can_heal()
        
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'default')


    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_default(self,game,queryData)
        return

######################
###### SUPPPORT ######
######################
            
class Support(Agent):
    def __init__(self, agentName, userID, username, firstName,
                 baseHealth=None, baseDmg=None, baseUltCD=None,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None
                 ):
        
        super().__init__(agentName, userID, username, firstName,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)   
