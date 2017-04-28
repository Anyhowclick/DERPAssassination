import asyncio
import telepot
import pprint
from telepot.aio.routing import *
from CommandHandler import CommandHandler
from Admin import auto_update

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
                                                 'groups',
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
        #Assign auto_update_script
        self.router.routing_table['_auto_update'] = self.on__auto_update

    #Calls auto_update script found in Admin.py
    #Updates the no. of members in each group using the /group command, and in the future
    #the stats database
    async def on__auto_update(self,event):
        await auto_update(self)
        print('OK!')
        self.scheduler.event_later(3600, ('_auto_update',{'seconds': 3600}))
        return

    #Define other non-essential methods, in no particular order
    async def on_new_chat_member(self,msg,name):
        return

    async def on_left_chat_member(self,msg,name):
        return

    async def on_pinned_message(self,msg,name):
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

    async def on_document(self,msg,name):
        return

    async def on_photo(self,msg,name):
        return

    async def on_contact(self,msg,name):
        return

    async def on_video(self,msg,name):
        return

    async def on_audio(self,msg,name):
        return

    async def on_voice(self,msg,name):
        return

    async def on_sticker(self,msg,name):
        return
