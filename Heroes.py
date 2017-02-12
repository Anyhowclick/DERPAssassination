#Each hero might have extra attributes for ulti
from AgentClasses import *
from Messages import Messages, send_message
from Database import DB
from Shield import Shield

#Generate a list of 1 instance of each character
def allAgents():
    return {'Sonhae':Sonhae, 'Taiji':Taiji, 'Dracule':Dracule, 
            'Novah':Novah, 'Saitami':Saitami, 'Grim':Grim,
            'Harambe':Harambe, 'Hamia':Hamia, 'Impilo':Impilo, 
            'Elias':Elias, 'Prim':Prim, 'Ralpha':Ralpha,'Sanar':Sanar,
            'Anna':Anna, 'Munie':Munie, 'Wanda':Wanda,
            'Aspida':Aspida,
            } 

#########################################
############# OFFENSE CLASS #############
#########################################

######################
####### SONHAE #######
######################

class Sonhae(Offense):
    def __init__(self, userID, username, firstName):
        super().__init__('Sonhae', userID, username, firstName,
                         baseUltCD=3,attackAfterUlt=False,
                         baseHealth=85, baseDmg=30, baseUltDmg=40)

    def ult(self,enemy):
        result = super().ult()
        if result:
            return result
        #Pagoe uses sticky bomb (message for this)
        return self.attack(enemy,self.ultDmg,msg=Messages['combat']['ult']['Sonhae']%(self.get_idty(),enemy.get_idty()))
        
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)
        
    
#####################
####### TAIJI #######
#####################

class Taiji(Offense):
    def __init__(self, userID, username, firstName):
        super().__init__('Taiji', userID, username, firstName,
                         baseUltCD=3,buffUlt=False)
        
    def ult(self,target): #target is self
        result = super().ult()
        if result:
            return result
        return Messages['combat']['ult']['Taiji']%(self.get_idty())

    def attacked(self,enemy,dmg,msg=''):
        if self.ultUsed and self != enemy:
            self.protector = enemy
            msg += Messages['combat']['deflect']%(self.get_idty(),enemy.get_idty())
        return super().attacked(enemy,dmg,msg)



            
#####################
###### DRACULE ######
#####################

class Dracule(Offense):
    def __init__(self, userID, username, firstName):
        super().__init__('Dracule', userID, username, firstName)
        
    def ult(self,target): #target is self
        result = super().ult()
        if result:
            return result
        return Messages['combat']['ult']['Dracule']%(self.get_idty())

    def attack(self,enemy,msg=''):
        recoveredHp = self.dmg
        msg += super().attack(enemy)
        while enemy.is_protected():
           enemy = enemy.protector
        if self.ultUsed and not self.canBeHealed:
            return msg + Messages['combat']['failHealSelf']%(self.get_idty())
        if self.ultUsed and not enemy.invuln:
            self.add_health(recoveredHp) #100% lifesteal
            return msg + Messages['combat']['recover']%(self.get_idty(),recoveredHp)
        return msg
        


        
###################
###### NOVAH ######
###################

class Novah(Offense):
    def __init__(self, userID, username, firstName):
        super().__init__('Novah', userID, username, firstName)

    def ult(self,target): #target is self
        if self.asleep:
            #insert asleep message
            return Messages['combat']['sleepUlt']%(self.get_idty())
        elif self.health <= 5:
            #Not enough health to sacrifice
            return Messages['combat']['ult']['NovahNOK']%(self.get_idty())
        else:
            self.ultUsed = True
            self.reset_ult_avail()
            self.reset_ult_CD()
            self.add_dmg(10)
            return self.drop_health(5, Messages['combat']['ult']['NovahOK']%(self.get_idty()))



#####################
###### SAITAMI ######
#####################
            
