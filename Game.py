import asyncio
import telepot
import telepot.aio
import telepot.aio.helper
import random
from telepot.namedtuple import *
from Heroes import *
from Messages import Messages
from Database import DB
'''
no. of VIPs and DERP agents are determined as such:
--VIPs and DERP agents--
No. of VIPs = no. of DERP agents
3-4 players: 1
5-7 players: 2
8-10 players: 3
11-13 players: 4
14-16 players: 5
17-19 players: 6
20-22 players: 7
23-25 players: 8
26-28 players: 9
29-32 players: 10

--Innercircle--
no.of players <=4: 1
no.of players > 4: 2 if (no.of players - 1) divisible by 3 else 1
'''

#Sorting order for queries
ORDER = {'ult':0, 'attack':1, 'heal':1}
AGENTULTS = {'Sonhae':0,'Taiji':-200,'Dracule':-100,'Novah':-100,'Saitami':0,
             'Grim':0,'Harambe':-300,'Impilo':-200,'Hamia':-300,'Aspida':-300,
             'Grote':-300,'Mitsuha':-100,
             'Grace':100,'Ralpha':0,'Sanar':0, 'Prim':-100, 'Elias':-400,
             'Yunos':-300,'Munie':-1000,'Anna':-500,'Wanda':-300}

#Randomly selects from a dictionary, deletes selected entry from it and returns the selection
def random_select(dicty): 
    key = random.choice(list(dicty.keys()))
    result = dicty[key]
    del dicty[key]
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
        await game.bot.sendMessage(target.userID,Messages['combat']['res'],parse_mode='HTML')
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
        await game.bot.sendMessage(agent.userID,Messages['combat']['KO'],parse_mode='HTML')
    elif not target.alive:
        await game.bot.sendMessage(target.userID,Messages['combat']['KO'],parse_mode='HTML')
        
    #Finally, return result
    return msg
    
