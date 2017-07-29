import asyncio
import telepot
import pprint
from telepot.aio.routing import *
from CommandHandler import CommandHandler
from Admin import auto_update
import Globals
from DatabaseStats import add_new_group

# ChatManager routes messages according to 1) message flavour 2) content type
class chatManager(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #Then route by commands (handled by CommandHandler)
        commandHandler = CommandHandler(self)
        commandRouter =  telepot.aio.helper.Router(lower_key(by_chat_command(separator='@',pass_args=True)),
                                             make_routing_table(commandHandler, [
                                                 'config',
                                                 'fixstuff81',
                                                 'join',
                                                 'menu',
                                                 'newgame',
                                                 'start',
                                                 ((None,), commandHandler.on_invalid_text),
                                                 (None, commandHandler.on_invalid_command),
                                             ]))
        #Initialise router
        contentTypeRouter = telepot.aio.helper.Router(by_content_type(),make_content_type_routing_table(self))
        contentTypeRouter.routing_table['text'] = commandRouter.route

        #Assign router to routing table
        self.router.routing_table['chat'] = contentTypeRouter.route

    #Define other non-essential methods, in no particular order
    async def on_audio(self,msg,name):
        return

    async def on_contact(self,msg,name):
        return
    
    async def on_delete_chat_photo(self,msg,name):
        return

    async def on_document(self,msg,name):
        return
    
    async def on_left_chat_member(self,msg,name):
        return

    async def on_location(self,msg,name):
        return

    async def on_new_chat_member(self,msg,name):
        return

    async def on_new_chat_photo(self,msg,name):
        return
    
    async def on_new_chat_title(self,msg,name):
        ID = msg['chat']['id']
        
        try:
            Globals.GRPID[ID]
            await Globals.QUEUE.put((Globals.GRPID[ID],'title',msg['new_chat_title']))
        except KeyError:
            await add_new_group(ID,msg)
        self.close()
        return
    
    async def on_new_pinned_message(self,msg,name):
        return

    async def on_photo(self,msg,name):
        return

    async def on_pinned_message(self,msg,name):
        return

    async def on_sticker(self,msg,name):
        return
    
    async def on_video(self,msg,name):
        return

    async def on_voice(self,msg,name):
        return
