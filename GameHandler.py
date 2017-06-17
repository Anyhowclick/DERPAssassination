import asyncio
import telepot
import telepot.aio
import telepot.aio.helper
import math
import time
from telepot.exception import *
from telepot.namedtuple import *
from Game import Game
from Messages import send_message, edit_message, EN
from DatabaseStats import *
import DatabaseStats
from Admin import check_admin, get_maintenance
'''
gameHandler will handle all game-related commands, such
as /newgame, /join, and facilitates the game in creating
and managing events (The different rounds, power-ups event etc.)

Agent stats and abilities are stored in the AgentClasses and Agent
python scripts. Whatever text messages are to be printed will be
imported from Messages
'''

MINPLAYERS = 2 #FOR TESTING
#MINPLAYERS = 3 #FOR IMPLEMENTATION
MAXPLAYERS = 20
QUEUE = DatabaseStats.QUEUE

class gameHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gameRunning = False #Whether a game is running or not. Have issues with using self.game, hence need for boolean
        self.game = None #Game object
        self.players = {} #Users who joined the game (unassigned agents)
        self.messageEditor = None #Message editor
        self.countdownEvent = None #Countdown till game start (to allow people to join)
        self.queued = {} #Users who want to be notified when the game ends
        #Catching countdown events
        self.router.routing_table['_countdown_game_start'] = self.on__countdown_game_start
        self.router.routing_table['_countdown_game_next_round'] = self.on__countdown_game_next_round
        self.router.routing_table['_countdown_collate_result'] = self.on__countdown_collate_result
        self.router.routing_table['_power_up'] = self.on__power_up

    async def on_chat_message(self, msg):
        contentType, chatType, chatID = telepot.glance(msg)
        userID = msg['from']['id']

#If message is not text, ignore
        if contentType != 'text':
            self.bot.close()
            return

#Formatting the message coming in
        command = msg['text'].strip().lower()
        #Check if command meant for the bot
        if '@derpassassinbot' not in command and '@cpdppybetabot' not in command:
            self.bot.close()
            return
        command = command.split('@')[0]

        #First, ignore /config, because it's handled by CommandHandler
        if command == '/config':
            self.bot.close()
            return

#Initialisation of variables
        GRPID = DatabaseStats.GRPID
        LOCALID = DatabaseStats.LOCALID
        DBP = DatabaseStats.DBP
        DBG = DatabaseStats.DBG
            
        if chatType == 'group' or 'supergroup':
            #Check for new user / group
            #Note that Messages will be defined
            try:
                GRPID[chatID]
                Messages = LANG[chatID]
            except KeyError:
                Messages = await add_new_group(chatID,msg)

            try:
                LOCALID[userID]
            except KeyError:
                await add_new_person(userID,msg)

######################
#####  /newgame  #####
######################

#TO-DO: Update person's username / first_name
#Handle /newgame command (command used in private chat handled by CommandHandler)
            if command == '/normalgame':
                await self._initGame(chatID,userID,msg,0) #Initialise whatever needs to be initialised


#####################
######  /join  ######
#####################

#TO-DO: Update person's username / first_name
#Handle /join command (command used in private chat handled by CommandHandler)
            elif command == '/join':
                await self._joinGame(chatID,userID,msg)

#########################
######  /killgame  ######
#########################

            elif command == '/killgame': #First need to check if user is admin
                if not await check_admin(self.bot,chatID,userID): #Function returns true if admin, false otherwise
                    self.bot.close()
                    return

                #Reset players
                self.players = {}

                #Cancel countdown if any      
                if self.countdownEvent: 
                    self.scheduler.cancel(self.countdownEvent)
                    self.countdownEvent = None

                #Kill instance of the game running
                if self.gameRunning: 
                    await self.game.kill_game()
                    self.game = None
                    self.gameRunning = False

                await send_message(self.bot,chatID,Messages['killGame'])
                self.bot.close()
                return

