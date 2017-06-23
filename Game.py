import asyncio
import telepot
import telepot.aio
import telepot.aio.helper
import random
import time
import Globals
from telepot.namedtuple import *
from Heroes import one_agent_instance
from KeyboardQuery import generate_agent_info
from Messages import send_message, edit_message
'''
no. of VIPs and DERP agents are determined as such:
--VIPs and DERP agents--
No. of DERP agents = 2x no. of VIPs (rounded up if odd)
Numbers below are no. of DERP agents, brackets = no. of VIPs

3-4 players: 1
5-6 players: 2 (1)
7-9 players: 3 (2)
10-11 players: 4 (2)
12-14 players: 5 (3)
15-16 players: 6 (3)
17-19 players: 7 (4)
20-21 players: 8 (4)
22-24 players: 9 (5)
25-26 players: 10 (5)
27-29 players: 11 (5)
30-31 players: 12 (6)
32 players: 13 (6)
'''


#Sorting order for queries
ORDER = {'ult':0, 'attack':1, 'heal':1}
AGENTULTS = {
    'Anna':-500, 'Aspida':-300, 'Dracule':-100, 'Elias':-400,
    'Grace':100, 'Grim':0, 'Grote':-300, 'Hamia':-300, 'Harambe':-300,
    'Impilo':-200, 'Jigglet':-1000, 'Jordan':-200,
    'Mitsuha':-100, 'Munie':-1000, 'Novah':-100, 'Prim':100,
    'Ralpha':0, 'Saitami':0,'Sanar':0, 'Sonhae':0,'Taiji':-200,
    'Wanda':-300, 'Yunos':-300,}
#Limit for agents who can select multiple agents
LIMITS = {'Grim':3,'Sanar':3}

#Randomly selects from a dictionary, deletes selected entry from it and returns the selection
def random_select(dicty):
    key = list(dicty.keys())
    for i in range(0,random.randint(1,10)):
        random.shuffle(key)
    key = random.choice(key)
    result = dicty[key]
    del dicty[key]
    return result

#Function to handle cases where more queries than allowed are received, due to pressing the callback button multiple times (my hypothesis)
#(Eg. Grim attacking more than 3 unique ppl, when it should be 3 max)
#Reminder that each query is a tuple of form: (date,agent,target,option)
#Because we want to avoid mutating the list while iterating through it,
#it's better to store the results in a separate list and return this separate list instead
def remove_extras(queries):
    #First, because the date is unique, the good thing is we don't need it anymore
    #So will remove and replace with arbitary number 1
    #This is to allow me to use set() to remove duplicates!
    tmp = []
    for query in queries:
        tmp.append((1,query[1],query[2],query[3]))

    tmp = list(set(tmp))
    #make a duplicate of the LIMITS defined above in globals
    limit = LIMITS.copy()
                   
    #create a new list to be returned
    result = []
    for query in tmp:
        #if query is from multiple selection agent as described above)
        if query[1] in limit:
            #Check if limit exceeded
            if limit[query[1]] > 0:
                #include in result
                result.append(query)
                #Subtract 1
                limit[query[1]] -= 1
            #Otherwise don't include (dont need to do anything)
        #Otherwise leave it alone
        else:
            result.append(query)
    return result
    

#Processing query
#Returns a message to be sent to group chat
#Each query is a tuple: (date,agent,target,option)
async def proc_query(game,query):
    agent, target, option = query[1], query[2], query[3]
    survivors = game.get_alive_all()
    if agent == 'Grace' and agent in survivors and option == 'ult': #Handling exception for Grace ult
        agent = survivors[agent]
        target = game.get_dead_all()[target]
        agent.ult(target)
        #Send message to target informing him of being resurrected
        await send_message(game.bot,target.userID,Globals.LANG[target.userID]['combat']['res'],parse_mode='HTML')
        return agent.ult(target)
    elif agent not in survivors or target not in survivors: #Agent or target has died, don't do anything
        return ''

    #Retrieve objects
    agent,target = survivors[agent], survivors[target]

    #Apply option
    if option == 'ult':
        if isinstance(agent,Elias): #or isinstance(agent,Eliseo):
            await agent.reveal(target,game)
        msg = agent.ult(target)
    elif option == 'heal':
        msg = agent.heal(target)
    else:
        msg = agent.attack(target)

    #Check if agent or target died, send dieded messages
    if not agent.alive:
        await send_message(game.bot,agent.userID,Globals.LANG[agent.userID]['combat']['KO'],parse_mode='HTML')
    elif not target.alive:
        await send_message(game.bot,target.userID,Globals.LANG[target.userID]['combat']['KO'],parse_mode='HTML')

    #Finally, return result
    return msg

