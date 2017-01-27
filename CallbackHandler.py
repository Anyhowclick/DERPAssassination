import asyncio
import telepot
import time
from telepot.aio.routing import *
from telepot.namedtuple import *
from Messages import Messages, send_message, edit_message
from Database import DB

# Function to group elements together by iterating through sequence
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

class CallbackHandler(telepot.aio.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_callback_query(self, msg):
        queryID, fromID, queryData = telepot.glance(msg, flavor='callback_query')

        ################################
        ##### AGENT INFO CALLBACKS #####
        ################################
        if queryData in Messages['agentNames']:
            text = Messages['agentDescription'][queryData]
            text += "\n\nWould you like to find out about other agents?"
            markup = InlineKeyboardMarkup(inline_keyboard=
                                          [[InlineKeyboardButton(text="Yes",callback_data="Yes"),
                                           InlineKeyboardButton(text="No",callback_data="No")]
                                           ])
            
            await edit_message(self.editor,text,reply_markup=markup,parse_mode='HTML')

        elif queryData == "Yes":
            await self.editor.editMessageReplyMarkup(reply_markup=None)
            keyboard = []
            #Code reuse from CommandHandler.on_agents method
            for group in chunker(Messages['agentNames'],2):
                result = []
                for element in group:
                    result.append(InlineKeyboardButton(text=element,callback_data=element))
                keyboard.append(result)
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            await send_message(self.bot,fromID,Messages['findOutChar'],reply_markup = markup)

        elif queryData == "No":
            await self.editor.editMessageReplyMarkup(reply_markup=None)
            await send_message(self.bot,fromID,'Alright.')
            self.close()

        ##################################
        ##### GAME-RELATED CALLBACKS #####
        ##################################
        elif '{' in queryData:
            #Retreive stored hero and game object in userID from DB
            agent,game = DB[fromID]
            #Time given in message is the time the message was sent, which is more or less the same for all
            #so have to use own time
            date = int(time.time())
            
            if queryData == '{ULTYES}':
                await agent.editor.editMessageReplyMarkup(reply_markup=None) #no acknowledgement message
                await send_message(self.bot,fromID,Messages['abilityUsed'],parse_mode='HTML')
                queryData = queryData[:-1] + '|'+ str(date) + '|}' #so structure becomes {ULTYES|date|}
                
            #If callback data is just an option to call another query
            elif queryData ==  '{ULTNO}':
                await agent.editor.editMessageReplyMarkup(reply_markup=None)
                await send_message(self.bot,fromID,Messages['abilityNotUsed'],parse_mode='HTML')

            elif queryData == '{NONE}':
                await agent.editor.editMessageReplyMarkup(reply_markup=None)
                await send_message(self.bot,fromID,Messages['acknowledgement'],parse_mode='HTML')
                self.close()
                return

            elif queryData in ('{ATTACK}','{HEAL}'):
                await agent.editor.editMessageReplyMarkup(reply_markup=None)
                
            else: #callback data has the data structure: agentName{|targetAgentName|option|}
                await edit_message(agent.editor,Messages['choiceAccept']%(queryData.split('|')[1]),
                                                   reply_markup=None,
                                                   parse_mode='HTML')
                queryData = queryData[:-1] + str(date) + '|}' #so structure becomes agentName{|targetAgentName|option|date|}
                
            await agent.process_query(game,queryData) #send to agent object for processing
            self.close()
            
