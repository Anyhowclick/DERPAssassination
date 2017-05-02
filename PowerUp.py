import numpy as np
import random

######################################
########### POWER-UP CLASS ###########
######################################

class PowerUp(object):
#### Constructor #####
    def __init__(self, name, rate, limit):
        self.name = name #Name of powerUp
        self.rate = [rate,1-rate] #Rate of SUCCESS Eg. 0.6 = 60% good, 40% bad
        self.baseRate = rate #Just in case I decide to make the rate adjustable
        self.limit = limit #Max no. of ppl this power up can be applied to
        self.baseLimit = limit #Just in case I decide to make this attribute adjustable
        self.power = False #Power up the power up!

    def reset_limit(self):
        self.limit = self.baseLimit

    def reset_power(self):
        self.power = False
        
    def reset_rate(self):
        self.rate = self.baseRate

    def reset(self):
        self.reset_limit()
        self.reset_power()
        self.reset_rate()
        
    def toggle_power(self):
        self.power = True
        
###### Power Up Method ######
    def use_power(self,agent):
        raise NotImplementedError #To be implemented by each type of power-up


##########################
##### DMG MULTIPLIER #####
##########################
    
class DmgX(PowerUp):
    def __init__(self):
        super().__init__('DmgX', 0.6, 3)
        self.gen_dmg()
        
    #Randomly generate how much damage to add/remove
    def gen_dmg(self):
        if self.power: #If powerUp is powered up, increase stakes
            dmg = [round(np.random.uniform(2.2,3),1),0]
        else: #Leave as it is
            dmg = [round(np.random.uniform(1.5,2),1),round(np.random.uniform(0,0.5),1)]
        #Choose random float (to 1dp) with given rate and save value
        self.dmg = np.random.choice(dmg,p=self.rate)
        
    def use_power(self,agent):
        #Minus 1 because we are adding dmg (not multiplying)
        agent.add_dmg(round((self.dmg-1)*agent.baseDmg))


##########################
######## HP ADDER ########
##########################
        
class HP(PowerUp):
    def __init__(self):
        super().__init__('HP', 0.6, 3)

    def use_power(self,agent):
        if self.power: #If powerUp is powered up, increase stakes
            hp = 30
        else: #Leave as it is
            hp = 20

        #Choose to either add or remove health
        choice = np.random.choice([0,1],p=self.rate)
        if choice:
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
         

def generate_powerUp():
    return np.random.choice([DmgX(),HP(),LoD()],p=[0.65,0.3,0.05])