class Saitami(Offense):
    def __init__(self, userID, username, firstName):
        super().__init__('Saitami', userID, username, firstName,
                         baseUltCD=4, attackAfterUlt=False)

    def ult(self,enemy):
        result = super().ult()
        if result:
            return result
        while enemy.is_protected(): #Need to get the target in order to calculate dmg to deal
            enemy = enemy.protector
        if enemy.invuln:
            return Messages['combat']['ultInvuln']%(self.get_idty(),enemy.get_idty(),enemy.get_idty())
        enemy.health = 1
        return Messages['combat']['ult']['Saitami']%(self.get_idty(),enemy.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)


##################
###### GRIM ######
##################
            
class Grim(Offense):
    def __init__(self, userID, username, firstName):
        super().__init__('Grim', userID, username, firstName,
                         baseUltDmg=30, attackAfterUlt=False)
        self.selected = []

    def reset_next_round(self):
        self.selected = []
        super().reset_next_round()
        
    def ult(self,enemy):
        result = super().ult()
        if result:
            return result
        return self.attack(enemy,dmg=self.ultDmg,msg=Messages['combat']['ult']['Grim']%(self.get_idty(),enemy.get_idty()))

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'multi')

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_multi(self,game,queryData,3)



######################################
############# TANK CLASS #############
######################################
        
####################
###### ASPIDA ######
####################

class Aspida(Tank):
    def __init__(self, userID, username, firstName):
        super().__init__('Aspida', userID, username, firstName,
                         buffUlt=True,baseUltCD=3)
        self.shieldAmt = 40
        
    def ult(self,target):
        result = super().ult()
        if result:
            return result
        elif not target.canBeShielded:
            return Messages['combat']['failShield']%(self.get_idty(),target.get_idty())
        target.shield = Shield(self.shieldAmt)
        if self == target:
            return Messages['combat']['ult']['AspidaSelf']%(self.get_idty(),self.shieldAmt)
        return Messages['combat']['ult']['Aspida']%(self.get_idty(),target.get_idty(),self.shieldAmt)
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)

        
###################
###### HAMIA ######
###################

class Hamia(Tank):
    def __init__(self, userID, username, firstName):
        super().__init__('Hamia', userID, username, firstName,
                         buffUlt=True,baseUltCD=1)
        self.baseUltDmgReduction = 0.05
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
        return Messages['combat']['ult']['Hamia']%(self.get_idty(),target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)

        
#####################
###### HARAMBE ######
#####################

class Harambe(Tank):
    def __init__(self, userID, username, firstName):
        super().__init__('Harambe', userID, username, firstName,
                         baseHealth=150)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        target.protector = self
        return Messages['combat']['ult']['Harambe']%(self.get_idty(),target.get_idty())
    
    def attacked(self,enemy,dmg,msg=''):
        if not self.ultUsed:
            return super().attacked(enemy,dmg,msg)
        recoveredHp = self.health
        msg = super().attacked(enemy,dmg,msg)
        recoveredHp = 0.25*(recoveredHp-self.health)
        if not self.canBeHealed:
            return msg + Messages['combat']['failHealSelf']%(self.get_idty())
        elif not recoveredHp:
            return msg
        self.add_health(recoveredHp)
        return msg + Messages['combat']['recover']%(self.get_idty(),recoveredHp)
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)



####################
###### IMPILO ######
####################

class Impilo(Tank):
    def __init__(self, userID, username, firstName):
        super().__init__('Impilo', userID, username, firstName,
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
            return Messages['combat']['ImpiloFailHeal']%(self.get_idty())
        self.add_health(recoveredHp) #Recover 25% of remaining health or ult hp (20++), whichever is higher
        return Messages['combat']['ult']['Impilo']%(self.get_idty(),recoveredHp)


########################################
############# HEALER CLASS #############
########################################

###################
###### ELIAS ######
###################

class Elias(Healer):
    def __init__(self, userID, username, firstName):
        super().__init__('Elias', userID, username, firstName,
                         baseUltCD=2,attackAfterUlt=True)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        if target == self:
            return Messages['combat']['ult']['EliasSelf']%(self.get_idty())
        elif target.invuln:
            return Messages['combat']['ultInvuln']%(self.get_idty(),target.get_idty(),target.get_idty())
        return Messages['combat']['ult']['Elias']%(self.get_idty(),target.get_idty())

    async def reveal(self,target,game):
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
        await send_message(game.bot,self.userID,msg,parse_mode='HTML')
        return

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)
        
    
####################
###### RALPHA ######
####################

