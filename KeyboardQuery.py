from telepot.namedtuple import *
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

STATS = [
    ('personal','#ca'),
    ('global','#cb'),
    ('back','#-1')
    ]
#Return the corresponding key to the data
def get_menu_key(data):
    for i in MENU:
        if i[1] == data:
            return i[0]
    return 'Error'

def generate_agent_info(Messages,agentCode):
    message = Messages['agents'][agentCode]
    #Handling healer class, because got extra attribute
    if '#bc' in agentCode:
        message=Messages['agentDescriptionHealer']%(
        message[0],message[1],message[2],message[3],message[4],message[6],message[5]
        )
    else:
        message = Messages['agentDescription']%(
        message[0],message[1],message[2],message[3],message[5],message[4]
        )
    return message

#############################
##### GENERATE KEYBOARD #####
#############################
#generate inline keyboard for action phases
def generate_action_keyboard(Messages, choice, players, mode):
    #Choice = type of option to generate, and to store as callback data
    #Players = list of players available for attacking
    #mode = game mode, for future use.

    if choice == '3options': #for healers, when ult is available, can choose to attack, use ability or heal
        return [[InlineKeyboardButton(text=Messages['attHealOption']['att'],callback_data="{ATTACK}"),
                InlineKeyboardButton(text=Messages['attHealOption']['heal'],callback_data="{HEAL}"),
                 InlineKeyboardButton(text=Messages['attHealOption']['ult'],callback_data="{|ULTYES|}")]
                ]

    elif choice == 'attHeal':  #for healers, ult not available
        return [[InlineKeyboardButton(text=Messages['attHealOption']['att'],callback_data="{ATTACK}"),
                InlineKeyboardButton(text=Messages['attHealOption']['heal'],callback_data="{HEAL}")]
                ]

    elif choice == 'ultOption': #See if person wants to use ult or not
        return [[InlineKeyboardButton(text=Messages['yes'],callback_data="{|ULTYES|}"),
                InlineKeyboardButton(text=Messages['no'],callback_data="{ULTNO}")]
                ]

    #For other options, callback data has the data structure: {|choice|targetAgentUserID|}. '|' is used as a separator
    #Choice = attack, ult, ult|num or heal.
    #ult|num is to handle multiple targets
    result = []        
    for agent in players:
        result.append([InlineKeyboardButton(text=agent.get_idty_query(),
                                            callback_data="{|"+choice+"|"+str(agent.userID)+"|}")])
    return result


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
    HERO_INFO = Messages['agents']
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

#Stats query
def generate_stats_keyboard(Messages):
    keyboard = []
    #Split into groups of 2
    for group in chunker(STATS,2):
        result = []
        for element in group:
            result.append(InlineKeyboardButton(text=Messages['menu'][element[0]],callback_data=element[1]))
        keyboard.append(result)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