#########################
######  /nextgame  ######
#########################

            elif command == '/nextgame':
                if get_maintenance(): #If bot closing for maintenance
                    await send_message(self.bot,chatID,Messages['maintenance']['shutdown'])
                    self.bot.close()
                    return

                elif not self.queued:  #If there's no waiting list, initialise one
                    self.reset_waiting_list(chatID)

                try:
                    username = msg['from']['username']
                    if username in self.queued['username']: #If person already in waiting list, ignore command
                        self.bot.close()
                        return
                    self.queued['username'] += '@' + username + ' '
                except KeyError:
                    if userID in self.queued['noUsername']: #Again, if person already in waiting list, ignore command
                        self.bot.close()
                        return
                    self.queued['noUsername'].append(userID)
                #PM user he was successfully added to waiting list
                if self.chatTitle:
                    await send_message(self.bot,userID,LANG[userID]['nextGameNotify']%(self.chatTitle))
                else: #Chat title has not been obtained yet, so just send generic message
                    await send_message(self.bot,userID,LANG[userID]['nextGameNotifyNoTitle'])
                self.bot.close()
                return

#########################
########  /leave ########
#########################

            #If the person wants to leave the game
            elif command == '/leave':
                #Not in joining phase or person not a player, just ignore
                if (not self.players) or (userID not in self.players):
                    self.bot.close()
                    return
                #Handle boundary case of just 1 person
                elif len(self.players) == 1:
                    self.scheduler.cancel(self.countdownEvent) #cancel event
                    self.players = {}
                    await edit_message(self.messageEditor,Messages['leaveGame1']%(msg['from']['first_name']))
                    self.bot.close()
                    return
                else:
                    self.players.pop(userID,None)
                    await edit_message(self.messageEditor,
                                       Messages['leaveGame']%(msg['from']['first_name']) + Messages['joinGame']['notMax']%(msg['from']['first_name'],len(self.players),MINPLAYERS,MAXPLAYERS),
                                       parse_mode='HTML')
                    self.bot.close()
                    return


##############################
######  GAME FUNCTIONS  ######
##############################
    async def _initGame(self,chatID,userID,msg,code):
        self.chatID = chatID
        self.chatTitle = msg['chat']['title']
        Messages = LANG[chatID]
        firstName = msg['from']['first_name']
        #code is to determine which game mode to start
        #0 = normal, 1 = FFA, 2 = ...
        
        #First check if bot is closing for maintenance...
        if get_maintenance():
            await send_message(self.bot,chatID,Messages['maintenance']['shutdown'])
            self.bot.close()
            return

        #Check if player is already in a game in another group chat
        try:
            stuff = DBP[userID] #Once person successfully joins game, will add into DBP
            if stuff:
                await send_message(self.bot,userID,LANG[userID]['isInGame'])
                self.bot.close()
                return
        except KeyError:
            pass
        
    #Then check for an ongoing game
        if self.gameRunning:
            await send_message(self.bot,chatID,Messages['existingGame'])
            self.bot.close()
            return
        
    #Game hasn't started, but someone initiated one, then help the person join
        elif self.players:
            await self._joinGame(chatID,userID,msg)

        #Check if bot can talk to user
        elif await self.can_talk(1,userID,firstName):
            self.players[userID] = msg['from'] #Add user info. Not using global queue, because groups tend to be relatively small. RELATIVE.
            #Storing into GLOBAL databases DBP and DBG, so gotta use global queue
            await QUEUE.put((DBG,chatID,[])) #to collate queries from users for processing. Uses list.
            await QUEUE.put((DBP,userID,(None,None))) #has data structure: (heroObject, gameObject). Just a 2-value tuple, not a tuple of tuple
            #Notify_waiting_list will do the sending of the message
            sent = await self.notify_waiting_list(chatID,Messages['newGame']%(msg['from']['first_name'],MINPLAYERS,MAXPLAYERS)+Messages['countdownNoRemind']%(60))
            self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent)) #So that above message can be edited if the person leaves
            # Generate countdown event
            self.countdownEvent = self.scheduler.event_later(40, ('_countdown_game_start', {'seconds': 40}))


    async def _joinGame(self,chatID,userID,msg):
        Messages = LANG[chatID]
        firstName = msg['from']['first_name']
        #Check if user has already joined a game, or this game
        if userID in DB:
            await send_message(self.bot,userID,LANG[userID]['isInGame'])
            return
        
        #Check if a game has been initiated, assuming a game isn't running already
        elif not self.players:
            #Then we help to start a new game!
            await self._initGame(chatID,userID,msg)
            return

        #Check if bot can talk to user
        elif await self.can_talk(0,userID,firstName):
            playerCount = len(self.players)
            if self.countdownEvent: #Cancel countdown if any
                self.scheduler.cancel(self.countdownEvent)
                self.countdownEvent = None
            if playerCount >= MAXPLAYERS:
                await send_message(self.bot,userID,LANG[userID]['max'])
                return
            self.players[userID] = msg['from'] #Add user info to players
            DB[userID] = () #Add user info to Database
            if playerCount == (MAXPLAYERS - 1): #Last player to be allowed to join, start the game!
                await send_message(self.bot,chatID,Messages['joinGame']['Max']%(msg['from']['first_name']),parse_mode='HTML')
                await self.game_start() #Start the game!
            else:
                playerCount += 1
                sent = await send_message(self.bot,chatID,Messages['joinGame']['notMax']%(msg['from']['first_name'],playerCount,MINPLAYERS,MAXPLAYERS),parse_mode='HTML')
                if sent:
                    self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent)) #So that above message can be edited if the person leaves
                # Generate countdown event
                self.countdownEvent = self.scheduler.event_later(10, ('_countdown_game_start', {'seconds': 10})) #FOR TESTING
                #self.countdownEvent = self.scheduler.event_later(30, ('_countdown_game_start', {'seconds': 40})) #FOR IMPLEMENTATION
            return

        #############
        # Countdown #
        #############
