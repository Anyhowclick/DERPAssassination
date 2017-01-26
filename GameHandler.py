import asyncio
import telepot
import telepot.aio
import telepot.aio.helper
from telepot.exception import *
from telepot.namedtuple import *
from Game import Game
from Messages import Messages
from Database import DB
from Admin import check_admin, get_maintenance
'''
gameHandler will handle all game-related commands, such
as /newgame, /join, as well as everything that involves running
the game (game progression, the 2 phases of each round, sending
and receiving callback queries from users, ability and attack order,
sending message to group chat etc.)

Agent stats and abilities are stored in the AgentClasses and Agent
python scripts. Whatever text messages are to be printed will be
imported from Messages
'''

MINPLAYERS = 2
MAXPLAYERS = 17

class gameHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None #Game object
        self.players = {} #Users who joined the game (unassigned agents)
        self.chatID = None #Group chat ID
        self.countdownEvent = None #Countdown till game start (to allow people to join)
        #Catching countdown events
        self.router.routing_table['_countdown_game_start'] = self.on__countdown_game_start
        self.router.routing_table['_countdown_game_next_round'] = self.on__countdown_game_next_round
        self.router.routing_table['_countdown_collate_result'] = self.on__countdown_collate_result

    async def on_chat_message(self, msg):
        contentType, chatType, chatID = telepot.glance(msg)
        userID = msg['from']['id']
#If message is not text, ignore
        if contentType != 'text':
            return

#Formatting the message coming in
        command = msg['text'].strip().lower()
        if '@derpassassinbot' not in command and '@derpassbetabot' not in command:
            return
        command = command.split('@')[0]
        if chatType == 'group' or 'supergroup':

######################
#####  /newgame  #####
######################

#Handle /newgame command (command used in private chat handled by CommandHandler)
            if command == '/newgame':
                await self._initGame(chatID,userID,msg) #Initialise whatever needs to be initialised


#####################
######  /join  ######
#####################

#Handle /join command (command used in private chat handled by CommandHandler)
            elif command == '/join':
                await self._joinGame(chatID,userID,msg)

#########################
######  /killgame  ######
#########################
                
            elif command == '/killgame': #First need to check if user is admin
                if not await check_admin(self.bot,chatID,userID): #Function returns true if admin, false otherwise
                    return
                if self.countdownEvent: #Cancel countdown if any
                    self.scheduler.cancel(self.countdownEvent)
                if self.players:
                    for player in self.players:
                        DB.pop(player,None)
                        self.players = {}
                elif self.game: #Instance of game running
                    await self.game.kill_game()
                    self.game = None
                await self.bot.sendMessage(chatID,Messages['killGame'])
                self.chatID = None
                return

    async def _initGame(self,chatID,userID,msg):
        self.chatID = chatID
        username = msg['from']['first_name']
        if get_maintenance():
            await self.bot.sendMessage(chatID,Messages['maintenance']['shutdown'],parse_mode='HTML')
            return
    #Check for an ongoing game
        if self.game:
            await self.bot.sendMessage(chatID,Messages['existingGame'])
            return
    #Game hasn't started, but someone initiated one, then help the person join
        elif self.players:
            await self._joinGame(chatID,userID,msg)
            return
    #Check if player is already in a game in another group chat
        elif userID in DB:
            await self.bot.sendMessage(userID,Messages['isInGame'])
            return
        #Check if bot can talk to user
        elif await self._talk('/newgame',userID,username):
            self.players[userID] = msg['from'] #Add user info
            DB[chatID]=[] #to collate queries from users for processing
            DB[userID]=() #has data structure: (heroObject, gameObject). Just a 2-value tuple, not a tuple of tuple
            await self.bot.sendMessage(chatID,Messages['newGame']%(msg['from']['first_name'],MINPLAYERS,MAXPLAYERS),parse_mode='HTML')
            # Generate countdown event
            await self.bot.sendMessage(chatID,Messages['countdownNoRemind']%(60),parse_mode='HTML')
            self.countdownEvent = self.scheduler.event_later(30, ('_countdown_game_start', {'seconds': 30}))


    async def _joinGame(self,chatID,userID,msg):
        username = msg['from']['first_name']
        #Check if a game has been initiated, assuming a game isn't running already
        if not self.players:
            #Then we help to start a new game!
            await self._initGame(chatID,userID,msg)
            return

        #Check if user has already joined a game, or this game
        elif userID in DB:
            await self.bot.sendMessage(userID,Messages['isInGame'])
            return

        #Check if bot can talk to user
        elif await self._talk('/join',userID,username):
            playerCount = len(self.players)
            if self.countdownEvent: #Cancel countdown if any
                self.scheduler.cancel(self.countdownEvent)
            if playerCount >= MAXPLAYERS:
                await self.bot.sendMessage(userID,Messages['max'])
                return
            self.players[userID] = msg['from'] #Add user info to players
            DB[userID] = () #Add user info to Database
            if playerCount == (MAXPLAYERS - 1): #Last player to be allowed to join, start the game!
                await self.bot.sendMessage(chatID,Messages['joinGame']['Max']%(msg['from']['first_name']),parse_mode='HTML')
                await self.game_start() #Start the game!
            else:
                playerCount += 1
                await self.bot.sendMessage(chatID,Messages['joinGame']['notMax']%(msg['from']['first_name'],playerCount,MINPLAYERS,MAXPLAYERS),parse_mode='HTML')
                # Generate countdown event
                self.countdownEvent = self.scheduler.event_later(10, ('_countdown_game_start', {'seconds': 10})) #FOR TESTING
                #self.countdownEvent = self.scheduler.event_later(30, ('_countdown_game_start', {'seconds': 30})) #FOR IMPLEMENTATION
            return

        #############
        # Countdown #
        #############
