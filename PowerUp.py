import numpy as np
import random

'''
Each survivor is given equal power, which is pooled together (self.amt)
So if more ppl consume the power up, there will be less power for each (to the point where it is harmful),
and vice versa.
'''

######################################
########### POWER-UP CLASS ###########
######################################

class PowerUp(object):
#### Constructor #####
    def __init__(self, name, ppl):
        self.name = name #Name of powerUp
        self.ppl = ppl #No. of survivors 
        self.power = False #Power up the power up!
        if ppl <= 4: #Calc optimal no. of ppl = 1/2 of survivors
            self.limit = int(np.floor(0.5*ppl))
        else:
            self.limit = int(np.ceil(0.5*ppl)) 
        #Total 'power' generated. Less survivors = more power for balancing. Special handling for just 2 survivors.
        #This power will be divided amongst those who choose to eat the power up
        if ppl == 2:
            self.amt = round(np.random.uniform(0.7,0.9),3) * 2
        elif ppl <= 7:
            self.amt = (round(np.random.uniform(0.6,0.65),3)) * ppl
        else:
            self.amt = (round(np.random.uniform(0.55,0.6),3)) * ppl
        
    def toggle_power(self): #For future use
        self.power = True

    def gen_rate(self,chosen):
        #Returns amount to be distributed to each individual
        #chosen is the list of ppl who chose to consume the power up
        #others refer to number of ppl who didnt consume the power up, ie. = survivors - chosen
        rate = len(chosen) #To save space. First store no. of ppl who consume power-up
        if not rate: #Nobody chose to eat power-up
            return 0

        rate -= self.limit #Calculate if more or less than half of survivors ate the power up
        #More means most likely helpful, less means harmful.
        rate = int(rate)

        #Special handling for 2 players
        if self.ppl == 2:
            rate = [0.5,0.5] #Make it a gamble for 2 player games
            self.amt = [2.4, 0.2]

        elif rate <= -2: #Few people eat power up, so more power amongst few
            rate = [0.98,0.02] #Most likely will turn out well, but allow small probability for adverse event
            self.amt = [min((self.amt / len(chosen)), 2.4), 0.85] #Adverse case isn't that adverse

        elif rate >= 2: #Too many people eat power up
            rate = [0.98,0.02]
            #Make good case not too 
            self.amt = [min((self.amt / len(chosen)), 2.4), 1.1] #Good case isn't that good
            
        #Boundary cases
        elif rate == -1: #Beneficial or rate == 1: 
            rate = [0.88,0.12] #Probability of adverse event is slightly higher
            self.amt = [max((self.amt / len(chosen)), 1.4), 0.8]
            #Lower cap for power-up, adverse cap is slightly worse

        elif rate == 1:
            rate = [0.88,0.12] #Probability of adverse event is slightly higher
            self.amt = [min((self.amt / len(chosen)), 2.1), 0.7]
            #Lower cap for power-up, adverse cap is slightly worse

        else: #Just nice half of ppl choose to eat power-up. Give flat rate.
            rate = [0.8,0.2]
            self.amt = [1.1,0.9]

        rate = np.random.choice(self.amt,p=rate)
        rate = round(rate,3)
        return rate


##########################
##### DMG MULTIPLIER #####
##########################
    
class DmgX(PowerUp):
    def __init__(self,Messages,ppl):        
        super().__init__('DmgX', ppl)

    
    def power_up(self,Messages,chosen):
        #chosen is the list of ppl who chose to consume the power up
        #others refer to number of ppl who didnt consume the power up, ie. = survivors - chosen
        self.amt = super().gen_rate(chosen)
        if not self.amt:
            return Messages['powerUp']['zero']
            
        elif self.amt >= 1:
            self.amt -= 0.9 # +0.1 rate bonus, then -1 because we calculate increase. Thus -0.9
            msg = self.power_agents(chosen)
            return Messages['powerUp']['DmgX']['good'].format(names=msg,percent=(self.amt*100))

        else:
            self.amt -= 1.1 # -0.1 rate penalty, then -1 because we calculate increase. Thus -1.1
            msg = self.power_agents(chosen)
            return Messages['powerUp']['DmgX']['bad'].format(names=msg,percent=(np.abs(self.amt*100)))
    
    def power_agents(self,chosen):
        msg = ''
        for agent in chosen:
            agent.add_dmg(round(self.amt*agent.baseDmg))
            msg += agent.get_idty() + ", "
        msg = msg[:-2] #Remove comma
        return msg


##########################
######## HP ADDER ########
##########################
        
class HP(PowerUp):
    def __init__(self):
        super().__init__('HP', 0.6, 3)
        self.msg = self.gen_hp() #Message to be verdict of whether the power-up is beneficial or harmful

    ##Choose to either add or remove health
    def gen_dmg(self):
        hp = 30 if self.power else 20
        self.hp = np.random.choice([1,-1],p=self.rate)*hp
        return self.Messages
    
    def use_power(self,agent):
        if self.hp > 0:
            agent.add_health(hp)
        else:
            agent.drop_health(hp)

###############################
######## LIFE OR DEATH ########
###############################

class LoD(PowerUp):
    def __init__(self):
        super().__init__('LoD', 0.45, 1)

    def use_power(self,agent):
        #Will either be restored to full health, or will die!
        choice = np.random.choice([0,1],p=self.rate)
        if choice:
            agent.reset_health()
        else:
            agent.die()
         

def generate_powerUp(Messages):
    return np.random.choice([DmgX(Messages),HP(Messages),LoD(Messages)],p=[0.65,0.3,0.05])