#Countdown to game start, notify users of time they have left to join after a set time
    async def on__countdown_game_start(self,event):
        timer = event['_countdown_game_start']['seconds']
        if timer == 40: #60 to 20s
            sent = await send_message(self.bot,self.chatID,LANG[self.chatID]['countdownRemind']%(20),parse_mode='HTML')
            if sent:
                self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent))
            self.countdownEvent = self.scheduler.event_later(20, ('_countdown_game_start', {'seconds': 20}))
        else:
            if len(self.players) < MINPLAYERS: #Prevent the game from starting
                await edit_message(self.messageEditor,LANG[self.chatID]['failStart']['lackppl'])
                self.countdownEvent = None
                for player in self.players:
                    DB.pop(player,None)
                self.players = {}
                return
            #Start the game!
            await self.game_start()

#Function to attempt talking to a user, failure will prevent user from starting or joining a game
    async def can_talk(self,start,userID,username):
        #variable start is boolean. 1 = initiate, 0 = join
        message = LANG[userID]['newGameToUser'] if start else LANG[userID]['joinToUser']
        try:
            await self.bot.sendMessage(userID,message)
        except telepot.exception.BotWasBlockedError:
            await send_message(self.bot,self.chatID,LANG[self.chatID]['failTalk']%(username))
            return False
        except telepot.exception.TelegramError:
            await send_message(self.bot,self.chatID,LANG[self.chatID]['failTalk']%(username))
            return False
        else:
            return True


##########################
######  Game start  ######
##########################
    async def game_start(self):
        if self.game:
            return
        sent = await send_message(self.bot,self.chatID,LANG[self.chatID]['okStart'])
        if sent:
            self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent))
        self.game = Game(self.bot,self.chatID,self.players,self.messageEditor)
        await self.game.allocate(self.players,len(self.players),self.game)
        self.countdownEvent = self.scheduler.event_later(1, ('_countdown_game_next_round', {'seconds': 1}))

