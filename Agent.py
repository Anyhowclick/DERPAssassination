import Globals

#defining character class
class Agent(object):

#### Constructor #####
    def __init__(self, agentCode, userID, username, firstName, Messages,
                 baseHealth=None, baseDmg=None, baseUltCD=None,
                 alive=True,health=None, dmg=None,
                 ultCD=None, ultAvail=False, ultUsed=False, buffUlt=False, attackAfterUlt=True,
                 canBeHealed=True, canBeShielded=True,
                 asleep=False, invuln=False, controlled=False, shield=None, dmgReduction=None, protector=None,
                 ):
        self.agentName = Messages['agents'][agentCode][0]#Name of agent assigned, obtain from Messages.py Eg. Sonhae, Impilo
        self.agentCode = agentCode #Special code to identify the agent in Messages.py Eg. #baa, #bab etc.
        self.userID = userID #telegram user ID
        self.username = username #telegram username
        self.firstName = firstName #telegram user first name
        self.editor = None #to be initialised if there's a callback query
        self.Messages = Messages #this is the language database for the group chat
        self.stats = {
            "pplHealed":{}, #Unique ppl healed.
            "pplKilled":{}, #Unique ppl killed.
            "healAmt":0,
            "dmg":0,
            }
        
        #Base values for health = 100, damage = 15 and ulti cooldown = 3
        self.baseHealth = baseHealth if baseHealth else 100
        self.baseDmg = baseDmg if baseDmg else 20
        self.baseUltCD = baseUltCD if baseUltCD else 2 #no. of turns left for ult to be ready
        
        #Set alive status, health, dmg and ulti cooldown
        self.alive = alive
        self.team = None #Team is either "DERP", "PYRO", or "PYROVIP"
        self.health = health if health else self.baseHealth
        self.dmg = dmg if dmg else self.baseDmg
        
        #Ulti attributes
        self.ultCD = self.baseUltCD
        self.ultAvail = ultAvail #availability of ulti
        self.ultUsed = ultUsed #states if ability is being used this turn
        self.buffUlt = buffUlt #boolean value stating whether ult can be powered up
        self.attackAfterUlt = attackAfterUlt #boolean value stating whether agent can attack after ult activation
        self.canBeHealed = canBeHealed #boolean value stating whether agent can be healed
        self.canBeShielded = canBeShielded #boolean value stating whether agent can be healed
        
        #Possible statuses initialisation to false / None
        self.asleep = asleep
        self.invuln = invuln
        self.controlled = controlled
        self.shield = shield
        self.dmgReduction = dmgReduction if dmgReduction else 0 #10% reduction = 0.1
        self.protector = protector #Protector object so that all damage can be deflected to him
        

        
## User info accessors ##
    def get_user_info(self):
        return (self.userID,self.firstName)

    def get_idty(self): #Returns only agent name, to keep messages shorter
        return '<b>' + self.agentName + '</b>'

    def get_full_idty(self): #Returns agentName together with clickable first name (assuming user has username)
        if self.username:
            return self.agentName + " " + "<a href='http://telegram.me/" + self.username + "'>(" + self.firstName + ")</a>"
        return self.agentName + '<b> (' + self.firstName + ')</b>'

    def get_clickable_name(self): #Returns just the first name of the person, together with link if user has username
        if self.username:
            return "<a href='http://telegram.me/" + self.username + "'>" + self.firstName + "</a>"
        return '<b>' + self.firstName + '</b>'
    
    def get_idty_query(self): #Returns a string as such. AgentName(firstName), without bold tags for query display
        return self.agentName + ' (' + self.firstName + ')'
    
## Status accessors ##

    def is_shielded(self):
        return True if self.shield else False

    def is_protected(self):
        return True if self.protector else False


