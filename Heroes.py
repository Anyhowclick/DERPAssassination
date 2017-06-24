#Each hero might have extra attributes for ulti
from AgentClasses import *
from Messages import *
from Shield import Shield
import random
import Globals

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

#Generate a list of 1 instance of each character
#Compulsory contains all agents that will definitely be included every game
def one_agent_instance(playerCount):
    compulsory = {'Elias':Elias}
    result = {'Sonhae':Sonhae, #'Taiji':Taiji, 'Dracule':Dracule,
              'Novah':Novah, 'Saitami':Saitami, 'Grim':Grim,
              'Jordan':Jordan, 'Jigglet':Jigglet,
              'Harambe':Harambe, 'Hamia':Hamia, 'Impilo':Impilo,
              'Prim':Prim, 'Ralpha':Ralpha,'Sanar':Sanar,
              'Anna':Anna, 'Munie':Munie, 'Wanda':Wanda,
              'Aspida':Aspida,
            }
    #Exclude Elias
    if playerCount <= 4:
        return result

    #Making sure Elias (and potentially other agents in the future) is included otherwise
    for i in range(0,playerCount-len(compulsory)):
        key = list(result.keys())
        key = random.choice(key)
        compulsory[key] = result[key]
        del result[key]
    return compulsory

#########################################
############# OFFENSE CLASS #############
#########################################

#####################
###### DRACULE ######
#####################

class Dracule(Offense):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#baa', userID, username, firstName, Messages)
        
    def ult(self,target): #target is self
        result = super().ult()
        if result:
            return result
        return self.Messages['combat']['ult']['Dracule']%(self.get_idty())

    def attack(self,enemy,msg='',code=0):
        #60% of base damage
        recoveredHp = 0.6*self.dmg
        msg += super().attack(enemy,msg=msg,code=code)
        while enemy.is_protected() and enemy.protector != enemy:
           enemy = enemy.protector
        if self.ultUsed and not self.canBeHealed:
            return msg + self.Messages['combat']['failHealSelf']%(self.get_idty())
        elif self.ultUsed and not enemy.invuln:
            self.add_health(recoveredHp)
            self.add_stats_heal(recoveredHp)
            return msg + self.Messages['combat']['recover']%(self.get_idty(),recoveredHp)
        return msg


##################
###### GRIM ######
##################
            
class Grim(Offense):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bab', userID, username, firstName, Messages,
                         baseDmg=22, baseUltCD=3, baseUltDmg=25, attackAfterUlt=False)
        self.selected = []

    def reset_next_round(self):
        self.selected = []
        super().reset_next_round()
        
    def ult(self,enemy):
        result = super().ult()
        if result:
            return result
        return self.attack(enemy,dmg=self.ultDmg,msg=self.Messages['combat']['ult']['Grim']%(self.get_idty(),enemy.get_idty()),code=1)

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'multi',gameMode)
        return
    
    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,('multi',3))
        return

####################
###### JORDAN ######
####################
            
class Jordan(Offense):
    def __init__(self, userID, username, firstName, Messages):
        self.selected = None #Will be an agent
        super().__init__('#bac', userID, username, firstName, Messages,
                         baseDmg=22, baseUltCD=5)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        if target.invuln:
            return self.Messages['combat']['ultInvuln']%(self.get_idty(),target.get_idty(),target.get_idty())
        #Use on self
        elif self == target:
            return self.Messages['combat']['ult']['JordanSelf']%(self.get_idty())
        #Split health 50-50 (ratio might change in the future)
        self.health = (self.health + target.health) / 2
        target.health = self.health
        return self.Messages['combat']['ult']['Jordan']%(self.get_idty(),target.get_idty(),self.health)
        
        
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return
    
    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return

###################
###### NOVAH ######
###################

class Novah(Offense):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bad', userID, username, firstName, Messages)

    def ult(self,target): #target is self
        if self.asleep:
            #insert asleep message
            return self.Messages['combat']['sleepUlt']%(self.get_idty())
        elif self.health <= 5:
            #Not enough health to sacrifice
            return self.Messages['combat']['ult']['NovahNOK']%(self.get_idty())
        else:
            self.ultUsed = True
            self.reset_ult_avail()
            self.reset_ult_CD()
            self.add_dmg(10)
            return self.drop_health(5, self.Messages['combat']['ult']['NovahOK']%(self.get_idty()))

        