class normalGame(object):
    def __init__(self, bot, chatID, playerCount, messageEditor):
        self.bot = bot
        self.chatID = chatID
        self.Messages = Globals.LANG[chatID]
        self.messageEditor = messageEditor #edit the previous message (Game is starting...), & others where applicable
        self.message = '' #Old message where new text is to be appended to it
        self.agents = {}
        self.round = 0 # Denotes current round
        self.playerCount = playerCount
        self.gameMode = 1
        
        #determine no. of VIPs and DERP agents to have (DERP is 1.5 or 2x more than VIPs!)
        if self.playerCount <= 4:
            DERPCount = 1
        else:
            #observe that we can to determine the no. of DERP via a 2-piece function.
            #If no. of players modulo 5 = 0 or 1, it will be 1 function, otherwise it will another function
            #DERPCount will be abused to save space
            DERPCount = (self.playerCount%5)
            if DERPCount <= 1:
                DERPCount = 2*(self.playerCount//5)
            else:
                DERPCount = 1 + 2*(self.playerCount//5)

        self.DERPCount = DERPCount
        self.VIPCount = int(round((DERPCount/2)+0.1, 0))


        #######################################################
        ### Assigning and PM-ing roles and teams to players ###
        #######################################################
    async def allocate(self,players):
        
        #filter special heroes based on no. of players
        AGENTS = one_agent_instance(self.playerCount)

        for count in range(1,self.playerCount+1):
            player = random_select(players) #randomly select a player
            agent = random_select(AGENTS) #randomly select a hero
            playerID = player['id'] #same as userID
            try: #see if user has a username. It's also in case the user updates his username, so update our DB
                username = player['username']
            except KeyError:
                username = None

            player = agent(playerID,username,player['first_name'],self.Messages) #assign player to hero
            self.agents[playerID] = player #save agent into game object, using player's ID as the key
            await Globals.QUEUE.put((Globals.DBP,playerID,(player,self))) # add hero object to database,
            # so that callback queries can be sent to it by CallbackHandler for processing
            # Also, game object is added for retrieving important info by CallbackHandler

            Messages = Globals.LANG[playerID]
            message = Messages['agentDesc']%(player.agentName)
            message += generate_agent_info(Messages,player.agentCode) #PM player role, function found in KeyboardQuery.py
            sent = await send_message(self.bot,playerID,message)
            player.editor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent)) #editor will be used to append team message later on

            #Assigning teams
            if count <= self.DERPCount: #first assign DERP agents
                player.team = 'DERP'
                #Message will be sent at a later stage

            elif (self.playerCount-count) >= self.VIPCount: #followed by PYRO agents
                player.team = 'PYRO'
                message += Messages['teamPYRO']
                await edit_message(player.editor,message)

            else: #finally VIPs
                player.team = 'PYROVIP'
                message += Messages['VIPself']
                await edit_message(player.editor,message)
                if self.playerCount > 4: #Exclude games with 3-4 people: no need for people to be informed
                    randomPlayer = random.choice(list(self.get_alive_PYROteam().values()))
                    while randomPlayer.userID == player.userID: #ensure that someone other than the VIP himself is selected
                        randomPlayer = random.choice(list(self.get_alive_PYROteam().values()))
                    #PM the chosen player
                    await send_message(self.bot,randomPlayer.userID,Globals.LANG[randomPlayer.userID]['VIP']%(player.agentName,player.firstName),parse_mode='HTML')

            #Finally, reset agent editor
            player.editor = None

        #Let DERP agents know who is on their team
        #Message will be in group chat language
        Messages = self.Messages
        self.message = Messages['summary']['teamDERP']
        for agent in list(self.get_all_DERP().values()):
            self.message += Messages['summary']['agent']%(agent.get_full_idty())
        self.message += Messages['teamDERP']
        for agent in list(self.get_all_DERP().values()):
            await send_message(self.bot,agent.userID,self.message)

        #Finally, announce player assignment to group chat
        players = self.get_alive_all()
        self.message = Messages['allotSuccess']
        for agentName,agent in players.items():
            self.message += Messages['summary']['agentStart']%(agent.get_clickable_name(),agentName)
        self.message += Messages['delay']
        await edit_message(self.messageEditor,self.message)
        await asyncio.sleep(5)
        self.message = None #reset variable
        return


        #######################################################
        ######## Logic for running 1 round of the game ########
        #######################################################
    async def next_round(self):
        self.round += 1 #Increment round number
        players = self.get_alive_all()
        for agent in players.values():
            agent.minus_CD()
            await agent.send_query(self.bot,'start',list(players.values()),self.gameMode)
        return

    #To close all unanswered queries, then sort queries, process them and print 1 huge message in group chat
    #To check if game should end
    #To return a boolean value deciding if the game should end
    async def end_round(self):
        #Close all unanswered queries with "time is up!" notification
        agents = list(self.get_alive_all().values())
        for agent in agents:
            try:
                await agent.editor.editMessageReplyMarkup(reply_markup=None)
                await edit_message(agent.editor,Globals.LANG[agent.userID]['timeUp'])
            except telepot.exception.TelegramError:
                continue

        #Set Messages variable, obtain queries
        Messages = self.Messages
        queries = DB[self.chatID]
        
        #Clear the queries!
        DB[self.chatID] = []
        #Each query is a tuple: (date,agent,target,option)
        queries.sort(key = lambda x: (ORDER[x[3]],x[0]))
        #Split the list into abilities and others
        imptQueries = []
        while queries:
            if queries[0][3] == 'ult':
                imptQueries.append(queries[0])
                del queries[0]
            else:
                break
        
        #Sort by date, but with queries grouped by agent
        order = {}
        for idx,query in reversed(list(enumerate(imptQueries))):
            #apply customised sort for ults
            idx += AGENTULTS[query[1]]
            order[query[1]] = idx
        imptQueries.sort(key = lambda x: (order[x[1]]))

        #Recombine queries
        imptQueries.extend(queries)

        #Handle cases where more queries than allowed are received (Eg. Grim attacking more than 3 ppl, when it should be 3 max)
        #Also remove duplicate queries
        imptQueries = remove_extras(imptQueries)
        
        #Getting AFK players
        AFK = list(self.get_alive_all().keys())
        for query in imptQueries:
            if query[1] in AFK:
                AFK.remove(query[1])

        #Add in self auto-attack queries
        for agent in AFK:
            imptQueries.append((1000,agent,agent,'attack'))

        #Process queries!!
        message = Messages['combat']['intro']%(self.round)
        for query in imptQueries:
            message += await proc_query(self,query)
        #If message becomes too long, split up the message to send
        while len(message)>4096:
            idx = message.find('\n',3900) + 2
            await send_message(self.bot,self.chatID,message[:idx])
            message = message[idx:].strip()
            await asyncio.sleep(2)

        #Last iteration
        await send_message(self.bot,self.chatID,message)

        #Send summary message
        message = Messages['summary']['intro']
        agents = list(self.get_alive_all().values()) #abusing variable name in consideration of memory space
        if agents:
            message += Messages['summary']['aliveStart']
            for agent in agents:
                message += Messages['summary']['alive']%(agent.get_full_idty(),1 if (agent.health < 1) else agent.health)
                #At the same time, reset agent statuses for next round
                agent.reset_next_round()
        agents = list(self.get_dead_all())
        if agents:
            message += Messages['summary']['deadStart']
        #A lot of code reuse below, maybe I should modularise it
        agents = list(self.get_dead_DERP().values())
        for agent in agents:
            message += Messages['summary']['deadDERP']%(agent.get_full_idty())
        agents = list(self.get_dead_PYRO().values())
        for agent in agents:
            message += Messages['summary']['deadPYRO']%(agent.get_full_idty())
        agents = list(self.get_dead_PYROVIP().values())
        for agent in agents:
            message += Messages['summary']['deadPYROVIP']%(agent.get_full_idty())

        sent = await send_message(self.bot,self.chatID,message)
        self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent))
        self.message = message #To append end-game message,if any

        #Check if game should end
        if not self.get_alive_all() or (not self.get_alive_DERP() and not self.get_alive_PYROVIP()):
            #Send message that game ends in a draw since either everyone is dead, or all DERP agents and VIPs die in the same turn
            await self.bot.sendChatAction(self.chatID,action='upload_video')
            await self.bot.sendDocument(self.chatID,Messages['gifs']['drawVidID'])
            self.message += Messages['endGame']['draw']
            await edit_message(self.messageEditor,self.message)
            return (True,self.messageEditor,self.message)
        elif not self.get_alive_DERP():
            #Send message that Team PYRO won as all DERP agents have been killed!
            await self.bot.sendChatAction(self.chatID,action='upload_video')
            await self.bot.sendDocument(self.chatID,Messages['gifs']['PYROVidID'])
            self.message += Messages['endGame']['DERP.KO']
            await edit_message(self.messageEditor,self.message)
            return (True,self.messageEditor,self.message)

        elif not self.get_alive_PYROVIP():
            #Send message that Team DERP won as all VIP agents have been assassinated!
            await self.bot.sendChatAction(self.chatID,action='upload_video')
            await self.bot.sendDocument(self.chatID,Messages['gifs']['DERPVidID'])
            self.message += Messages['endGame']['PYROVIP.KO']
            await edit_message(self.messageEditor,self.message)
            return (True,self.messageEditor,self.message)

        elif self.round == 25:
            #End game by looking at which team has most health
            #Send message that game will end because it's gone on for far too long
            self.message = Messages['endGame']['tooLong']
            sent = await send_message(self.bot,self.chatID,self.message)
            self.messageEditor = telepot.aio.helper.Editor(self.bot, telepot.message_identifier(sent))

            DERPhealth = PYROhealth = 0
            for agent in list(self.get_alive_DERP().values()):
                DERPhealth += agent.health
            for agent in list(self.get_alive_PYROteam().values()):
                PYROhealth += agent.health

            self.message += Messages['endGame']['tooLongSummary']%(DERPhealth,PYROhealth)
            await edit_message(self.messageEditor,self.message)

            if DERPhealth > PYROhealth:
                await self.bot.sendChatAction(self.chatID,action='upload_video')
                await self.bot.sendDocument(self.chatID,Messages['gifs']['DERPVidID'])
                self.message += Messages['endGame']['DERPWin']
                await edit_message(self.messageEditor,self.message)

            elif PYROhealth > DERPhealth:
                await self.bot.sendChatAction(self.chatID,action='upload_video')
                await self.bot.sendDocument(self.chatID,Messages['gifs']['PYROVidID'])
                self.message += Messages['endGame']['PYROWin']
                await edit_message(self.messageEditor,self.message)

            else: #In the highly unlikely event of a draw
                await self.bot.sendChatAction(self.chatID,action='upload_video')
                await self.bot.sendDocument(self.chatID,Messages['gifs']['drawVidID'])
                self.message += Messages['endGame']['rareDraw']
                await edit_message(self.messageEditor,self.message)
            return (True,self.messageEditor,self.message)
        return (False,self.messageEditor,self.message)

    #To delete all entries in DB
    async def end_game(self):
        #Announce who was in which team, at the same time, remove them from DB
        #Start with team DERP
        agents = self.get_all_DERP()
        msg = self.Messages['summary']['endIntro'] + self.Messages['summary']['teamDERP']
        for agent in agents.values():
            del DB[agent.userID]
            msg += self.Messages['summary']['agent']%(agent.get_full_idty())

        #Then team PYRO
        agents = self.get_all_PYROteam()
        msg += self.Messages['summary']['teamPYRO']
        for agent in agents.values():
            del DB[agent.userID]
            if agent.team == 'PYROVIP':
                msg += self.Messages['summary']['VIP']%(agent.get_full_idty())
            else:
                msg += self.Messages['summary']['agent']%(agent.get_full_idty())

        #Send message
        await send_message(self.bot,self.chatID,msg)

        #Finally delete in DB
        del DB[self.chatID]

    #In case of error, kill the game
    async def kill_game(self):
        agents = self.get_all()
        #No agents, then just return
        if not agents:
            return
        for agent in list(agents.values()):
            DB.pop(agent.userID,None)
            print(str(agent.userID) + ' cleared!')
            try:
                #Close any open queries
                await agent.editor.editMessageReplyMarkup(reply_markup=None)
            except telepot.exception.TelegramError:
                pass
            except AttributeError:
                pass
            #Tell player game has been killed
            await send_message(self.bot,agent.userID,Globals.LANG[agent.userID]['killGameAgents'],reply_markup=None)
        #Clear all agents
        self.agents = None
        return


