import asyncio
import telepot
import Globals
Globals.init()
from telepot.aio.delegate import *
from Admin import toggle_maintenance
from ChatManager import chatManager
from CallbackHandler import CallbackHandler
from DatabaseStats import load_database, update_dict, auto_save_update
from GameHandler import gameHandler

'''
chatManager handles all '/' non-game related commands
(also ensures /newgame and /join are used in appopriate chats).

CallbackHandler handles all callback queries, including
game-related ones (user choices)

gameHandler manages /start (to get user + private chat IDs),
/newgame and /join, as well as the running of game in general.

This is the main file that initialises the bot, and the script to run
to start the bot.

'''
TOKEN = '442071087:AAERIPN4vPFcxQVf_H8NK4igur413PCQ-uQ'

DERPAssBot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(per_chat_id(), create_open, chatManager, timeout=197),
    pave_event_space()(
        per_callback_query_origin(), create_open, CallbackHandler, timeout=239),
    pave_event_space()(
        per_chat_id(types=['group','supergroup']), create_open, gameHandler,timeout=5419),
])

loop = asyncio.get_event_loop()
loop.create_task(DERPAssBot.message_loop())
loop.create_task(update_dict())
loop.create_task(auto_save_update())
load_database()
toggle_maintenance()
print('LEGGO!!')
loop.run_forever()
