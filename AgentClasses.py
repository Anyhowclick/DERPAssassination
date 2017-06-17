import telepot
from telepot.namedtuple import *
from Agent import Agent
from Messages import send_message, edit_message
from DatabaseStats import DBP, LANG

    
#####################
###### OFFENSE ######
#####################

#Offense heroes can have their ults powered up, except for 2 (Taiji & Saitami)
class Offense(Agent):
    def __init__(self, agentName, userID, username, firstName, Messages,
                 baseHealth=None, baseDmg=25, baseUltCD=None, baseUltDmg=0, ultDmg=None,
                 alive=True,health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=True, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None,
                 ):
        
        #set ult default damage for Offense Class
        self.baseUltDmg = baseUltDmg
        self.ultDmg = ultDmg if ultDmg else self.baseUltDmg
        
        super().__init__(agentName, userID, username, firstName, Messages,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    def reset_ult_dmg(self):
        self.ultDmg = self.baseUltDmg

    def add_ult_dmg(self,dmg): #dmg > 0 = add, dmg < 0 = reduce
        self.ultDmg += dmg

    def reset_next_round(self):
        super().reset_next_round()
        self.reset_ult_dmg()


    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'default')


    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_default(self,game,queryData)
        return
    
        
####################
####### TANK #######
####################
        
class Tank(Agent):
    def __init__(self, agentName, userID, username, firstName, Messages,
                 baseHealth=130, baseDmg=20, baseUltCD=3,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=0.02, protector=None
                 ):
        
        super().__init__(agentName, userID, username, firstName, Messages,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'default')


    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_default(self,game,queryData)
        return
    

####################
###### HEALER ######
####################

# Note that Healers have extra attributes: baseHealAmt and healAmt, and thus, have extra methods too

class Healer(Agent):
    def __init__(self, agentName, userID, username, firstName, Messages,
                 baseHealth=90, baseDmg=17, baseUltCD=3, baseHealAmt=10,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, healAmt=None, attackAfterUlt=False,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=0.1, protector=None
                 ):
        #set defaults for baseHealAmt and healAmt
        self.baseHealAmt = baseHealAmt
        self.healAmt = self.baseHealAmt
        self.canHeal = True

        super().__init__(agentName, userID, username, firstName, Messages,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)

    def reset_heal_amt(self):
        self.healAmt = self.baseHealAmt

    def reset_can_heal(self):
        self.canHeal = True
    
    def heal(self,ally,amt=0):
        amt = amt if amt else self.healAmt
        
        if self == ally:
            if self.canHeal and self.canBeHealed:
                self.add_health(0.5*amt)
                return self.Messages['combat']['selfHeal']%(self.get_idty(),self.health)
            else:
                return self.Messages['combat']['failHealSelf']%(self.get_idty())
            
        elif self.canHeal and ally.canBeHealed:
            ally.add_health(amt)
            return self.Messages['combat']['heal']%(ally.get_idty(),ally.health,self.get_idty())
        return self.Messages['combat']['failHeal']%(self.get_idty(),ally.get_idty())

    def add_heal_amt(self,amt):
        self.healAmt += amt

    def reset_next_round(self):
        super().reset_next_round()
        self.reset_heal_amt()
        self.reset_can_heal()
        
    ################
    ## SEND QUERY ##
    ################
    #refer to flowchart for greater clarity
    async def send_query(self,bot,data,players):
        await send_query(self,bot,data,players,'default')


    ###################
    ## PROCESS QUERY ##
    ###################
    async def process_query(self,game,queryData):
        await process_query_default(self,game,queryData)
        return

######################
###### SUPPPORT ######
######################
            
class Support(Agent):
    def __init__(self, agentName, userID, username, firstName, Messages,
                 baseHealth=None, baseDmg=None, baseUltCD=None,
                 alive=True, health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None
                 ):
        
        super().__init__(agentName, userID, username, firstName, Messages,
                         baseHealth, baseDmg, baseUltCD,
                         alive, health, dmg,
                         ultCD, ultAvail, ultUsed, buffUlt, attackAfterUlt,
                         canBeHealed, canBeShielded,
                         asleep, invuln, controlled, shield, dmgReduction, protector)   
