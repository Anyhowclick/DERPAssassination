import telepot
from telepot.namedtuple import *
from Agent import Agent
from Messages import send_message, edit_message
from KeyboardQuery import generate_action_keyboard
import Globals

######################
##### SEND QUERY #####
######################
#Each class will have its own predefined send_query method, but these are customised alternatives
#depending on hero requirements

async def send_query(self,bot,queryData,players,mode,gameMode):
    #bot is to send message
    #queryData = callback data
    #players = list of agents for options
    #mode = default, single or multiple
    #Default = no need target, single = single target, multiple = multiple targets
    Messages = Globals.LANG[self.userID]
    #The default for the start of every query
    if queryData == 'start':
        if isinstance(self,Healer):
            #For healers, they can do 3 things: Attk, heal or ult (if available)
            if self.ultAvail:
                message = Messages['query']['doWhat']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'3options',players,gameMode))
            else:
                message = Messages['query']['doWhat']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'attHeal',players,gameMode))
        else: #Non-healers
            if self.ultAvail: #If can ult, ask if they want to use
                message = Messages['query']['canUlt']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'ultOption',players,gameMode))
            else: #Otherwise, ask them who they wanna attack
                message = Messages['query']['attack']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'attack',players,gameMode))

    #If agent can attk / heal after using ult....
    elif queryData =='healerOptionsAfterUlt':
        message = Messages['query']['doWhatNext']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'attHeal',players,gameMode))

    #Person chose to heal. So ask for who the person wants to heal
    elif queryData == 'heal':
        message = Messages['query']['heal']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'heal',players,gameMode))

    #Person chose to use ult. Data structure is either 'ult' or ('ult',num) where num is the nth target.
    elif 'ult' in queryData:
        if mode == 'single':
            message = Messages['query']['ult'][self.agentName]
            markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'ult',players,gameMode))

        elif mode == 'multi': #Ult data will be (ult,num) where num is the nth target to use his ability on
            num = int(queryData[1])
            message = Messages['query']['select'][min(4,num)]%(num) + Messages['query']['ult'][self.agentName] #Anything more than 4, no need special prefix for message
            keyboard = generate_action_keyboard(Messages,'ult|'+str(num),players,gameMode)
            if num > 1: #Add a 'I'm done' option
                keyboard.append([InlineKeyboardButton(text=Messages['none'],callback_data='{NONE}')])
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    else:
        message = Messages['query']['attack']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_action_keyboard(Messages,'attack',players,gameMode))

    #If first query, send new message
    if not self.editor:
        sent = await send_message(bot,self.userID,message,reply_markup=markup)
        self.editor = telepot.aio.helper.Editor(bot,telepot.message_identifier(sent))

    #Otherwise, keep editing the old one!!
    else:
        await edit_message(self.editor,message,reply_markup=markup)
    return