##########################
######  Next Round  ######
##########################
    async def on__countdown_game_next_round(self,event):
        #To send and receive callback queries regarding user actions (Phase 1)
        await self.game.next_round()
        #Schedule timer for Phase 2
        survivors = len(self.game.get_alive_all())
        if survivors == 2:
            timer = 25
        elif survivors <= 6:
            timer = 5 #FOR TESTING
            #timer = 40 #FOR IMPLEMENTATION
        else:
            timer = 55
        sent = await send_message(self.bot,self.chatID,LANG[self.chatID]['countdownToPhase2']%(timer+20))
        if sent:
            self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent))
        self.countdownEvent = self.scheduler.event_later(timer, ('_countdown_collate_result', {'seconds': timer}))

    ##Phase 2##
    #To close all unanswered queries, then sort queries, process them and print 1 huge message in group chat
    #To check if game should end
    #Otherwise schedule next round
    async def on__countdown_collate_result(self,event):
        timer = event['_countdown_collate_result']['seconds']
        if timer != 20: #Send reminder to inform people they have 20s left to make choices!
            await edit_message(self.messageEditor,LANG[self.chatID]['countdownChoice']%(20))
            self.countdownEvent = self.scheduler.event_later(20, ('_countdown_collate_result', {'seconds': 20}))
            return

        #endGame is a boolean value to decide if the game should end or not
        #The other 2 are for editing the last message sent by Game object
        endGame,self.messageEditor, message = await self.game.end_round()
        survivors = len(self.game.get_alive_all())

        if endGame: #to close the game, reset all variables
            await self.game.end_game()
            self.game = None
            self.players = {}
            return

        #Otherwise, set timer according to customised math function
        rnd = self.game.round
        if survivors == 2:
            timer = 30
        else:
            weight = 1/(1+0.001*math.pow(math.e,0.55*rnd))
            timer = weight*(60*(1 + 1/(0.5+math.pow(math.e,4-0.55*survivors))))+(1-weight)*(-60*(2/(1+math.pow(math.e,5.2-0.73*rnd))-3))
            timer = int(round(timer,-1))

        await edit_message(self.messageEditor,message + LANG[self.chatID]['countdownToPhase1']%(timer))
        self.countdownEvent = self.scheduler.event_later(timer, ('_countdown_game_next_round', {'seconds': timer}))
        return
        #TESTING POWER-UP EVENT
        #if survivors == 2:
            #Generate random countdown to power-up event
            #actualTimer = max(5, int(math.pow(time.time(),int(time.time() % 7)) % timer))
            #self.countdownEvent = self.scheduler.event_later(actualTimer, ('_power_up', {'seconds': timer-actualTimer}))
        #else:
            #self.countdownEvent = self.scheduler.event_later(timer, ('_countdown_game_next_round', {'seconds': timer}))
        #return

#############################################
######  Notify peeps in  waiting list  ######
#############################################

    async def notify_waiting_list(self,chatID,message):
        if not self.queued: #No one to include in message, just send original message
            return await send_message(self.bot,chatID,message)
        #First send message to people with no usernames that a new game has started
        for userID in self.queued['noUsername']:
            await send_message(self.bot,userID,LANG[userID]['nextGameNoUsername']%(self.chatTitle))
        #Send message in group chat to notify those with usernames that a new game has started
        message = self.queued['username'] + message
        self.reset_waiting_list(chatID)
        return await send_message(self.bot,chatID,message)

##################################
######  Reset waiting list  ######
##################################

    def reset_waiting_list(self,chatID):
        #For users with usernames, just append usernames to message to be sent in group chat
        #Those without will be PMed
        self.queued = {'username':'','noUsername':[]}
        return

##########################
##### POWER-UP EVENT #####
##########################

    async def on__power_up(self,event):
        timer = event['_power_up']['seconds']
        #Generate random power up
        sent = await send_message(self.bot,self.chatID,LANG[self.chatID]['powerUp']['DmgX']%(3))
        sent = await send_message(self.bot,self.chatID,LANG[self.chatID]['powerUp']['Health']%(3))
        sent = await send_message(self.bot,self.chatID,LANG[self.chatID]['powerUp']['LoD']%(3))
        if sent:
            self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent))
        #Send query
        self.countdownEvent = self.scheduler.event_later(timer, ('_countdown_game_next_round', {'seconds': timer}))
        
