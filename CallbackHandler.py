import asyncio
import telepot
import time
from telepot.aio.routing import *
from telepot.namedtuple import *
from Messages import ALL_LANGS, setLang, send_message, edit_message, EN
from KeyboardQuery import *
from DatabaseStats import save_lang
import DatabaseStats
from Admin import check_admin, check_spam, get_maintenance, get_grp_info

# Function to group elements together by iterating through sequence
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

#Callback queries are split into 3 types:
#1. Configuration --> Changing settings (starting with @@)
#1. Menu --> Anything related to the navigation of the menu (starting with #)
#2. Game --> Game-related queries



class CallbackHandler(telepot.aio.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_callback_query(self, msg):
        LOCALID = DatabaseStats.LOCALID
        GRPID = DatabaseStats.GRPID
        LANG = DatabaseStats.LANG
        DBP = DatabaseStats.DBP
        DBG = DatabaseStats.DBG
        queryID, ID, queryData = telepot.glance(msg, flavor='callback_query')

        try:
            Messages = LANG[ID]
        except KeyError:
            Messages = EN #Set default to English
            
        #First check maintenance status
        if get_maintenance():
            await edit_message(self.editor,Messages['maintenance']['status'],reply_markup=None,parse_mode='HTML')
            return
        
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
                try:
                    await agent.editor.editMessageReplyMarkup(reply_markup=None)
                except AttributeError:
                    pass
            else: #callback data has the data structure: agentName{|targetAgentName|option|}
                await edit_message(agent.editor,Messages['choiceAccept']%(queryData.split('|')[1]),
                                                   reply_markup=None,
                                                   parse_mode='HTML')
                queryData = queryData[:-1] + str(date) + '|}' #so structure becomes agentName{|targetAgentName|option|date|}
                
            await agent.process_query(game,queryData) #send to agent object for processing
            self.close()

        ##############################
        ###### CHECK IF SPAMMED ######
        ##############################
        if await check_spam(self,msg):
            await edit_message(self.editor,Messages['spam'][2],reply_markup=None,parse_mode='HTML')
            self.close()
            return
        
        #########################
        ##### MENU CALLBACK #####
        #########################
        print(queryData)
        ##########
        ###BACK###
        ##########
        #To return to previous menu page (Back button pressed)
        if queryData == '#-1':
            markup = generate_menu_keyboard(Messages,queryData)
            await edit_message(self.editor,Messages['start'],reply_markup=markup,parse_mode='HTML')
            self.close()
            return
        
        ##########
        ###INFO###
        ##########
        elif queryData == '#a0':
            markup = generate_info_keyboard(Messages,queryData)
            await edit_message(self.editor,Messages['info'],reply_markup=markup,parse_mode='HTML')
            self.close()
            return

        ###########
        ###Rules###
        ###########
        elif queryData == '#aa':
            markup = generate_back_keyboard(Messages,queryData)
            await self.bot.sendPhoto(ID,Messages['rules']['fileID'])
            await edit_message(self.editor,Messages['rules']['sent'],reply_markup=markup)
            self.close()
            return
        
        ############
        ###Agents###
        ############
        elif queryData == '#b0':
            markup = generate_agent_keyboard(Messages,queryData)
            await edit_message(self.editor,Messages['findOutChar'],reply_markup=markup,parse_mode='HTML')
            self.close()
            return

        elif '#b' in queryData:
            markup = generate_agent_keyboard(Messages,queryData)
            message = OrderedDict(Messages['agents'])[queryData]
            
            #Handling healer class, because got extra attribute
            if '#bc' in queryData:
                message=Messages['agentDescriptionHealer']%(
                    message[0],message[1],message[2],message[3],message[4],message[6],message[5]
                    )
            else:
                message = Messages['agentDescription']%(
                    message[0],message[1],message[2],message[3],message[5],message[4]
                    )
            await edit_message(self.editor,message,reply_markup=markup,parse_mode='HTML')
            self.close()
            return

        ############
        ###CONFIG###
        ############
        #Separate keyboards so that I know whether to save language for the person, or for the group
        if queryData == '#d0' or '#d1' in queryData:
            if queryData == '#d0':
                markup = generate_lang_keyboard()
            else:
                queryData = queryData.split('|')[1]
                markup = generate_lang_keyboard(grp=queryData) 
            await edit_message(self.editor,setLang,reply_markup=markup,parse_mode='HTML')
            self.close()
            return
        
        #SET / CHANGE LANGUAGE for personal
        elif '#da' in queryData: #Eg. #da0EN
            await save_lang(ID,queryData[-2:])
            Messages = LANG[ID]
            markup = generate_menu_keyboard(Messages,-1)
            await edit_message(self.editor,Messages['start'],reply_markup=markup,parse_mode='HTML')
            self.close()
            return
        
        #SET / CHANGE LANGUAGE for group
        elif '#db' in queryData: #Eg. db|-12345678|IN
            queryData = queryData.split('|')
            await save_lang(queryData[1],queryData[2])
            Messages = LANG[ID]
            markup = generate_config_keyboard(Messages,'#-1',queryData[1])
            await edit_message(self.editor,Messages['config']['intro']%(GRPID[int(queryData[1])]['title']),reply_markup=markup,parse_mode='HTML')
            self.close()
            return
        
        #Exit!
        elif '#-2' in queryData:
            await edit_message(self.editor,Messages['config']['done'],reply_markup=None,parse_mode='HTML')
            self.close()
            return
        
        ############
        ###Groups###
        ############
        elif queryData == '#e0':
            markup = generate_menu_keyboard(Messages,queryData)
            message = Messages['groups']
            grps = await get_grp_info(self.bot)
            #Each item in grps is a tuple as follows: (grpID,{'memberCount':members,'title':GrpTitle,'link':inviteLink})
            for item in grps:
                result = item[1]
                message += result['link'] + result['title'] + '</a>\n'
                message += LANG[ID]['groupsMemberCount']%(result['members'])
            await edit_message(self.editor,message,reply_markup = markup)
            self.close()
            return
        
        #######                                                                                    #######
        ###Information that doesn't require processing (namely support, donate, rate and about buttons)###
        #######                                                                                    #######
        elif queryData in ('#f0','#g0','#h0','#i0'):
            markup = generate_menu_keyboard(Messages,queryData)
            key = get_menu_key(queryData)
            await edit_message(self.editor,Messages[key],reply_markup=markup,parse_mode='HTML')
            self.close()
            return
        
        markup = generate_back_keyboard(Messages,queryData)
        await edit_message(self.editor,Messages['menu']['soon'],reply_markup=markup,parse_mode='HTML')
        self.close()
        return
            