#Countdown to game start, notify users of time they have left to join after a set time
    async def on__countdown_game_start(self,event):
        timer = event['_countdown_game_start']['seconds']
        if timer == 30: #60 to 30s
            await self.bot.sendMessage(self.chatID,Messages['countdownRemind']%(30),parse_mode='HTML')
            self.countdownEvent = self.scheduler.event_later(20, ('_countdown_game_start', {'seconds': 20}))
        elif timer == 20: #30s to 10s
            await self.bot.sendMessage(self.chatID,Messages['countdownNoRemind']%(10),parse_mode='HTML')
            self.countdownEvent = self.scheduler.event_later(10, ('_countdown_game_start', {'seconds': 10}))
        else:
            if len(self.players) < MINPLAYERS: #Prevent the game from starting
                await self.bot.sendMessage(self.chatID,Messages['failStart']['lackppl'])
                self.countdownEvent = None
                self.chatID = None #Not really required, but for completeness
                for player in self.players:
                    DB.pop(player,None)
                self.players = {}
                return
            #Start the game!
            await self.game_start()

#Function to attempt talking to a user, failure will prevent user from starting or joining a game
    async def _talk(self,command,userID,username):
        message = Messages['newGameToUser'] if command == '/newgame' else Messages['joinToUser']
        try:
            await self.bot.sendMessage(userID,message)
        except telepot.exception.BotWasBlockedError:
            await self.bot.sendMessage(self.chatID,Messages['failTalk']%(username),parse_mode='HTML')
            return False
        except telepot.exception.TelegramError:
            await self.bot.sendMessage(self.chatID,Messages['failTalk']%(username),parse_mode='HTML')
            return False
        else:
            return True


##########################
######  Game start  ######
##########################
    async def game_start(self):
        await self.bot.sendMessage(self.chatID,Messages['okStart'])
        self.game = Game(self.bot,self.chatID,self.players)
        await self.game.allocate(self.players,len(self.players),self.game)
        self.countdownEvent = self.scheduler.event_later(0, ('_countdown_game_next_round', {'seconds': 0}))

##########################
######  Next Round  ######
##########################
    async def on__countdown_game_next_round(self,event):
        #To send and receive callback queries regarding user actions (Phase 1)
        await self.game.next_round()
        #Schedule timer for Phase 2
        survivors = len(self.game.get_alive_all())
        if survivors == 2:
            timer = 10
        elif survivors <= 6:
            timer = 5 #FOR TESTING
            #timer = 40 #FOR IMPLEMENTATION
        else:
            timer = 70
        await self.bot.sendMessage(self.chatID,Messages['countdownToPhase2']%(timer+20),parse_mode='HTML')
        self.countdownEvent = self.scheduler.event_later(timer, ('_countdown_collate_result', {'seconds': timer}))

    ##Phase 2##
    #To close all unanswered queries, then sort queries, process them and print 1 huge message in group chat
    #To check if game should end
    #Otherwise schedule next round
    async def on__countdown_collate_result(self,event):
        timer = event['_countdown_collate_result']['seconds']
        if timer != 20: #Send reminder to inform people they have 20s left to make choices!
            await self.bot.sendMessage(self.chatID,Messages['countdownChoice']%(20),parse_mode='HTML')
            self.countdownEvent = self.scheduler.event_later(20, ('_countdown_collate_result', {'seconds': 20}))
            return
        endGame = await self.game.end_round() #endGame is a boolean value to decide if the game should end or not
        survivors = len(self.game.get_alive_all())
        if endGame: #to close the game, reset all variables
            await self.game.end_game()
            self.game = None
            self.chatID = None
            self.players = {}
            return
        #Otherwise, set timer according to no. of survivors
        if survivors <= 3:
            timer = 10 #FOR TESTING
            #timer = 45 #FOR IMPLEMENTATION
        elif survivors <= 5:
            timer = 90
        elif survivors <= 11:
            timer = 120
        else:
            timer = 150
        await self.bot.sendMessage(self.chatID,Messages['countdownToPhase1']%(timer),parse_mode='HTML')
        self.countdownEvent = self.scheduler.event_later(timer, ('_countdown_game_next_round', {'seconds': timer}))