class Game(object):
    def __init__(self,
                 bot,
                 chatID,
                 players):
        self.bot = bot
        self.chatID = chatID
        self.agents = {}
        self.round = 0 # Denotes current round
        playerCount = len(players)
        #determine no. of VIPs and DERP agents to have (both are the same!), and how many people should know per VIP
        if playerCount <= 4:
            VIPCount = 1
            innerCircle = 1
        else:
            VIPCount = (playerCount+1)//3
            innerCircle = 2 if not (playerCount-1)%3 else 1
        self.VIPCount = VIPCount
        self.innerCircle = innerCircle

        #######################################################
        ### Assigning and PM-ing roles and teams to players ###
        #######################################################
    async def allocate(self,players,playerCount,game):
        VIPCount = game.VIPCount
        innerCircle = game.innerCircle
        AGENTS = allAgents()
        
        for count in range(1,playerCount+1):
            player = random_select(players)
            agent = random_select(AGENTS) #returns Hero object
            playerID = player['id'] #same as uerID
            try: #see if user has a username
                username = player['username']
            except KeyError:
                username = player['first_name'] #otherwise use first name as username
            player = agent(playerID,username,player['first_name']) #assign player to hero
            self.agents[player.agentName] = player #save agent into game object
            DB[playerID]=(player,game) # add hero object to database,
            # so that callback queries can be sent to it by CallbackHandler for processing
            # Also, game object is added for retrieving important info by CallbackHandler
            message = Messages['agentDescriptionFirstPerson'][player.agentName]%(player.agentName) #PM player role
            await self.bot.sendMessage(playerID,message,parse_mode='HTML')
            #Assigning teams
            if count <= VIPCount: #first assign DERP agents
                player.team = 'DERP'
                await self.bot.sendMessage(playerID,Messages['teamDERP'])
            elif (playerCount-count) >= VIPCount: #followed by PYRO agents
                player.team = 'PYRO'
                await self.bot.sendMessage(playerID,Messages['teamPYRO'])
            else: #finally PYRO agents
                player.team = 'PYROVIP'
                await self.bot.sendMessage(playerID,Messages['VIPself'])
                if playerCount > 3: #Handle special case when only 3 people, then no need for innerCircle
                    for innerCount in range(0,innerCircle):
                        randomPlayer = random.choice(list(self.get_alive_PYROteam().values()))
                        while randomPlayer.userID == player.userID: #ensure that someone other than the VIP himself is selected
                            randomPlayer = random.choice(list(self.get_alive_PYROteam().values())) 
                            #PM the chosen player
                        await self.bot.sendMessage(randomPlayer.userID,Messages['VIP']%(player.agentName,player.firstName),parse_mode='HTML')

        #Let DERP agents know who is on their team
        DERPmsg = Messages['summary']['teamDERP']
        for agent in list(self.get_all_DERP().values()):
            DERPmsg += Messages['summary']['agent']%(agent.get_idty())
        for agent in list(self.get_all_DERP().values()):
            await self.bot.sendMessage(agent.userID,DERPmsg,parse_mode='HTML')
                                                              
        #Finally, announce player assignment to group chat
        players = self.get_alive_all()
        message = Messages['allotSuccess']
        for agentName,agent in players.items():
            message += Messages['summary']['agentStart']%(agent.username,agentName)
        await self.bot.sendMessage(self.chatID,message,parse_mode='HTML')
        return


        #######################################################
        ######## Logic for running 1 round of the game ########
        #######################################################
    async def next_round(self):
        self.round += 1 #Increment round number
        players = self.get_alive_all()
        for agent in players.values():
            agent.minus_CD()
            await agent.send_query(self.bot,'startQuery',list(players.values()))
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
                await self.bot.sendMessage(agent.userID,Messages['timeUp'])
            except telepot.exception.TelegramError:
                continue
            
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

        #Getting AFK players
        AFK = list(self.get_alive_all().keys())
        for query in imptQueries:
            if query[1] in AFK:
                AFK.remove(query[1])
                
        #Add in self auto-attack queries
        for agent in AFK:
            imptQueries.append((1000,agent,agent,'attack'))
            
        #Process queries!!
        message = Messages['combat']['intro']
        for query in imptQueries:
            message += await proc_query(self,query)
        #If message becomes too long, split up the message to send
        while len(message)>4096:
            idx = message.find('\n',3900) + 2
            await self.bot.sendMessage(self.chatID,message[:idx],parse_mode='HTML')
            message = message[idx:].strip()
            await asyncio.sleep(2)
        await self.bot.sendMessage(self.chatID,message,parse_mode='HTML')

        #Send summary message
        message = Messages['summary']['intro']
        agents = list(self.get_alive_all().values()) #abusing variable name in consideration of memory space
        if agents:
            message += Messages['summary']['aliveStart']
            for agent in agents:
                message += Messages['summary']['alive']%(agent.get_idty(),int(agent.health))
                #At the same time, reset agent statuses for next round
                agent.reset_next_round()
        agents = list(self.get_dead_all())
        if agents:
            message += Messages['summary']['deadStart']
        #A lot of code reuse below, maybe I should modularise it
        agents = list(self.get_dead_DERP().values())
        for agent in agents:
            message += Messages['summary']['deadDERP']%(agent.get_idty())
        agents = list(self.get_dead_PYRO().values())
        for agent in agents:
            message += Messages['summary']['deadPYRO']%(agent.get_idty())
        agents = list(self.get_dead_PYROVIP().values())
        for agent in agents:
            message += Messages['summary']['deadPYROVIP']%(agent.get_idty())
        await self.bot.sendMessage(self.chatID,message,parse_mode='HTML')

        #Check if game should end
        if not self.get_alive_all():
            #Send message that game ends in a draw since everyone is dead
            await self.bot.sendChatAction(self.chatID,action='upload_video')
            await self.bot.sendDocument(self.chatID,Messages['gifs']['drawVidID'])
            await self.bot.sendMessage(self.chatID,Messages['endGame']['draw'],parse_mode='HTML')
            return True
        elif not self.get_alive_DERP():
            #Send message that Team PYRO won as all DERP agents have been killed!
            await self.bot.sendChatAction(self.chatID,action='upload_video')
            await self.bot.sendDocument(self.chatID,Messages['gifs']['PYROVidID'])
            await self.bot.sendMessage(self.chatID,Messages['endGame']['DERP.KO'],parse_mode='HTML')
            return True
        
        elif not self.get_alive_PYROVIP():
            #Send message that Team DERP won as all VIP agents have been assassinated!
            await self.bot.sendChatAction(self.chatID,action='upload_video')
            await self.bot.sendDocument(self.chatID,Messages['gifs']['DERPVidID'])
            await self.bot.sendMessage(self.chatID,Messages['endGame']['PYROVIP.KO'],parse_mode='HTML')
            return True
        
        elif self.round == 25:
            #End game by looking at which team has most health
            #Send message that game will end because it's gone on for far too long
            await self.bot.sendMessage(self.chatID,Messages['endGame']['tooLong'])
            DERPhealth = PYROhealth = 0
            for agent in list(self.get_alive_DERP().values()):
                DERPhealth += agent.health
            for agent in list(self.get_alive_PYROteam().values()):
                PYROhealth += agent.health
            await self.bot.sendMessage(self.chatID,Messages['endGame']['tooLongSummary']%(DERPhealth,PYROhealth),parse_mode='HTML')
            if DERPhealth > PYROhealth:
                await self.bot.sendChatAction(self.chatID,action='upload_video')
                await self.bot.sendDocument(self.chatID,Messages['gifs']['DERPVidID'])
                await self.bot.sendMessage(self.chatID,Messages['endGame']['DERPWin'],parse_mode='HTML')
            elif PYROhealth > DERPhealth:
                await self.bot.sendChatAction(self.chatID,action='upload_video')
                await self.bot.sendDocument(self.chatID,Messages['gifs']['PYROVidID'])
                await self.bot.sendMessage(self.chatID,Messages['endGame']['PYROWin'],parse_mode='HTML')
            else: #In the highly unlikely event of a draw
                await self.bot.sendChatAction(self.chatID,action='upload_video')
                await self.bot.sendDocument(self.chatID,Messages['gifs']['drawVidID'])
                await self.bot.sendMessage(self.chatID,Messages['endGame']['rareDraw'],parse_mode='HTML')
            return True
        return False

    #To delete all entries in DB
    async def end_game(self):
        #Announce who was in which team, at the same time, remove them from DB
        #Start with team DERP
        agents = self.get_all_DERP()
        msg = Messages['summary']['endIntro'] + Messages['summary']['teamDERP']
        for agent in agents.values():
            del DB[agent.userID]
            msg += Messages['summary']['agent']%(agent.get_idty())
            
        #Then team PYRO
        agents = self.get_all_PYROteam()
        msg += Messages['summary']['teamPYRO']
        for agent in agents.values():
            del DB[agent.userID]
            if agent.team == 'PYROVIP':
                msg += Messages['summary']['VIP']%(agent.get_idty())
            else:
                msg += Messages['summary']['agent']%(agent.get_idty())

        #Send message
        await self.bot.sendMessage(self.chatID,msg,parse_mode='HTML')
        
        #Finally delete in DB
        del DB[self.chatID]
    
    
    
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
