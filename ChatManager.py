import asyncio
import telepot
import pprint
from telepot.aio.routing import *
from CommandHandler import CommandHandler

# ChatManager routes messages according to 1) message flavour 2) content type
class chatManager(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Then route by commands (handled by CommandHandler)
        commandHandler = CommandHandler(self)
        commandRouter =  telepot.aio.helper.Router(lower_key(by_chat_command(separator='@',pass_args=True)),
                                             make_routing_table(commandHandler, [
                                                 'about',
                                                 'agents',
                                                 'dlyw81',
                                                 'donate',
                                                 'fixstuff81',
                                                 'future',
                                                 'newgame',
                                                 'join',
                                                 'rate',
                                                 'rules',
                                                 'setlang',
                                                 'start',
                                                 'stats',
                                                 'story',
                                                 'support',
                                                 ((None,), commandHandler.on_invalid_text),
                                                 (None, commandHandler.on_invalid_command),
                                             ]))
        #Initialise router
        contentTypeRouter = telepot.aio.helper.Router(by_content_type(),make_content_type_routing_table(self))
        contentTypeRouter.routing_table['text'] = commandRouter.route
        contentTypeRouter.routing_table['new_chat_member'] = self.on_new_chat_member
     
        #Assign router to routing table
        self.router.routing_table['chat'] = contentTypeRouter.route
        

    #Define other non-essential methods
    async def on_new_chat_member(self,msg,name):
        return

    async def on_left_chat_member(self,msg,name):
        return

    async def on_new_chat_title(self,msg,name):
        return

    async def on_location(self,msg,name):
        return

    async def on_delete_chat_photo(self,msg,name):
        return
    
    async def on_new_chat_photo(self,msg,name):
        return

    async def on_new_pinned_message(self,msg,name):
        return    
    
    async def on_photo(self,msg,name):
        return

    async def on_video(self,msg,name):
        return

    async def on_voice(self,msg,name):
        return

    async def on_sticker(self,msg,name):
        return    