#####################
###### SAITAMI ######
#####################
            
class Saitami(Offense):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bae', userID, username, firstName, Messages,
                         baseUltCD=4, attackAfterUlt=False)
        self.poweredUp = False

    def ult(self,enemy):
        result = super().ult()
        if result:
            return result
        while enemy.is_protected(): #Need to get the target in order to calculate dmg to deal
            enemy = enemy.protector
        if enemy.invuln:
            return self.Messages['combat']['ultInvuln']%(self.get_idty(),enemy.get_idty(),enemy.get_idty())
        if self.poweredUp: #Instant-KO
            self.add_stats_killed(enemy)
            return self.Messages['combat']['ult']['SaitamiPower']%(self.get_idty(),enemy.get_idty()) + enemy.die()
        else:
            enemy.health = 1
            return self.Messages['combat']['ult']['Saitami']%(enemy.get_idty(),self.get_idty())

    def buff_ult(self):
        self.poweredUp = True
        
    def reset_next_round(self):
        super().reset_next_round()
        self.poweredUp = False
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return


        
######################
####### SONHAE #######
######################

class Sonhae(Offense):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#baf', userID, username, firstName, Messages,
                         baseUltCD=3,attackAfterUlt=False,
                         baseHealth=85, baseDmg=30, baseUltDmg=40)

    def ult(self,enemy):
        result = super().ult()
        if result:
            return result
        #Pagoe uses sticky bomb (message for this)
        return self.attack(enemy,dmg=self.ultDmg,msg=self.Messages['combat']['ult']['Sonhae']%(self.get_idty(),enemy.get_idty()),code=1)
        
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return
        
    
#####################
####### TAIJI #######
#####################

class Taiji(Offense):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bag', userID, username, firstName, Messages,
                         baseUltCD=3,buffUlt=False)
        
    def ult(self,target): #target is self
        result = super().ult()
        if result:
            return result
        return self.Messages['combat']['ult']['Taiji']%(self.get_idty())

    def attacked(self,enemy,dmg,msg='',code=0):
        if self.ultUsed and self != enemy:
            self.protector = enemy
            msg += self.Messages['combat']['deflect']%(self.get_idty(),enemy.get_idty())
        return super().attacked(enemy,dmg=dmg,msg=msg,code=code)


######################################
############# TANK CLASS #############
######################################
        
####################
###### ASPIDA ######
####################

class Aspida(Tank):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bba', userID, username, firstName, Messages,
                         buffUlt=True,baseUltCD=3)
        self.shieldAmt = 40
        
    def ult(self,target):
        result = super().ult()
        if result:
            return result
        elif not target.canBeShielded:
            return self.Messages['combat']['failShield']%(self.get_idty(),target.get_idty())
        target.shield = Shield(self.shieldAmt)
        if self == target:
            return self.Messages['combat']['ult']['AspidaSelf']%(self.get_idty(),self.shieldAmt)
        return self.Messages['combat']['ult']['Aspida']%(self.get_idty(),self.shieldAmt,target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return

        
###################
###### HAMIA ######
###################

class Hamia(Tank):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bbb', userID, username, firstName, Messages,
                         buffUlt=True,baseUltCD=2)
        self.baseUltDmgReduction = 0.5
        self.ultDmgReduction = self.baseUltDmgReduction

    def reset_next_round(self):
        super().reset_next_round()
        self.ultDmgReduction = self.baseUltDmgReduction

    def add_ult_dmg_reduction(self,amt):
        self.ultDmgReduction += amt

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        target.add_dmg_reduction(self.ultDmgReduction)
        return self.Messages['combat']['ult']['Hamia']%(self.get_idty(),target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return

        
#####################
###### HARAMBE ######
#####################

class Harambe(Tank):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bbc', userID, username, firstName, Messages,
                         baseHealth=130)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        target.protector = self
        return self.Messages['combat']['ult']['Harambe']%(self.get_idty(),target.get_idty())
    
    def attacked(self,enemy,dmg,msg='',code=0):
        if not self.ultUsed:
            return super().attacked(enemy,dmg=dmg,msg=msg,code=code)
        recoveredHp = self.health
        msg = super().attacked(enemy,dmg,msg)
        recoveredHp = 0.25*(recoveredHp-self.health)
        if not self.canBeHealed:
            return msg + self.Messages['combat']['failHealSelf']%(self.get_idty())
        elif recoveredHp <= 0:
            return msg
        self.add_health(recoveredHp)
        self.add_stats_heal(recoveredHp)
        return msg + self.Messages['combat']['recover']%(self.get_idty(),recoveredHp)
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return



