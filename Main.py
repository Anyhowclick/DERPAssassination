import asyncio
import telepot
import aiohttp
from telepot.aio.delegate import *
from ChatManager import chatManager
from CallbackHandler import CallbackHandler
from GameHandler import gameHandler

'''
chatManager handles all '/' non-game related commands,
to be routed to CommandHandler.

CallbackHandler handles all callback queries, including
game-related ones (user choices)

gameHandler manages /start (to get user + private chat IDs),
/newgame, /join and /killgame, as well as the running of game in general.

This is the main file that initialises the bot, and the script to run
to start the bot.

'''
TOKEN = 'YOUR TOKEN HERE'

DERPAssBot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(per_chat_id(), create_open, chatManager, timeout=30),
    pave_event_space()(
        per_callback_query_origin(), create_open, CallbackHandler, timeout=180),
    pave_event_space()(
        per_chat_id(types=['group','supergroup']), create_open, gameHandler,timeout=9999),
])


##################################
####### FOR PYTHONANYWHERE #######
##################################
#proxy_url = "http://proxy.server:3128"

#telepot.aio.api._pools = {
#    'default': aiohttp.ProxyConnector(proxy=proxy_url, limit=999)
#}

#telepot.aio.api._onetime_pool_spec = (aiohttp.ProxyConnector, dict(proxy=proxy_url, force_close=True))

###################################
loop = asyncio.get_event_loop()
loop.create_task(DERPAssBot.message_loop())
print('LEGGO!!')

loop.run_forever()
