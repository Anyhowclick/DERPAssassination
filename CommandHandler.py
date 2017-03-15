import asyncio
import telepot
from telepot.aio.delegate import *
from telepot.aio.routing import *
from telepot.namedtuple import *
import threading
from Messages import EN, ALL_LANGS, send_message
from Admin import check_admin, check_spam, get_maintenance, toggle_maintenance, get_grp_info
from Database import DB, LANG, load_preferences, set_lang, save_lang

# Function to group elements together by iterating through sequence
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# CommandHandler handles all text commands addressed to the bot
class CommandHandler(object):
    def __init__(self,bot):
        self.bot = bot

# To verify that the command is meant for this bot
    def verify(self, msg, name):
        return True if ('DERPAssassinBot' in name or 'DERPAssBetaBot' in name) or (not name and msg['chat']['type']=='private') else False

# Route accordingly. If private msg, then send privately, else should send in the grp chat
    def get_ID(self,msg):
        return msg['from']['id'] if msg['chat']['type'] == 'private' else msg['chat']['id']

# Methods are sorted by alphabetical order, but special handlers are placed at the bottom

# Gives information about me! =)
    async def on_about(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return

        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')
        
        if self.verify(msg, name):
            await send_message(self.bot.bot,ID,LANG[ID]['about'],parse_mode='HTML')
            self.bot.close()
            return

# Gives information about the agents. Command is only to be used in private chat
    async def on_agents(self, msg, name):
        ID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return
        
        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')

        Messages = LANG[ID]
        if msg['chat']['type']!='private':
            await send_message(self.bot.bot,ID,Messages['notPrivateChat'])
            return
        
        elif self.verify(msg, name):
            keyboard = []
            for group in chunker(Messages['agentNames'],2):
                result = []
                for element in group:
                    result.append(InlineKeyboardButton(text=element,callback_data=element))
                keyboard.append(result)
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            await send_message(self.bot.bot,ID,Messages['findOutChar'],
                                          reply_markup = markup)
            self.bot.close()

#To initialise admin stuff --> DON"T LOSE YOUR WAYYYYY. YOUR MINDDDDD
    async def on_dlyw81(self, msg, name):
        if int(msg['from']['id']) == 28173774:
            load_preferences() #Load preferences
            self.bot.scheduler.event_later(0, ('_auto_update', {'seconds': 0})) #Start auto update script in CommandHandler, which is routed to Admin.py
            #The function is placed in ChatManager for continual scheduling of the task every hour
            toggle_maintenance()
            await self.bot.sender.sendMessage(EN['initialise'])
        return

# Funding the development of this game!
    async def on_donate(self, msg, name):
        if await check_spam(self.bot,msg):
            return

        ID = msg['from']['id']
        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')
            
        if self.verify(msg, name):
            await self.bot.sender.sendMessage(LANG[ID]['donate'],disable_web_page_preview=True)
            self.bot.close()

#SPECIAL COMMAND to close bot for maintenance
    async def on_fixstuff81(self, msg, name):
        if int(msg['from']['id']) == 28173774:
            await self.bot.sender.sendMessage(EN['maintenance']['OK'])
            toggle_maintenance()
        self.bot.close()
        return

#Command to get groups to join
    async def on_groups(self, msg, name):
        if await check_spam(self.bot,msg):
            return
        ID = msg['from']['id']
        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')

        message = LANG[ID]['groups']
        grps = get_grp_info()
        for key in list(grps.keys()):
            result = grps[key]
            message += result['link'] + result['title'] + '</a>\n'
            message += LANG[ID]['groupsMemberCount']%(result['members'])
        await send_message(self.bot.bot,self.get_ID(msg),message)
        self.bot.close()
        return
    
# Let GameHandler take the command, will ignore
    async def on_join(self, msg, name):
        ID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return

        #Note that if message is in group chat, GameHandler will handle
        if msg['chat']['type'] == 'private':
            if ID not in LANG: #default language will be english
                save_lang(ID,'EN')
            await send_message(self.bot.bot,ID,LANG[ID]['privateChat'])

        elif self.verify(msg, name):
            self.bot.close()

# Will send message if used in private chat, else let GameHandler take command
    async def on_newgame(self, msg, name):
        ID = msg['from']['id']

        if await check_spam(self.bot,msg):
            return
        
        if msg['chat']['type'] == 'private':
            if ID not in LANG: #default language will be english
                save_lang(ID,'EN')
            await send_message(self.bot.bot,ID,LANG[ID]['lonely'])

        elif self.verify(msg, name):
            self.bot.close()

# Rate the game!
    async def on_rate(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return

        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')
        
        await send_message(self.bot.bot,ID,LANG[ID]['rate'])
        self.bot.close()
        return

# Rules of the game
    async def on_rules(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return

        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')

        if msg['chat']['type'] == 'private': #Give the full version of rules
            await send_message(self.bot.bot,ID,LANG[ID]['rulesPrivate'])
        else: #Give the TLDR version
            await send_message(self.bot.bot,ID,LANG[ID]['rulesGroup'])
        self.bot.close()
        return

# Set language
    async def on_setlang(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        if msg['chat']['type'] == 'private':
            await set_lang(self.bot.bot,ID)
        elif msg['chat']['type'] == 'group' or 'supergroup':
            if not await check_admin(self.bot.bot,ID,msg['from']['id']):
                return
            await set_lang(self.bot.bot,ID)
        self.bot.close()
        return

        
# Default text user sees upon starting PM
    async def on_start(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        elif self.verify(msg, name):
            #ask for language preference if it hasn't been captured
            if ID not in LANG:
                await set_lang(self.bot.bot,ID,start=True)
                return
        await send_message(self.bot.bot,ID,LANG[ID]['start'],parse_mode='HTML')
        self.bot.close()
        return

    async def on_stats(self, msg, name):
        #if int(msg['from']['id']) == 28173774:
            #await self.bot.sender.sendMessage()
        self.bot.close()
        return

# Story behind the game
    async def on_story(self, msg, name):
        ID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return

        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')

        Messages = LANG[ID]
        if msg['chat']['type']!='private':
            await send_message(self.bot.bot,ID,Messages['notPrivateChat'])
            return
        elif self.verify(msg, name):
            await send_message(self.bot.bot,ID,Messages['story'])
            self.bot.close()
        return

# Bot support
    async def on_support(self, msg, name):
        ID = self.get_ID(msg)

        if await check_spam(self.bot,msg):
            return

        if ID not in LANG: #default language will be english
            save_lang(ID,'EN')

        await send_message(self.bot.bot,ID,LANG[ID]['support'],parse_mode='HTML')
        self.bot.close()
        return
        
####################
##SPECIAL HANDLERS##
####################
    async def on_invalid_text(self, msg):
        return

    async def on_invalid_command(self, msg, name):
        return


