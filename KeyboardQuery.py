from telepot.namedtuple import *
from collections import OrderedDict
from Messages import setLang, ALL_LANGS, LANGEMOTES

'''
To generate keyboard options and to process queries.
'''
#Pre-condition: Any sequence of object, but must NOT be hashable (Thus dictionaries NOT accepted)
# Function to group elements together by iterating through sequence
#Seq is a sequence of objects
#Size is the desired size of each chunk
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

#Main menu buttons, where each option is of form (key,callbackdata)
#Key is used to retrieve actual text in Messages (due to different languages)
MENU = [
    ('info','#a0'),
    ('agents', '#b0'),
    ('stats','#c0'),
    ('lang','#d0'),
    ('groups','#e0'),
    ('donate','#f0'),
    ('rate','#g0'),
    ('about','#h0'),
    ('support','#i0')
    ]

INFO = [
    ('rules','#aa'), #To be replaced with game modes, then rules with callback data #aa+
    ('upgrades','#ab'),
    ('back','#-1')
    ]

CONFIG = [
    ('lang','#d1'),
    ('exit','#-2')
    ]
    
#Return the corresponding key to the data
def get_menu_key(data):
    for i in MENU:
        if i[1] == data:
            return i[0]
    return 'Error'

#############################
##### GENERATE KEYBOARD #####
#############################
#Messages: The dictionary of messages in the person's language
#State: See the code legend, but it's basically the callback data of menus so I know which state to return to

#Only back button keyboard
def generate_back_keyboard(Messages,state):
    #Just need to route to the previous menu level, which is easy to do thanks to the customised callback data
    #Base case: To route back to top menu level
    if state[-1] == '0':
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=Messages['menu']['back'],callback_data='#-1')]])
    state = state[:-1] + '0'
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=Messages['menu']['back'],callback_data=state)]])

#Config button keyboard for group admins
#ID here is the groupID that needs to be in the callback data, so I know which group the settings are changed for (Duh right?)
def generate_config_keyboard(Messages,state,ID):
    ID = str(ID)
    keyboard = []
    #Split into groups of 2
    for group in chunker(CONFIG,2):
        result = []
        for element in group:
            result.append(InlineKeyboardButton(text=Messages['config'][element[0]],callback_data=element[1]+'|'+ID))
        keyboard.append(result)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Agent info keyboard
def generate_agent_keyboard(Messages,state):
    keyboard = []
    HERO_INFO = OrderedDict(Messages['agents'])
    #Split into groups of 2
    for group in chunker(list(HERO_INFO.keys()),2):
        result = []
        for key in group:
            #Replace state with backward arrow icon
            if key == state:
                result.append(InlineKeyboardButton(text=Messages['config']['back'],callback_data='#-1'))
            else:
                #Text is just the agent name
                result.append(InlineKeyboardButton(text=HERO_INFO[key][0],callback_data=key))
        keyboard.append(result)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Info related queries
def generate_info_keyboard(Messages,state):
    keyboard = []
    #Split into groups of 2
    for group in chunker(INFO,2):
        result = []
        for element in group:
            result.append(InlineKeyboardButton(text=Messages['menu'][element[0]],callback_data=element[1]))
        keyboard.append(result)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Let user select their preferred language, store in database
def generate_lang_keyboard(grp=''):
    #group variable is to separate changing language personally VS group
    keyboard = []
    for group in chunker(ALL_LANGS,3):
        result = []
        for element in group:
            result.append(InlineKeyboardButton(text=LANGEMOTES[element],
                                               callback_data=('#db|' + grp + '|' + element if grp else '#da'+element)))
        keyboard.append(result)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Menu related queries
def generate_menu_keyboard(Messages,state):
    keyboard = []
    #Split into groups of 2
    for group in chunker(MENU,2):
        result = []
        for element in group:
            #Replace state with backward arrow icon
            if element[1] == state:
                result.append(InlineKeyboardButton(text=Messages['menu']['back'],callback_data='#-1'))
            else:
                result.append(InlineKeyboardButton(text=Messages['menu'][element[0]],callback_data=element[1]))
        keyboard.append(result)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)




#############################
##### GENERATE KEYBOARD #####
#############################

#generate inline keyboard for callback queries
def generate_keyboard(Messages, agentName, choice, data):
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
        result.append([InlineKeyboardButton(text=agent.get_idty_query(),
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
    Messages = LANG[self.userID]
    if data == 'startQuery':
        if isinstance(self,Healer):
            if self.ultAvail:
                message = Messages['query']['doWhat']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'3options',players))
            else:
                message = Messages['query']['doWhat']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'attHeal',players))
        else:
            if self.ultAvail:
                message = Messages['query']['canUlt']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'ultOption',players))
            else:
                message = Messages['query']['attack']
                markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'attack',players))

    elif data =='healerOptionsAfterUlt':
        message = Messages['query']['doWhatNext']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'attHeal',players))
        
    elif data == 'heal':
        message = Messages['query']['heal']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'heal',players))
        
    elif 'ult' in data:
        if mode == 'single':
            message = Messages['query']['ult'][self.agentName]
            markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'ult',players))

        elif mode == 'multi': #Ult data will be (ult,%d) where %d is the nth target to use his ability on
            num = int(data[1])
            message = Messages['query']['select'][min(4,num)]%(num) + Messages['query']['ult'][self.agentName]
            keyboard = generate_keyboard(Messages,self.agentName,'ult|'+str(num),players)
            if num > 1: #Add a 'I'm done' option
                keyboard.append([InlineKeyboardButton(text=Messages['none'],callback_data='{NONE}')])
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    else:
        message = Messages['query']['attack']
        markup = InlineKeyboardMarkup(inline_keyboard = generate_keyboard(Messages,self.agentName,'attack',players))

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