#Accessor methods
#Each method returns a dictionary of agents with the key:value pair being agentName:agent
    def get_all(self):
        return self.agents

    def get_all_DERP(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.team == 'DERP' :
                result[agent.agentName] = agent
        return result

    def get_all_PYRO(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.team == 'PYRO' :
                result[agent.agentName] = agent
        return result

    def get_all_PYROteam(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.team in ('PYRO','PYROVIP') :
                result[agent.agentName] = agent
        return result

    def get_all_PYROVIP(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.team == 'PYROVIP' :
                result[agent.agentName] = agent
        return result


    def get_alive_all(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.alive:
                result[agent.agentName] = agent
        return result

    def get_alive_DERP(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.alive and agent.team == 'DERP':
                result[agent.agentName] = agent
        return result

    def get_alive_PYRO(self): #Non-VIPs
        result = {}
        for agent in list(self.agents.values()):
            if agent.alive and agent.team == 'PYRO':
                result[agent.agentName] = agent
        return result

    def get_alive_PYROteam(self): #could use composition of the 2 other getter methods, but then there'll be 2 iterations when we can do it in 1
        result = {}
        for agent in list(self.agents.values()):
            if agent.alive and agent.team in ('PYRO','PYROVIP'):
                result[agent.agentName] = agent
        return result

    def get_alive_PYROVIP(self):
        result = {}
        for agent in list(self.agents.values()):
            if agent.alive and agent.team == 'PYROVIP':
                result[agent.agentName] = agent
        return result

    def get_dead_all(self):
        result = {}
        for agent in list(self.agents.values()):
            if not agent.alive:
                result[agent.agentName] = agent
        return result

    def get_dead_DERP(self):
        result = {}
        for agent in list(self.agents.values()):
            if not agent.alive and agent.team == 'DERP':
                result[agent.agentName] = agent
        return result

    def get_dead_PYRO(self):
        result = {}
        for agent in list(self.agents.values()):
            if not agent.alive and agent.team == 'PYRO':
                result[agent.agentName] = agent
        return result

    def get_dead_PYROteam(self):
        result = {}
        for agent in list(self.agents.values()):
            if not agent.alive and agent.team == ('PYRO','PYROVIP'):
                result[agent.agentName] = agent
        return result

    def get_dead_PYROVIP(self):
        result = {}
        for agent in list(self.agents.values()):
            if not agent.alive and agent.team == 'PYROVIP':
                result[agent.agentName] = agent
        return result

