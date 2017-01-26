from Messages import Messages
    
#defining character class
class Shield(object):

#### Constructor #####
    def __init__(self,amt,invuln=False,healAmt=0):
        self.amt = amt #shield amt
        self.invuln = invuln #whether shield is invulnerable
        self.healAmt = healAmt #how much health restored to target (applied together with shield)

    def heal(self,person,target):
        if self.healAmt and target.canBeHealed:
            target.add_health(healAmt)
            return Messages['combat']['shieldHeal']%(target.get_idty(),target.health,person.get_idty())
        return Messages['combat']['failShieldHeal']%(person.get_idty(),target.get_idty())

    def drop_shield_amt(self,dmg):
        self.amt -= dmg
