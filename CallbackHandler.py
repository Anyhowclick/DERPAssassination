import asyncio
import telepot
import time
from telepot.aio.routing import *
from telepot.namedtuple import *
from Messages import ALL_LANGS, setLang, edit_message, EN
from KeyboardQuery import *
from DatabaseStats import save_lang
import Globals
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
        queryID, ID, queryData = telepot.glance(msg, flavor='callback_query')
        print(queryData)

        try:
            Messages = Globals.LANG[ID]
        except KeyError:
            Messages = EN #Set default to English
            
        #First check maintenance status
        if get_maintenance():
            await edit_message(self.editor,Messages['maintenance']['status'],reply_markup=None,parse_mode='HTML')
            return
        
        ##################################
        ##### GAME-RELATED CALLBACKS #####
        ##################################
        if '~' in queryData:
            try:
                agent,game = Globals.DBP[ID]
                Messages = game.Messages
                if queryData == '~POWUP~':
                    game.powUp.add(agent)
                    await game.bot.answerCallbackQuery(queryID, text=Messages['powerUp']['yes'], show_alert=True)
                    await edit_message(game.messageEditor,
                                       Messages['powerUp'][game.powerUp.name]['desc'].format(
                                           game.powerUp.limit,len(game.powUp)),
                                       reply_markup=generate_powerUp_keyboard(Messages) if game.powOn else None)
                    self.close()
                    return
            
                elif queryData == '~POWDOWN~':
                    game.powUp.remove(agent)
                    await game.bot.answerCallbackQuery(queryID, text=Messages['powerUp']['no'], show_alert=True)
                    await edit_message(game.messageEditor,
                                       Messages['powerUp'][game.powerUp.name]['desc'].format(
                                           game.powerUp.limit,len(game.powUp)),
                                       reply_markup=generate_powerUp_keyboard(Messages) if game.powOn else None)
                    self.close()
                    return

            except KeyError:
                self.close()
                return
            
        elif '{' in queryData:
            #Retreive stored hero and game object in userID from DB
            agent,game = Globals.DBP[ID]
            #Time given in message is the time the message was sent, which is more or less the same for all
            #so have to use own time
            date = int(time.time())
                                           
            if queryData == '{|ULTYES|}':
                await edit_message(agent.editor,Messages['abilityUsed'],parse_mode='HTML',reply_markup=None)
                queryData = queryData[:-1] + str(date) + '|}' #so structure becomes {|ULTYES|date|}
                
            #If callback data is just an option to call another query
            elif queryData ==  '{ULTNO}':
                await edit_message(agent.editor,Messages['abilityNotUsed'],parse_mode='HTML',reply_markup=None)

            #Person decides to stop using ult
            elif queryData == '{NONE}':
                await edit_message(agent.editor,Messages['acknowledgement'],parse_mode='HTML',reply_markup=None)
                self.close()
                return

            elif queryData in ('{ATTACK}','{HEAL}'):
                try:
                    await agent.editor.editMessageReplyMarkup(reply_markup=None)
                except AttributeError:
                    pass
                
            else: #callback data has the data structure: {|choice|targetAgentID|}
                #Handle exception for multi-ult
                agentID = queryData.split('|')
                if len(agentID[2]) <= 2:
                    agentID = int(agentID[3])
                else:
                    agentID = int(agentID[2])
                await edit_message(agent.editor,Messages['choiceAccept']%(game.agents[agentID].agentName),
                                                   reply_markup=None,
                                                   parse_mode='HTML')
                queryData = queryData[:-1] + str(date) + '|}' #so structure becomes {|choice|targetAgentID|date|}

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
        ###Info###
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
            message = generate_agent_info(Messages,queryData) #queryData = agentCode, function found in KeyboardQuery
            await edit_message(self.editor,message,reply_markup=markup,parse_mode='HTML')
            self.close()
            return

        ###########
        ###Stats###
        ###########
        elif queryData == '#c0':
            markup = generate_stats_keyboard(Messages)
            await edit_message(self.editor,Messages['stats']['query'],reply_markup=markup,parse_mode='HTML')
            self.close()
            return

        elif '#c' in queryData:
            markup = generate_back_keyboard(Messages,queryData)
            if ID == 28173774:
                #get local stats
                message = Messages['stats']['local']
                d = Globals.LOCALID[ID]
                if d['normalGamesPlayed']:
                    p = (d['derpNormalWins']/d['normalGamesPlayed']*100,
                         d['drawsNormal']/d['normalGamesPlayed']*100,
                         d['pyroNormalWins']/d['normalGamesPlayed']*100,
                         d['normalGamesSurvived']/d['normalGamesPlayed']*100
                         )
                else:
                    p = (0,0,0,0)
                message = message.format(d=d,p=p)
                
                #Get no. of groups and players playing
                activeGrps, activePlayers = 0,0
                for grp in Globals.DBG:
                    if Globals.DBG[grp]:
                        activeGrps += 1
                for player in Globals.DBP:
                    if Globals.DBP[player]:
                        activePlayers += 1
                message += Messages['stats']['des'].format(activeGrps,activePlayers)
                
                #Finally, get global stats
                d = Globals.GLOBAL_STATS
                totalGames = d['derpWins'] + d['pyroWins'] + d['drawsNormal']
                if totalGames == 0:
                    p = (0,0,0,0)
                else:
                    p = (totalGames,d['derpWins']/totalGames*100,d['pyroWins']/totalGames*100,d['drawsNormal']/totalGames*100)
                message += Messages['stats']['global'].format(d=d,p=p)
                await edit_message(self.editor,message,reply_markup=markup,parse_mode='HTML')
                self.close()
                return
            if queryData == '#ca': #Local stats
                #get local stats
                d = Globals.LOCALID[ID]
                if d['normalGamesPlayed']:
                    p = (d['derpNormalWins']/d['normalGamesPlayed']*100,
                         d['drawsNormal']/d['normalGamesPlayed']*100,
                         d['pyroNormalWins']/d['normalGamesPlayed']*100,
                         d['normalGamesSurvived']/d['normalGamesPlayed']*100
                         )
                else:
                    p = (0,0,0,0)
                await edit_message(self.editor,Messages['stats']['local'].format(d=d,p=p),reply_markup=markup,parse_mode='HTML')
                self.close()
                return
            else: #Global stats
                d = Globals.GLOBAL_STATS
                totalGames = d['derpWins'] + d['pyroWins'] + d['drawsNormal']
                if totalGames == 0:
                    p = (0,0,0,0)
                else:
                    p = (totalGames,d['derpWins']/totalGames*100,d['drawsNormal']/totalGames*100,d['pyroWins']/totalGames*100)
                await edit_message(self.editor,Messages['stats']['global'].format(d=d,p=p),reply_markup=markup,parse_mode='HTML')
                self.close()
                return
        
        ############
        ###Config###
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
            Messages = Globals.LANG[ID]
            markup = generate_menu_keyboard(Messages,-1)
            await edit_message(self.editor,Messages['start'],reply_markup=markup,parse_mode='HTML')
            self.close()
            return
        
        #SET / CHANGE LANGUAGE for group
        elif '#db' in queryData: #Eg. db|-12345678|IN
            queryData = queryData.split('|')
            await save_lang(queryData[1],queryData[2])
            Messages = Globals.LANG[ID]
            markup = generate_config_keyboard(Messages,'#-1',queryData[1])
            await edit_message(self.editor,Messages['config']['intro']%(Globals.GRPID[int(queryData[1])]['title']),reply_markup=markup,parse_mode='HTML')
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
                message += Globals.LANG[ID]['groupsMemberCount']%(result['members'])
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
            