class Ralpha(Healer):
    def __init__(self, userID, username, firstName):
        super().__init__('Ralpha', userID, username, firstName,
                         baseUltCD=4)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        target.reset_health()
        if self == target:
            self.drop_health(0.2*self.health)
            return Messages['combat']['ult']['RalphaSelf']%(self.get_idty())
        return Messages['combat']['ult']['Ralpha']%(self.get_idty(),target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)
        

###################
###### SANAR ######
###################
        
class Sanar(Healer):
    def __init__(self, userID, username, firstName):
        super().__init__('Sanar', userID, username, firstName,
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
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'multi')

    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_multi(self,game,queryData,3)

##################
###### PRIM ######
##################

class Prim(Healer):
    def __init__(self, userID, username, firstName):
        super().__init__('Prim', userID, username, firstName, attackAfterUlt=True,
                         baseUltCD=3)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        elif target == self:
            return Messages['combat']['ult']['PrimSelf']%(self.get_idty())
        target.ultAvail = True
        target.ultCD = 0
        return Messages['combat']['ult']['Prim']%(self.get_idty(),target.get_idty())
    
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)

        
        
#########################################
############# SUPPORT CLASS #############
#########################################

###################
###### MUNIE ######
###################
class Munie(Support):
    def __init__(self, userID, username, firstName):
        super().__init__('Munie', userID, username, firstName,
                         baseUltCD=3)

    def ult(self,ally):
        result = super().ult()
        if result:
            return result
        ally.invuln = True
        if ally == self:
            return Messages['combat']['ult']['MunieSelf']%(self.get_idty())
        return Messages['combat']['ult']['Munie']%(self.get_idty(),ally.get_idty())
        


    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)

        
##################
###### ANNA ######
##################
class Anna(Support):
    def __init__(self, userID, username, firstName):
        super().__init__('Anna', userID, username, firstName,
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
                ally.add_ult_dmg_reduction(0.08)
            # elif ally.agentName in ('Aspida','Yunos'):
                #TO-DO: Increase provide shield amt

        if ally == self:
            return Messages['combat']['ult']['AnnaSelf']%(self.get_idty())    
        return Messages['combat']['ult']['Anna']%(ally.get_idty(),self.get_idty())

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)


###################
###### WANDA ######
###################
class Wanda(Support):
    def __init__(self, userID, username, firstName):
        super().__init__('Wanda', userID, username, firstName,
                         baseUltCD=3)

    def ult(self,target):
        result = super().ult()
        if result:
            return result
        if target.invuln:
            return Messages['combat']['ultInvuln']%(self.get_idty(),target.get_idty(),target.get_idty())

        if isinstance(target,Healer):
            target.canHeal = False
            target.canBeHealed = False
            self.ultCD = 4
            return Messages['combat']['ult']['WandaHealer']%(self.get_idty(),target.get_idty())
        
        target.canBeHealed = False
        self.ultCD = 3
        if target == self:
            return Messages['combat']['ult']['WandaSelf']%(self.get_idty())
        return Messages['combat']['ult']['Wanda']%(self.get_idty(),target.get_idty())

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'single')

    ###################
    ## PROCESS QUERY ##
    ###################
    #refer to flowchart for greater clarity
    async def process_query(self,game,queryData):
        await process_query_single(self,game,queryData)
        
# TO-DO: SIMO MUST HAVE addUltDmg method, Aspida and Yunos to have shield methods
