import asyncio
import telepot
import time
from telepot.aio.routing import *
from telepot.namedtuple import *
from Messages import ALL_LANGS, send_message, edit_message
from Database import DB, LANG, save_lang
from Admin import check_admin

# Function to group elements together by iterating through sequence
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

class CallbackHandler(telepot.aio.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_callback_query(self, msg):
        queryID, ID, queryData = telepot.glance(msg, flavor='callback_query')
        ################################
        ###### LANGUAGE CALLBACKS ######
        ################################
        if '@@' in queryData: #Eg. EN@@, IN@@
            save_lang(ID,queryData[:-2])
            await edit_message(self.editor,LANG[ID]['start'],reply_markup=None,parse_mode='HTML')
            return
        
        elif queryData in ALL_LANGS:
            chatID = int(msg['message']['chat']['id'])
            if chatID < 0:
                if not await check_admin(self.bot,chatID,ID):
                    return
                text = save_lang(chatID,queryData)
            else:
                text = save_lang(ID,queryData)
            await edit_message(self.editor,text,reply_markup=None,parse_mode='HTML')
            self.close()
            return

        Messages = LANG[ID]
        ################################
        ##### AGENT INFO CALLBACKS #####
        ################################
        
        if queryData in Messages['agentNames']:
            text = Messages['agentDescription'][queryData]
            text += Messages['findOutMoreChar']
            markup = InlineKeyboardMarkup(inline_keyboard=
                                          [[InlineKeyboardButton(text=Messages['yes'],callback_data=Messages['yes']),
                                           InlineKeyboardButton(text=Messages['no'],callback_data=Messages['no'])]
                                           ])
            
            await edit_message(self.editor,text,reply_markup=markup,parse_mode='HTML')
            self.close()
            
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
            await send_message(self.bot,ID,Messages['findOutChar'],reply_markup = markup)

        elif queryData == "No":
            await self.editor.editMessageReplyMarkup(reply_markup=None)
            await send_message(self.bot,ID,'Alright.')
            self.close()

        ##################################
        ##### GAME-RELATED CALLBACKS #####
        ##################################
        elif '{' in queryData:
            #Retreive stored hero and game object in userID from DB
            agent,game = DB[ID]
            #Time given in message is the time the message was sent, which is more or less the same for all
            #so have to use own time
            date = int(time.time())
            
            if queryData == '{ULTYES}':
                await edit_message(agent.editor,Messages['abilityUsed'],parse_mode='HTML',reply_markup=None)
                queryData = queryData[:-1] + '|'+ str(date) + '|}' #so structure becomes {ULTYES|date|}
                
            #If callback data is just an option to call another query
            elif queryData ==  '{ULTNO}':
                await edit_message(agent.editor,Messages['abilityNotUsed'],parse_mode='HTML',reply_markup=None)

            elif queryData == '{NONE}':
                await edit_message(agent.editor,Messages['acknowledgement'],parse_mode='HTML',reply_markup=None)
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
            