###################
## PROCESS QUERY ##
###################
async def process_query(self,game,queryData,mode):
    #self = Hero object
    #game = Game object
    #queryData = data obtained from user selection. Common data structure of the form {|option|targetAgentID|date|}, {|ULTYES|date|} etc.
    #option being 'attack','heal','ult'
    #mode = 'default','single',('multi',num) where num is max no. of targets the hero can choose
    #result will be the final tuple to be stored in Globals.DBG. Has data structure (option,agentID,targetAgentID,date)
    
    #Common method that applies to all agents
    if queryData in ('{ULTNO}','{ATTACK}'): #Person chose to attack
        await self.send_query(game.bot,'attack',list(game.get_alive_all().values()),game.gameMode)
        return

    elif '{HEAL}' == queryData: #Person chose to heal
        await self.send_query(game.bot,'heal',list(game.get_alive_all().values()),game.gameMode)
        return
    
    if mode == 'single':
            if 'ULTYES' in queryData: #queryData is {|ULTYES|date|}, person chose to use ult. Single means has to choose 1 target
                await self.send_query(game.bot,'ult',list(game.get_alive_all().values()),game.gameMode)
                return
            #Check if hero can attack after using ult. If can, send query
            elif 'ult' in queryData and self.attackAfterUlt:
                if self.attackAfterUlt: #Need to send additional query asking who the player wants to attack (or heal)
                    if isinstance(self,Healer): #Hero is a healer, so ask if want to attack or heal
                        await self.send_query(game.bot,'healerOptionsAfterUlt',list(game.get_alive_all().values()),game.gameMode)
                    else:
                        await self.send_query(game.bot,'attack',list(game.get_alive_all().values()),game.gameMode)
                    
    elif 'multi' in mode: #Mode = (muilti,num) where num is max no. of targets hero can attack
        #For abilities affecting multiple targets, agents won't be able to attack after ability activation (subject to change)
            if 'ULTYES' in queryData: #Ask for 1st target he wants to attack
                await self.send_query(game.bot,('ult',1,mode[1]),list(game.get_alive_all().values()),game.gameMode)
                return
            elif 'ult' in queryData: #Need to send additional queries
                #Data structure of form {|ult|num|targetAgentID|date|}
                queryData = queryData.split('|')
                num, target = int(queryData[2]), game.agents[int(queryData[3])]
                self.selected.append(target) #add target object to selected options
                num += 1 #Increment no. of ppl selected by 1
                if num <= mode[1]: #send another query to ask for next target
                    #remove the previous selected targets from list
                    players = [x for x in list(game.get_alive_all().values()) if x not in self.selected]
                    if players: #If got ppl to select, send query.
                        await self.send_query(game.bot,('ult',num),players,game.gameMode)
                        
                #Store as a 4-value tuple: (option,agentID,targetAgentID,date)        
                await Globals.QUEUE.put((Globals.DBG,game.chatID,('ult',self.userID,int(queryData[3]),int(queryData[4]))))
                return
                
    else: #Default mode
        if 'ULTYES' in queryData:
            if self.attackAfterUlt: #Need to send additional query asking who the player wants to attack (or heal)
                if isinstance(self,Healer): #Hero is a healer, so ask if want to attack or heal
                    await self.send_query(game.bot,'healerOptionsAfterUlt',list(game.get_alive_all().values()),game.gameMode)
                else:
                    await self.send_query(game.bot,'attack',list(game.get_alive_all().values()),game.gameMode)
                
    #Finally, we store the query in the game object.
    #queryData is of the form {|option|targetAgentID|date|}
    queryData = queryData.split('|')
    #Store as a 4-value tuple: (option,agentID,targetAgentID,date)
    await Globals.QUEUE.put((Globals.DBG,game.chatID,(queryData[1],self.userID,int(queryData[2]),int(queryData[3]))))
    return

#####################
###### OFFENSE ######
#####################

#Offense heroes can have their ults powered up, except for 2 (Taiji & Saitami)
class Offense(Agent):
    def __init__(self, agentCode, userID, username, firstName, Messages,
                 baseHealth=None, baseDmg=25, baseUltCD=None, baseUltDmg=0, ultDmg=None,
                 alive=True,health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=True, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None,
                 ):
        
        #set ult default damage for Offense Class
        self.baseUltDmg = baseUltDmg
        self.ultDmg = ultDmg if ultDmg else self.baseUltDmg
        
        super().__init__(agentCode, userID, username, firstName, Messages,
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
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'default',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'default')
        return
    
        
####################
####### TANK #######
####################
        
class Tank(Agent):
    def __init__(self, agentCode, userID, username, firstName, Messages,
                 baseHealth=130, baseDmg=20, baseUltCD=3,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=0.02, protector=None
                 ):
        
        super().__init__(agentCode, userID, username, firstName, Messages,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'default',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'default')
        return
    

####################
###### HEALER ######
####################

# Note that Healers have extra attributes: baseHealAmt and healAmt, and thus, have extra methods too

class Healer(Agent):
    def __init__(self, agentCode, userID, username, firstName, Messages,
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

        super().__init__(agentCode, userID, username, firstName, Messages,
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
                self.add_stats_heal(0.5*amt)
                return self.Messages['combat']['selfHeal']%(self.get_idty(),self.health)
            else:
                return self.Messages['combat']['failHealSelf']%(self.get_idty())
            
        elif self.canHeal and ally.canBeHealed:
            ally.add_health(amt)
            self.add_stats_heal(amt)
            self.add_stats_healed(ally)
            return self.Messages['combat']['heal']%(ally.get_idty(),ally.health,self.get_idty())
        return self.Messages['combat']['failHeal']%(self.get_idty(),ally.get_idty())

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
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'default',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'default')
        return

######################
###### SUPPPORT ######
######################
            
class Support(Agent):
    def __init__(self, agentCode, userID, username, firstName, Messages,
                 baseHealth=None, baseDmg=None, baseUltCD=None,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None
                 ):
        
        super().__init__(agentCode, userID, username, firstName, Messages,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)   