##### Methods #####
    
    ### resetting current health, dmg and ult to that of base
    def reset_health(self):
        self.health = self.baseHealth

    def reset_dmg(self):
        self.dmg = self.baseDmg

    def reset_ult_CD(self):
        self.ultCD = self.baseUltCD

    def reset_ult_avail(self):
        self.ultAvail = False

    def reset_ult_used(self):
        self.ultUsed = False

    def reset_can_be_healed(self):
        self.canBeHealed = True

    def reset_can_be_shielded(self):
        self.canBeShielded = True

    ### reset alive status, shield amount, dmg reduction, protector
    def reset_alive(self):
        self.alive = True

    def reset_shield(self):
        self.shield = None

    def reset_dmg_reduction(self):
        self.dmgReduction = 0

    def reset_protector(self):
        self.protector = None

    ### increasing / decreasing health, dmg

    def add_health(self,hp):
        self.health = min(self.health+hp, self.baseHealth)

    
    def drop_health(self,hp,enemy,msg=str('')):
        self.health = max(self.health-hp, 0)
        if (not self.health):
            enemy.add_stats_killed(self) #stats method found below
            return msg + self.die()
        return msg
        

    def add_dmg(self,dmg): #dmg > 0 = addDmg, dmg < 0 = reduceDmg
        self.dmg += dmg

    def add_dmg_reduction(self,amt):
        self.dmgReduction += amt
            
    ### player killed ###
    def die(self):
        self.reset()
        self.alive = False
        return self.Messages['combat']['die']%(self.get_idty())

    def reset_status(self):
        self.asleep, self.invuln, self.controlled, = (False,)*3

    ### reset for next round ###
    def reset_next_round(self):
        self.reset_status()
        self.reset_dmg()
        self.reset_shield()
        self.reset_protector()
        self.reset_ult_used()
        self.reset_can_be_healed()
        self.reset_can_be_shielded()
        self.reset_dmg_reduction()
        self.editor = None
        
    ### Reset char ###
    def reset(self):
        self.reset_next_round()
        self.reset_health()
        self.reset_ult_CD()
        self.reset_ult_avail()
        self.reset_alive()

    ### Decrease ultCD by 1 every turn, value >= 0 ###
        
    def minus_CD(self):
        cd = self.ultCD
        cd -= 1
        cd = max(cd,0)
        if not cd: #Make ult available
            self.ultAvail = True
        self.ultCD = cd

    ##### COMBAT #####
    def attack(self,enemy,dmg=None,msg='',code=0):
        #Refer to master code cheatsheet
        #0 = default, 1 = exclude attk, 2 = exclude invuln....
        if self.asleep:
            #message indicating that player is asleep
            return msg + self.Messages['combat']['sleepAtt']%(self.get_idty())
        dmg = dmg if dmg else self.dmg
        return enemy.attacked(self,dmg,msg,code)

    def attacked(self,enemy,dmg,msg='',code=0):
        if self.invuln:
            #message indicating that player is invulnerable
            return msg + self.Messages['combat']['invuln']%(self.get_idty(),enemy.get_idty())

        elif self.is_protected() and self.protector != self:
            protector = self.protector
            #message that damage is taken by protector
            msg = msg + self.Messages['combat']['protect']%(enemy.get_idty(),protector.get_idty())
            return protector.attacked(enemy,dmg,msg,code)
        
        elif self.is_shielded():
            if dmg > self.shield.amt:
                msg +=  self.Messages['combat']['shieldBroken']%(self.get_idty(),enemy.get_idty())
                dmg = (1-self.dmgReduction)*(dmg-self.shield.amt)
                msg += self.drop_health(amt,enemy,msg)
                enemy.add_stats_dmg(dmg)
                self.reset_shield()
                #message that shield was broken, damage taken
                return msg
            self.shield.drop_shield_amt(dmg)
            enemy.add_stats_dmg(dmg)
            #message that shield remains intact
            return msg + self.Messages['combat']['shieldIntact']%(enemy.get_idty(),self.get_idty(),self.shield.amt)
        if self == enemy:
            #self-inflict msg
            msg += self.Messages['combat']['selfAtt']%(self.get_idty())
            return self.drop_health((1-self.dmgReduction)*dmg,enemy,msg)
        if code != 1:
            msg += self.Messages['combat']['hurt']%(enemy.get_idty(), self.get_idty())
        dmg = (1-self.dmgReduction)*dmg
        enemy.add_stats_dmg(dmg)
        return self.drop_health(dmg,enemy,msg)

    def ult(self):
        #return either a msg or nothing. No news is good news!
        if self.asleep:
            #insert asleep message
            return self.Messages['combat']['sleepUlt']%(self.agentName)
        else:
            self.ultUsed = True
            self.reset_ult_avail()
            self.reset_ult_CD()
            return None

##### STATS #####        
    def add_stats_dmg(self,amt):
        self.stats['dmg'] += amt

    def add_stats_heal(self,amt):
        self.stats['healAmt'] += amt

    def add_stats_killed(self,enemy):
        if enemy is self:
            return
        self.stats['pplKilled'][enemy.userID] = 1 #Value here doesnt matter

    def add_stats_healed(self,ally):
        if ally is self:
            return
        self.stats['pplHealed'][ally.userID] = 1 #Value here doesnt matter