####################
###### IMPILO ######
####################

class Impilo(Tank):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bbd', userID, username, firstName, Messages,
                         buffUlt=True,baseUltCD=4)

        self.baseUltDmgReduction,self.baseUltHp = 0.05,20
        self.ultDmgReduction,self.ultHp = self.baseUltDmgReduction,self.baseUltHp
        
    def reset_next_round(self):
        super().reset_next_round()
        self.ultDmgReduction,self.ultHp = self.baseUltDmgReduction,self.baseUltHp

    def add_ult_dmg_reduction(self,amt):
        self.ultDmgReduction += amt

    def add_ult_health(self,amt):
        self.ultHp += amt
    
    def ult(self,target): #target is self
        result = super().ult()
        if result:
            return result
        self.add_dmg_reduction(self.ultDmgReduction)
        recoveredHp = max(0.25*self.health,self.ultHp)
        if not self.canBeHealed:
            return self.Messages['combat']['ImpiloFailHeal']%(self.get_idty())
        self.add_health(recoveredHp) #Recover 25% of remaining health or ult hp (20++), whichever is higher
        self.add_stats_heal(recoveredHp)
        return self.Messages['combat']['ult']['Impilo']%(self.get_idty(),recoveredHp)


########################################
############# HEALER CLASS #############
########################################

###################
###### ELIAS ######
###################

class Elias(Healer):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bca', userID, username, firstName, Messages,
                         baseUltCD=2,attackAfterUlt=True)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        if target == self:
            return self.Messages['combat']['ult']['EliasSelf']%(self.get_idty())
        elif target.invuln:
            return self.Messages['combat']['ultInvuln']%(self.get_idty(),target.get_idty(),target.get_idty())
        return self.Messages['combat']['ult']['Elias']%(self.get_idty(),target.get_idty())

    async def reveal(self,target,game):
        Messages = Globals.LANG[self.userID]
        if target.invuln:
            msg = Messages['combat']['ult']['revealFail']%(target.get_idty())
        else:
            if target.team == 'PYRO':
                msg = Messages['combat']['teamPYRO']
            elif target.team == 'PYROVIP':
                msg = Messages['combat']['teamPYROVIP']
            else:
                msg = Messages['combat']['teamDERP']
            if target == self:
                msg = Messages['combat']['ult']['EliasSelfPrivate']%(msg)
            else:
                msg = Messages['combat']['ult']['EliasPrivate']%(target.get_idty(),msg)
        await send_message(game.bot,self.userID,msg)
        return

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return
        
    
####################
###### RALPHA ######
####################

class Ralpha(Healer):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bcc', userID, username, firstName, Messages,
                         baseUltCD=4)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        beforeHealth = target.health
        target.reset_health()
        #Reset to 70% of base health if self
        if self == target:
            self.drop_health(0.3*self.health)
            #Target's health increased compared to last time
            if self.health >= beforeHealth:
                self.add_stats_heal(self.health - beforeHealth)
                return self.Messages['combat']['ult']['RalphaSelf']%(self.get_idty())
            #Otherwise reset back to before ability was used
            else:
                target.health = beforeHealth 
                return self.Messages['combat']['failHealSelf']%(self.get_idty())

        #Otherwise reset to 80% of base health
        else:
            target.drop_health(0.2*self.health)
            #Target's health increased compared to last time
            if target.health >= beforeHealth:
                self.add_stats_heal(target.health - beforeHealth)
                self.add_stats_healed(target)
                return self.Messages['combat']['ult']['Ralpha']%(self.get_idty(),target.get_idty())
            #Otherwise reset back to before ability was used
            else:
                target.health = beforeHealth 
                return self.Messages['combat']['failHeal']%(self.get_idty(),target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return
        

###################
###### SANAR ######
###################
        
class Sanar(Healer):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bcd', userID, username, firstName, Messages,
                         buffUlt=True)
        self.selected = []
        self.ultBaseHealAmt = 20
        self.ultHealAmt = self.ultBaseHealAmt

    def reset_ult_heal_amt(self):
        self.ultHealAmt = self.ultBaseHealAmt

    def add_ult_heal_amt(self,amt):
        self.ultHealAmt += amt
        
    def reset_next_round(self):
        self.selected = []
        self.reset_ult_heal_amt()
        super().reset_next_round()
        
    def ult(self,ally):
        result = super().ult()
        if result:
            return result
        return self.heal(ally,self.ultHealAmt)

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'multi',gameMode)
        return
    
    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,('multi',3))
        return

