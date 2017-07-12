import asyncio
import pprint
import telepot
import Globals
from telepot.aio.delegate import *
from telepot.aio.routing import *
from telepot.namedtuple import *
from Messages import EN, setLang, send_message
from KeyboardQuery import *
from Admin import check_admin, check_spam, get_maintenance, toggle_maintenance
from DatabaseStats import add_new_person, save_lang

######################################################################################
####################### TO OBTAIN FILE ID AFTER UPLOAD ###############################
######################################################################################
def equivalent(data, nt):
    if type(data) is dict:
        keys = list(data.keys())

        # number of dictionary keys == number of non-None values in namedtuple?
        if len(keys) != len([f for f in nt._fields if getattr(nt, f) is not None]):
            return False

        # map `from` to `from_`
        fields = list([k+'_' if k in ['from'] else k for k in keys])

        return all(map(equivalent, [data[k] for k in keys], [getattr(nt, f) for f in fields]))
    elif type(data) is list:
        return all(map(equivalent, data, nt))
    else:
        return data==nt
    
def examine(result, type):
    try:
        print('Examining %s ......' % type)

        nt = type(**result)
        assert equivalent(result, nt), 'Not equivalent:::::::::::::::\n%s\n::::::::::::::::\n%s' % (result, nt)

        pprint.pprint(result)
        pprint.pprint(nt)
        print()
    except AssertionError:
        traceback.print_exc()
        print('Do you want to continue? [y]', end=' ')
        answer = input()
        if answer != 'y':
            exit(1)
###########################################################################
###########################################################################

# CommandHandler handles all text commands addressed to the bot
class CommandHandler(object):
    def __init__(self,bot):
        self.bot = bot
        
# To verify that the command is meant for this bot
    def verify(self, msg, name):
        return True if ('DERPAssassinBot' in name or 'CPDPPYBetaBot' in name) or (not name and msg['chat']['type']=='private') else False

# Route accordingly. If private msg, then send privately, else should send in the grp chat
    def get_ID(self,msg):
        return msg['from']['id'] if msg['chat']['type'] == 'private' else msg['chat']['id']

# Methods are sorted by alphabetical order, but special handlers are placed at the bottom

# Set language
    async def on_config(self, msg, name): #Only for group chats to edit group settings
        ID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return
        #Check if user has set language, other defaut to english
        try:
            Globals.LOCALID[ID]
            Messages = Globals.LANG[ID]
        except KeyError:
            Messages = await add_new_person(ID,msg)
        if get_maintenance(): #if maintenance, send bot down msg
            await send_message(self.bot.bot,ID,Messages['maintenance']['shutdown'])
            self.bot.close()
            return

        #Check if private chat
        if msg['chat']['type'] == 'private':
            await send_message(self.bot.bot,ID,Messages['notGroup'])

        #Check for group admin... otherwise send message that they're not group admin
        elif msg['chat']['type'] == 'group' or 'supergroup':
            if not await check_admin(self.bot.bot,msg['chat']['id'],ID):
                await send_message(self.bot.bot,ID,Messages['notGroupAdmin'])
            else:
                #Check if basic group stats have been recorded, otherwise add them into database
                try:
                    Globals.GRPID[msg['chat']['id']] 
                    await Globals.QUEUE.put((Globals.GRPID[msg['chat']['id']],'title',msg['chat']['title'])) #Update group chat title
                except KeyError:
                    Messages = await add_new_group(msg['chat']['id'],msg)

                markup = generate_config_keyboard(Messages,'#-1',msg['chat']['id'])
                await send_message(self.bot.bot,ID,Messages['config']['intro']%(msg['chat']['title']),reply_markup=markup)
        #Finally, shutdown
        self.bot.close()
        return
    
#SPECIAL COMMAND to close bot for maintenance
    async def on_fixstuff81(self, msg, name):
        if int(msg['from']['id']) == 28173774:
            toggle_maintenance()
            stat = get_maintenance()
            await self.bot.sender.sendMessage(EN['maintenance']['status']%stat)
        self.bot.close()
        return
    
# Let GameHandler take the command, will ignore
    async def on_join(self, msg, name):
        ID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return

        #Note that if message is in group chat, GameHandler will handle
        if msg['chat']['type'] == 'private':
            try:
                Messages = Globals.LANG[ID]
            except KeyError:
                Messages = EN
            await send_message(self.bot.bot,ID,Messages['notGroup'])
        self.bot.close()
        return

# Gives information about the agents. Command is only to be used in private chat
    async def on_menu(self, msg, name):
        ID = msg['from']['id']
        if await check_spam(self.bot,msg) or (msg['chat']['type'] != 'private'):
            return
        try:
            Globals.LOCALID[ID]
            Messages = Globals.LANG[ID]
        except KeyError:
            Messages = await add_new_person(ID,msg)
            
        if get_maintenance():
            await send_message(self.bot.bot,ID,Messages['maintenance']['shutdown'])
            return
        
        if self.verify(msg, name):
            markup = generate_menu_keyboard(Messages,-1)
            await send_message(self.bot.bot,ID,
                               Messages['start'],
                               reply_markup = markup)
            self.bot.close()
            
# Will send message if used in private chat, else let GameHandler take command
    async def on_newgame(self, msg, name):
        ID = msg['from']['id']

        if await check_spam(self.bot,msg):
            return
        
        if msg['chat']['type'] == 'private':
            if ID not in Globals.LANG: #default language will be english
                await save_lang(ID,'EN')
            await send_message(self.bot.bot,ID,Globals.LANG[ID]['lonely'])

        elif self.verify(msg, name):
            self.bot.close()

# Rules of the game
    async def on_rules(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        #r = open('rules.jpg','rb')
        #r = await self.bot.bot.sendPhoto(ID, r)
        #examine(r, telepot.namedtuple.Message)
        
# Default text user sees upon starting PM
    async def on_start(self, msg, name):
        ID = self.get_ID(msg)
        if msg['chat']['type'] != 'private':
            return
        if self.verify(msg, name):
            try:
                Globals.LOCALID[ID]
                #Route to menu immediately
                await self.on_menu(msg, name)
            #Otherwise ask for language preference
            except KeyError:
                await add_new_person(ID,msg)
                markup = generate_lang_keyboard()
                await send_message(self.bot.bot,ID,setLang,reply_markup=markup)
        self.bot.close()
        return
        
####################
##SPECIAL HANDLERS##
####################
    async def on_invalid_text(self, msg):
        return

    async def on_invalid_command(self, msg, name):
        return
