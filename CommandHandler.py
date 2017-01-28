import asyncio
import telepot
from telepot.aio.delegate import *
from telepot.aio.routing import *
from telepot.namedtuple import *
from Messages import Messages, send_message
from Admin import start_spam, check_spam, on_maintenance
from Database import DB

# Function to group elements together by iterating through sequence
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# CommandHandler handles all text commands addressed to the bot
class CommandHandler(object):
    def __init__(self,bot):
        self.bot = bot

# To verify that the command is meant for this bot
    def verify(self, msg, name):
        return True if ('DERPAssassinBot' in name) or (not name and msg['chat']['type']=='private') else False

# Route accordingly. If private msg, then send privately, else should send in the grp chat
    def get_ID(self,msg):
        return msg['from']['id'] if msg['chat']['type'] == 'private' else msg['chat']['id']

# Methods are sorted by alphabetical order, but special handlers are placed at the bottom

# Gives information about me! =)
    async def on_about(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        elif self.verify(msg, name):
            await send_message(self.bot.bot,ID,Messages['about'],parse_mode='HTML')
            self.bot.close()
            return

# Gives information about the agents. Command is only to be used in private chat
    async def on_agents(self, msg, name):
        userID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return
        elif msg['chat']['type']!='private':
            await send_message(self.bot.bot,userID,Messages['notPrivateChat'])
            return
        elif self.verify(msg, name):
            keyboard = []
            for group in chunker(Messages['agentNames'],2):
                result = []
                for element in group:
                    result.append(InlineKeyboardButton(text=element,callback_data=element))
                keyboard.append(result)
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            await send_message(self.bot.bot,userID,Messages['findOutChar'],
                                          reply_markup = markup)
            self.bot.close()

#To initialise admin stuff --> DON"T LOSE YOUR WAYYYYY. YOUR MINDDDDD
    async def on_dlyw81(self, msg, name):
        if int(msg['from']['id']) == 28173774:
            await self.bot.sender.sendMessage(Messages['spam']['start'])
            start_spam()
        self.bot.close()
        return

# Funding the development of this game!
    async def on_donate(self, msg, name):
        if await check_spam(self.bot,msg):
            return
        elif self.verify(msg, name):
            await self.bot.sender.sendMessage(Messages['donate'],disable_web_page_preview=True)
            self.bot.close()

    async def on_fixstuff81(self, msg, name):
        if int(msg['from']['id']) == 28173774:
            await self.bot.sender.sendMessage(Messages['maintenance']['OK'])
            on_maintenance()
        self.bot.close()
        return

# Planned updates!
    async def on_future(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        await send_message(self.bot.bot,ID,Messages['future'])
        self.bot.close()
        return

# Let GameHandler take the command, will ignore
    async def on_join(self, msg, name):
        userID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return
        elif msg['chat']['type'] == 'private':
            await send_message(self.bot.bot,userID,Messages['privateChat'])
        elif self.verify(msg, name):
            self.bot.close()

# Will send message if used in private chat, else let GameHandler take command
    async def on_newgame(self, msg, name):
        userID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return
        elif msg['chat']['type'] == 'private':
            await send_message(self.bot.bot,userID,Messages['lonely'])
        elif self.verify(msg, name):
            self.bot.close()

# Rate the game!
    async def on_rate(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        await send_message(self.bot.bot,ID,Messages['rate'],parse_mode='HTML')
        self.bot.close()
        return

# Rules of the game
    async def on_rules(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        await send_message(self.bot.bot,ID,Messages['rules'],parse_mode='HTML')
        self.bot.close()
        return

# Default text user sees upon starting PM
    async def on_start(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        elif self.verify(msg, name):
            await send_message(self.bot.bot,ID,Messages['start'],parse_mode='HTML')

# Story behind the game
    async def on_story(self, msg, name):
        userID = msg['from']['id']
        if await check_spam(self.bot,msg):
            return
        elif msg['chat']['type']!='private':
            await send_message(self.bot.bot,userID,Messages['notPrivateChat'])
            return
        elif self.verify(msg, name):
            await send_message(self.bot.bot,userID,Messages['story'])
            self.bot.close()
        return

# Bot support
    async def on_support(self, msg, name):
        ID = self.get_ID(msg)
        if await check_spam(self.bot,msg):
            return
        await send_message(self.bot.bot,ID,Messages['support'],parse_mode='HTML')
        self.bot.close()
        return

####################
##SPECIAL HANDLERS##
####################
    async def on_invalid_text(self, msg):
        return

    async def on_invalid_command(self, msg, name):
        return