##################
###### PRIM ######
##################

class Prim(Healer):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bcb', userID, username, firstName, Messages, attackAfterUlt=True,
                         baseUltCD=3)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        elif target == self:
            return self.Messages['combat']['ult']['PrimSelf']%(self.get_idty())
        target.ultAvail = True
        target.ultCD = 0
        return self.Messages['combat']['ult']['Prim']%(self.get_idty(),target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return
        
        
#########################################
############# SUPPORT CLASS #############
#########################################

##################
###### ANNA ######
##################
class Anna(Support):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bda', userID, username, firstName, Messages,
                         baseUltCD=2)

    def ult(self,ally):
        result = super().ult()
        if result:
            return result
        #add damage
        ally.add_dmg(0.2*ally.dmg)
        #add heal amount for healers
        if isinstance(ally,Healer):
            ally.add_heal_amt(0.5*ally.baseHealAmt)
            
        if ally.buffUlt: #Ability can be buffed
            if isinstance(ally,Offense): #or isinstance(ally,Simo):
                ally.add_ult_dmg(0.2*ally.baseUltDmg)

            elif isinstance(ally,Sanar):
                ally.add_ult_heal_amt(5)

            elif isinstance(ally,Impilo):
                ally.add_ult_dmg_reduction(0.05)
                ally.add_ult_health(10)

            elif isinstance(ally,Hamia):
                ally.add_ult_dmg_reduction(0.2)

            elif isinstance(ally,Saitami):
                ally.buff_ult()
            # elif ally.agentName in ('Aspida','Yunos'):
                #TO-DO: Increase provide shield amt

        if ally == self:
            return self.Messages['combat']['ult']['AnnaSelf']%(self.get_idty())    
        return self.Messages['combat']['ult']['Anna']%(ally.get_idty(),self.get_idty())

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return


#####################
###### JIGGLET ######
#####################
class Jigglet(Support):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bdb', userID, username, firstName, Messages,
                         baseUltCD=3)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        if target.invuln:
            return self.Messages['combat']['ultInvuln']%(self.get_idty(),target.get_idty(),target.get_idty())
        #Target goes to sleep!
        target.asleep = True
        if target == self:
            return self.Messages['combat']['ult']['JiggletSelf']%(self.get_idty())
        return self.Messages['combat']['ult']['Jigglet']%(self.get_idty(),target.get_idty())

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return

        
###################
###### MUNIE ######
###################
class Munie(Support):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bdc', userID, username, firstName, Messages,
                         baseUltCD=3)

    def ult(self,ally):
        result = super().ult()
        if result:
            return result
        ally.invuln = True
        if ally == self:
            return self.Messages['combat']['ult']['MunieSelf']%(self.get_idty())
        return self.Messages['combat']['ult']['Munie']%(self.get_idty(),ally.get_idty())
    

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return


###################
###### WANDA ######
###################
class Wanda(Support):
    def __init__(self, userID, username, firstName, Messages):
        super().__init__('#bdd', userID, username, firstName, Messages,
                         baseUltCD=3)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        if target.invuln:
            return self.Messages['combat']['ultInvuln']%(self.get_idty(),target.get_idty(),target.get_idty())

        if isinstance(target,Healer):
            target.canHeal = False
            target.canBeHealed = False
            self.ultCD = 4
            return self.Messages['combat']['ult']['WandaHealer']%(self.get_idty(),target.get_idty())
        
        target.canBeHealed = False
        self.ultCD = 3
        if target == self:
            return self.Messages['combat']['ult']['WandaSelf']%(self.get_idty())
        return self.Messages['combat']['ult']['Wanda']%(self.get_idty(),target.get_idty())

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players,gameMode):
        await send_query(self,bot,data,players,'single',gameMode)
        return

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query(self,game,queryData,'single')
        return
        
# TO-DO: SIMO MUST HAVE addUltDmg method, Aspida and Yunos to have shield methods
