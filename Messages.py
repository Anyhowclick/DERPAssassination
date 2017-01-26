Messages = {
    'about':
        "<b>About the game</b>\n"\
        "This game was inspired by Spyfall, Overwatch and Werewolf, combining elements from the 3. "\
        "It also references material from personal experiences over the years.\n\n"\
        "<b>About the developer</b>\n"\
        "You may contact me at @Anyhowclick, but kindly refrain from spamming, much appreciated!",

    'abilityUsed':
        "<b>Ability used!</b>",

    'abilityNotUsed':
        "<b>Ability not used!</b>",

    'acknowledgement':
        "Got it.",

    'agentDescription':
        {   #Offense class
            "Dracule":"<b>Name:</b> Dracule\n<b>Health:</b> 100\n<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Recovers a portion of his health when attacking. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Grim":"<b>Name:</b> Grim\n<b>Health:</b> 100\n<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Attacks up to 3 agents, dealing 30 damage per target. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Novah":"<b>Name:</b> Novah\n<b>Health:</b> 100\n<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Sacrifices some hp to deal extra damage. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Saitami":"<b>Name:</b> Saitami\n<b>Health:</b> 100\n<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Drops an agent's health to 1hp.\n"\
            "<b>Ability cooldown:</b> 4 turns",

            "Sonhae":"<b>Name:</b> Sonhae\n<b>Health:</b> 85\n<b>Damage:</b> 30\n"\
            "<b>Ability:</b> Throws C4 explosives at an opponent to deal 40 damage.\n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Taiji":"<b>Name:</b> Taiji\n<b>Health:</b> 100\n<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Deflects all attacks back to attackers, except for some abilities.\n"\
            "<b>Ability cooldown:</b> 3 turns",

            #Tank class
            "Aspida":"<b>Name:</b> Asipda\n<b>Health:</b> 130\n<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Provides a shield barrier (lasts 1 turn) to 1 agent. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Hamia":"<b>Name:</b> Hamia\n<b>Health:</b> 130\n<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Increases damage reduction of 1 agent. \n"\
            "<b>Ability cooldown:</b> 1 turn",

            "Harambe":"<b>Name:</b> Harambe\n<b>Health:</b> 150\n<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Bites the bullet for an agent! All damage meant for the agent will be directed"\
            "to Harambe instead. Furthermore, he recovers 25% of all damage taken this turn. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Impilo":"<b>Name:</b> Impilo\n<b>Health:</b> 130\n<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Recovers 20 hp or 25% of remaining health, whever is higher."\
            "In addition, he has increased damage reduction.\n"\
            "<b>Ability cooldown:</b> 4 turns",


            #Healer class
            "Elias":"<b>Name:</b> Elias\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that self-heal is only 50% effective, and healers can choose only to either damage "\
            "or heal agents, not both in the same turn.\n"\
            "<b>Ability:</b> Reveal which team an agent is from!\n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Grace":"<b>Name:</b> Grace\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that self-heal is only 50% effective, and healers can choose only to either damage "\
            "or heal agents, not both in the same turn.\n"\
            "<b>Ability:</b> Resurrects a dead agent with half of their base health. \n"\
            "<b>Ability cooldown:</b> 5 turns",

            "Prim":"<b>Name:</b> Prim\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that self-heal is only 50% effective, and healers can choose only to either damage "\
            "or heal agents, not both in the same turn.\n"\
            "<b>Ability:</b> Makes an agent's ability available for use for him/her next turn. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Ralpha":"<b>Name:</b> Ralpha\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that self-heal is only 50% effective, and healers can choose only to either damage "\
            "or heal agents, not both in the same turn.\n"\
            "<b>Ability:</b> Restores an agent to full health (including yourself, but less effective).\n"\
            "<b>Ability cooldown:</b> 4 turns",

            "Sanar":"<b>Name:</b> Sanar\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that self-heal is only 50% effective, and healers can choose only to either damage "\
            "or heal agents, not both, in the same turn.\n"\
            "<b>Ability:</b> Heals up to 3 agents for 20 hp each (50% effective on self still). \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Yunos":"<b>Name:</b> Yunos\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that self-heal is only 50% effective, and healers can choose only to either damage "\
            "or heal agents, not both in the same turn.\n"\
            "<b>Ability:</b> Provides energy shields for up to 3 agents. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            #Support class
            "Anna":"<b>Name:</b> Anna\n<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Powers up an agent (Target agent will have increased damage, heal amount (if applicable), "\
            "and abilities powered up (if possible), for 1 turn. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Jigglet":"<b>Name:</b> Jigglet\n<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Lulls an agent to sleep, rendering that agent useless for 1 turn. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Munie":"<b>Name:</b> Munie\n<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Causes an agent to be invulnerable to taking damage and negative effects for 1 turn.\n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Puppenspieler":"<b>Name:</b> Puppenspieler\n<b>Health:</b> 90\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Controls an agent for 1 turn. That agent's ability may be used as well (if available).\n"\
            "<b>Ability cooldown:</b> 4 turns",

            "Simo":"<b>Name:</b> Simo\n<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Fires a shield-piercing bullet, breaking the shield of an agent (and so deals extra damage). "\
            "If the agent is not shielded, then the bullet does slightly lower damage.\n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Wanda":"<b>Name:</b> Wanda\n<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Prevent an agent from being healed for 1 turn. In addition, if the agent is a healer, "\
            "he/she will be unable to heal others.\n"\
            "<b>Ability cooldown:</b> Depends on target chosen. 3 turns for non-healers, 4 for healers.",
        },

    'agentDescriptionFirstPerson':
        {   #Offense class
            "Dracule": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Recover a portion of your health when attacking. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Grim": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Attack up to 3 agents, dealing 30 damage per target. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Novah": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Sacrifice some of your health to deal extra damage. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Saitami": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Leave your target with 1hp remaining.\n"\
            "<b>Ability cooldown:</b> 4 turns",

            "Sonhae": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 85\n"\
            "<b>Damage:</b> 30\n"\
            "<b>Ability:</b> Throw C4 explosives at an opponent to deal 40 damage.\n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Taiji": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 25\n"\
            "<b>Ability:</b> Deflect all damage targeted at you back to attackers for 1 turn (excludes some abilities).\n"\
            "<b>Ability cooldown:</b> 3 turns",

            #Tank class
            "Aspida": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 130\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Provide a shield (lasting 1 turn) to 1 agent. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Hamia": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 130\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Increase damage reduction of 1 agent. \n"\
            "<b>Ability cooldown:</b> 1 turn",

            "Harambe": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 150\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Bite the bullet for an agent for 1 turn! All damage meant for the agent will be directed"\
            "to you instead. Furthermore, you will recover 25%% of all damage taken this turn. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Impilo": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 130\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Recover 20 hp or 20%% of remaining health, whichever is higher. You also have increased damage reduction for 1 turn. \n"\
            "<b>Ability cooldown:</b> 4 turns",


            #Healer class
            "Elias": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that healing yourself is an option, but is only 50%% effective. "\
            "Also, you can choose only to either damage or heal agents, "\
            "not both in the same turn.\n"\
            "<b>Ability:</b> Reveal which team an agent is from!\n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Grace": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that healing yourself is an option, but is only 50%% effective. "\
            "Also, you can choose only to either damage or heal agents, "\
            "not both in the same turn.\n"\
            "<b>Ability:</b> Resurrect a dead agent with half of their base health. \n"\
            "<b>Ability cooldown:</b> 5 turns",

            "Prim": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that healing yourself is an option, but is only 50%% effective. "\
            "Also, you can choose only to either damage or heal agents, "\
            "not both in the same turn.\n"\
            "<b>Ability:</b> Cause an agent's ability to be available for use for him/her next turn. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Ralpha": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that healing yourself is an option, but is only 50%% effective. "\
            "Also, you can choose only to either damage or heal agents, "\
            "not both in the same turn.\n"\
            "<b>Ability:</b> Restore an agent to full health (works on yourself too, but less effective).\n"\
            "<b>Ability cooldown:</b> 4 turns",

            "Sanar": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that healing yourself is an option, but is only 50%% effective. "\
            "Also, you can choose only to either damage or heal agents, "\
            "not both in the same turn.\n"\
            "<b>Ability:</b> Heal up to 3 agents, 20 hp for each agent (50%% effectiveness on healing yourself still applies). \n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Yunos": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 90\n"\
            "<b>Damage:</b> 17\n"\
            "<b>Heal Amount:</b> 10\n"\
            "Note that healing yourself is an option, but is only 50%% effective. "\
            "Also, you can choose only to either damage or heal agents, "\
            "not both in the same turn.\n"\
            "<b>Ability:</b> Give energy shields to a maximum of 3 agents. \n"\
            "<b>Ability cooldown:</b> 3 turns",

            #Support class
            "Anna": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Power up an agent (Target agent will have increased damage, heal amount (if applicable), "\
            "and abilities powered up (if possible), for 1 turn. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Jigglet": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Lull an agent to sleep, rendering that agent useless for 1 turn. \n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Munie": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Cause an agent to be invulnerable to taking damage and negative effects for 1 turn.\n"\
            "<b>Ability cooldown:</b> 3 turns",

            "Puppenspieler": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Control an agent for 1 turn. That agent's ability may be used as well (if available).\n"\
            "<b>Ability cooldown:</b> 4 turns",

            "Simo": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Fire a shield-piercing bullet, breaking the shield of an agent (and so deals extra damage). "\
            "If the agent is not shielded, then the bullet does slightly lower damage.\n"\
            "<b>Ability cooldown:</b> 2 turns",

            "Wanda": "You are %s! Your stats and ability are listed below: \n"\
            "<b>Health:</b> 100\n"\
            "<b>Damage:</b> 20\n"\
            "<b>Ability:</b> Prevent an agent from being healed for 1 turn. In addition, if the agent is a healer, "\
            "he/she will be unable to heal others.\n"\
            "<b>Ability cooldown:</b> Depends on target chosen. 3 turns for non-healers, 4 for healers.",
        },


    'agentNames':
        ["Anna","Aspida","Dracule","Elias","Grim",
         "Harambe","Hamia","Impilo","Munie",
         "Novah","Prim","Ralpha","Saitami",
         "Sanar","Sonhae","Taiji","Wanda",
         ],

    'allotSuccess':
        "Roles and teams have been allocated! Who's who:\n",

    'attHealOption':
        {'att': "Attack \U0001F5E1",
         'heal': "Heal \U0001F489",
         'ult': "Ability \U00002728",
         },

    'choiceAccept':
        "Choice accepted!: <b>%s</b>",

    'combat':
        {
            'deflect': "%s deflects the attack from %s!\n",
            'die': "<b>%s has been assassinated</b> \U00002620!!\n",
            'failHeal': "%s failed to heal %s! \U0001F61E\n",
            'failHealSelf': "%s tried to recover health, but failed! \U0001F61E\n",
            'failShield': "%s could not shield %s!\n",
            'hpLeft': "%s has %d hp left!\n",
            'heal': "%s has %d hp after healing from \U00002764 %s!\n",
            'hurt': "%s damages \U0001F52A %s!\n",
            'intro': "<b>\U00002694 COMBAT \U00002694</b>\n",
            'invuln': "%s was attacked, but is invulnerable!\n",
            'KO': "<b>You have been assassinated \U0001F480!!</b>",
            'protect': "%s's attack diverts to %s!\n",
            'res': "You have been <b>raised from the dead \U0001F3FB!</b> Get back into the fight \U0001F3FB!!",
            'recover': "%s recovers %d hp!\n",
            'selfAtt': "%s self-inflicts damage! \U0001F635\n",
            'selfHeal': "%s now has %d hp after self-healing! \U0001F36C\n",
            'sleepAtt': "%s wanted to attack but is asleep!\n",
            'sleepUlt': "%s wanted to use his/her ability but is asleep!\n",
            'shieldBroken': "%s's shield was broken by %s and takes damage!\n",
            'shieldIntact': "%s damaged %s's shield, leaving it with %d energy \U000026A1 remaining!\n",
            'shieldFailHeal': " %s's shield failed to heal %s!\n",
            'shieldHeal': " %s now has %d hp after being healed by %s's shield!\n",
            'teamDERP': 'on <b>team DERP \U0001F530</b>',
            'teamPYRO': 'on <b>team PYRO \U0001F525</b>',
            'teamPYROVIP': 'a \U0001F31F <b>VIP</b> on <b>team PYRO \U0001F525</b>',
            'ult':
                {
                    'Anna': "%s has been made stronger by %s this turn!\n",
                    'AnnaSelf': "%s is stronger this turn!\n",
                    'Aspida': "%s gave %s with a shield of <b>%d</b> energy! \U000026A1\n",
                    'AspidaSelf': "%s shielded herself with a shield of <b>%d</b> energy! \U000026A1\n",
                    'Dracule': "%s's attack, if successful, recovers a portion of his health this turn!\n",
                    'Elias': "%s knows which team %s is on! \U0001F60F\n",
                    'EliasSelf': "%s revealed his own identity to himself, which is sort of pointless, but well...\n",
                    'EliasPrivate': "%s is %s",
                    'EliasSelfPrivate': "You don't know which team you're on? \U0001F611 "\
                                        "Perhaps you're too lazy to scroll up. Oh well... you're %s",
                    'Grim': '%s fires his blasters at %s!\n',
                    'Harambe': "%s protects %s this turn! Also, he will recover 25%% of all damage dealt to him!\n",
                    'Hamia': "%s increased %s's damage reduction this turn!\n",
                    'Impilo': "%s has increased damage reduction and recovered %d health!\n",
                    'ImpiloFailHeal': "%s has increased damage reduction, but failed to recover health! \U0001F61E\n",
                    'Munie': '%s caused %s to be invulnerable this turn!\n',
                    'MunieSelf': "%s is invulnerable this turn!\n",
                    'NovahNOK': "%s tried to activate his ability but has insufficient health!\n",
                    'NovahOK': "%s sacrificed 5 hp to deal extra damage this turn!\n",
                    'Prim': "%s caused %s's ability to be ready for use next turn!\n",
                    'PrimSelf': "%s tried to use her ability on herself, but failed!\n",
                    'Ralpha': "%s restored %s back to full health! \U0001F48A\n ",
                    'RalphaSelf': "%s heals himself back to 80%% of his base health! \U0001F48A\n ",
                    'revealFail': "Sorry, %s is invulnerable! ¯\_(ツ)_/¯",
                    'Saitami': "%s got hit by %s's divinity bullet, and so is barely alive with 1 hp!\n",
                    'Sonhae': "%s threw C4 explosives at %s!\n",
                    'Taiji': "%s will deflect all incoming damage to his attackers this turn!\n",
                    'Wanda': "%s prevented %s from being healed \U0001F48A this turn!\n",
                    'WandaSelf': "For unknown reasons, %s prevented herself from being healed \U0001F48A this turn!\n",
                    'WandaHealer': "%s prevented %s from being healed \U0001F48A and from healing others \U00002695 this turn!\n",
                },
            'ultInvuln': "%s tried to use his/her ability on %s, but %s is invulnerable!\n",

        },

    'countdownNoRemind':
        "<b>%d</b> seconds left to join the game!",

    'countdownRemind':
        "<b>%d</b> seconds left to join the game! Make sure "\
        "that you have a private chat open with me (tap/click this: @DERPAssassinBot) before "\
        "using the /join@DERPAssassinBot command!",

    'countdownChoice':
        "<b>%d</b> seconds left for all surviving agents to execute their plans!",

    'countdownToPhase1':
        "Everyone now has <b>%d</b> seconds to discover who their allies are and formulate strategies!",

    'countdownToPhase2':
        "Surviving agents are given <b>%d</b> seconds to carry our their actions!",

    'donate':
        "Thank you for supporting the development of this game. You may "\
        "donate through paypal via this link: paypal.me/Anyhowclick \n"\
        "It's fine if you don't, just enjoy the game!",

    'existingGame':
        "A game is running at the moment!",

    'endGame':
        {'draw': "Everyone is dead, so the game <b>ENDS IN A DRAW!</b>",
         'rareDraw': "Somehow both teams have the same health, so the game <b>ENDS IN A DRAW!</b>",
         'DERP.KO': "Alas, the PYRO agents proved to be too hot \U0001F525 to handle! <b>TEAM PYRO \U0001F525 WINS!</b>",
         'DERPWin': "<b>TEAM DERP \U0001F530 WINS!</b>",
         'PYRO.KO': "The cool guys have chilled \U00002744 the evil-doers into oblivion! <b>TEAM DERP \U0001F530 WINS!</b>",
         'PYROVIP.KO': "All VIP targets were iced \U00002744! <b>TEAM DERP \U0001F530 WINS!</b>",
         'PYROWin': "<b>TEAM PYRO \U0001F525 WINS!</b>",
         'tooLong': "This game has gone long enough! Team with the most health wins!",
         'tooLongSummary': "Team DERP: <b>%d hp</b>\nTeam PYRO: <b>%d hp</b>\n",
        },

    'failStart':
        {'lackppl':"Can't start the game due to lack of players!",},

    'failTalk':
        "%s failed to start / join a game! Would you kindly start a private chat with me first? "\
        "Tap/click this: @DERPAssassinBot, then press /start in the private chat, <b>not in the group chat</b>",

    'findOutChar':
        "Which character would you like to know more about?",

    'future':
        "Refer to @DerpAssUpdates for server downtimes and upcoming features!",

        #"At the moment, I'm sticking with having VIPs on 1 team only, but I will not rule out the possibility "\
        #"of having both sides having VIPs, and the objectives of both teams would then be the same.\n"\
        #"More characters will be added in over time, meaning more players can join the game! I prevent "\
        #"repeat heroes because I want to avoid logic loops (Eg. 2 Taijis deflecting damage to each other), "\
        #"but likewise it's a consideration for the future.\n"\
        #"Apart from more heroes, there may be different modes (FFA, Rapid Fire "\
        #"(reduced ability cooldown to 1-2 turns etc.)\n"\
        #"I have 1 more major planned feature in mind, which I'll keep under wraps at the moment, but I "\
        #"think this game is decent enough as it is. What's most important is that this game remains "\
        #"simple,yet fun enough to play with friends.\n\n "\
        #"That's it for now, check back again once in a while for updates!",

    'gifs': #File_ids of gifs stored on telegram servers
        {'drawVidID': "BQADBQADGAADtFzTEYTmkivEF03PAg",
         'DERPVidID': "BQADBQADGgADtFzTEZqVI4tYFx3MAg",
         'PYROVidID': "BQADBQADGQADtFzTEZ5k3pNuPxYKAg",
         },
    'invalidCommand':
        "Sorry, I can't interpret the command you gave.",

    'invalidText':
        "Sorry, I don't understand what you said.",

    'isInGame':
        "You're already in a game, or in the midst of joining one!",

    'joinGame':
        {'Max':
             "<b>%s</b> has joined the game. Player limit reached! \n",
         'notMax':
             "<b>%s</b> has joined the game. There are currently <b>%d</b> players. "\
             "<b>%d</b> players minimum, <b>%d</b> maximum",
         },

    'joinToUser':
        "You have successfully joined the game!",

    'killGame':
        "Game has been killed!",

    'killGameAgents':
        "Sorry, there was a problem with the bot. The game has been terminated by a group admin.",

    'lonely':
        "Can't play this game by yourself! (well it could in the future, but anyway...) "\
        "Find some friends to play with!",

    'maintenance':
        {'OK': "Shutting down...",
         'shutdown': "Sorry, this bot is closing for maintenance. Refer to @DerpAssUpdates for "\
                     "the latest information!",
         },

    'newGame':
        "A new game has been started by %s! Use /join@DERPAssassinBot to join the game, and ensure "\
        "that you have started a private chat with me (click/tap: @DERPAssassinBot), then press /start in the private chat, "\
        "so I can interact with you throughout the game.\n\n"
        "<b>%d</b> players minimum, <b>%d</b> maximum",

    'newGameToUser':
        "You have successfully started a game!",

    'no':
        "No",

    'none':
        "I'm done choosing!",

    'notPrivateChat':
        "This command is only enabled in private chats.",

    'query':
        {'canUlt': "Your ability is available! Would you like to use it?",
         'doWhat': "What would you like to do this turn?",
         'doWhatNext': "What would you like to do next? \U0001F601",
         'attack': "Who would you like to attack?",
         'heal': "Who would you like to heal?",
         'select':
             {1: "Select your %dst target ",
              2: "Select your %dnd target ",
              3: "Select your %drd target ",
              4: "Select your %dth target ", #To take note that anything more should fall under this case, so set min(4,num) in code
              },
         'ult':
             {'Anna': "Choose someone to power up!",
              'Aspida': "Who would you like provide a shield to this turn?",
              'Elias': "Whose identity would you like to know?",
              'Grim': "to PEW! \U0001F52B",
              'Hamia': "Choose someone to increase their damage reduction. \U0001F590\U0001F3FE",
              'Harambe': "Who would you like to \U0001F6E1 protect?",
              'Munie': "Choose someone to be invulnerable.",
              'Prim': "Pick someone to enable his ability to be available next turn.",
              'Ralpha': "Who would you like to restore back to full health? \U0001F36D",
              'Sanar': "to heal! \U0001F496",
              'Saitami': "Who would you like to use your divinity bullet \U0001F52B on?",
              'Sonhae': "Who would you like to see explode \U0001F600?",
              'Wanda': "Pick someone to prevent him/her from being healed (and healing others).",
              },
         },

    'okStart':
        "Game is starting... Please wait while I assign roles, "\
        "teams and VIPs.",

    'privateChat':
        "This command is only enabled in group chats.",

    'rate':
        'You may leave a review for this bot <a href="https://telegram.me/storebot?start=derpassassinbot">here</a>! '\
        'Thank you for doing so! \U0001F60A ',

    'rules':
        "<b>TLDR version:</b> Team DERP tries to find and assassinate VIPs, team PYRO tries to defend them and assassinate team DERP.\n"\
        "<b>Rules</b>:\n\nPlayers are split into 2 teams: \U0001F530DERP and \U0001F525PYRO. "\
        "DERP's objective is to find and kill all VIPs \U0001F31F, while PYRO's objective is to "\
        "protect their VIPs and eliminate all DERP agents. "\
        "All agents are categorized into 4 classes: Offense, Tank, Healer and Support. "\
        "Each class has its strength (dealing most damage, or has damage reduction etc.), "\
        "and every agent has a unique ability. \n\n"\

        "The number of DERP agents and VIP agents <b>are equal</b>. Assignment of VIPs/DERP agents is as follows:\n"\
        "3-4 players: 1\n"\
        "5-7 players: 2\n"\
        "8-10 players: 3\n"\
        "11-13 players: 4\n"\
        "14-16 players: 5\n"\
        "17-19 players: 6\n"\
        "20-22 players: 7\n"\
        "23-25 players: 8\n"\
        "26-28 players: 9\n"\
        "29-32 players: 10\n"\
        "Each VIP will be made known to 1-2 other PYRO players, and <b>each DERP agent knows who other DERP agents are.</b> "\
        "So PYRO agents (and VIPs) have to figure out who to trust, while DERP agents try to blend in. This is where "\
        "deception can come into play.\n\n"\

        "Each round is split into 2 phases: 1) the action phase and 2) the discussion phase.\n"\
        "\n<b>Action phase</b>\nAll players are given 60 or 90 seconds (depending on no. of players alive) "\
        "to carry out their actions. Players can choose to attack \U0001F44A another player, "\
        "or use their ability \U0001F4AA if it is available. For players who fail to select any option "\
        "(for a variety of reasons), "\
        "their characters would auto-attack themselves (so that they eventually die). "\
        "The usage of abilities take precedence over normal attacks. "\
        "Except for certain abilities, everything is processed on a "\
        "first-send-first serve basis. It is therefore a case of fastest fingers first!\n"

        "\n<b>Discussion phase</b>\nA message collating all usage of abilities and attacks will "\
        "be sent to the group chat. Players are then given 90-150 seconds "\
        "to read the message, accuse and convince other agents of the team they belong to, and formulate "\
        "strategies for the next round. \n\n"

        "The game ends when either all DERP or PYRO agents are dead, or when all VIPs have been "\
        "assassinated. If it doesn't end in 10 rounds, all players will have 2x damage. The game will "\
        "automatically end after 25 rounds, where the team with the most health declared the winner. Since "\
        "each round lasts 150-210 seconds, a game is expected to take 15-30 mins, but can stretch to a maximum "\
        "of 87.5 mins.\n\n"\
        "<b>TLDR version:</b> Team DERP tries to find and assassinate VIPs, team PYRO tries to defend them and assassinate team DERP.",
    'spam':
        {'start': 'Spam detector initialised!',
         1: "I won't respond for 10 seconds because you have been "\
             "a little agressive with interacting with me. This is an anti-spam preventive measure. Sorry about that! \U0001F605",
         2: "I won't respond for 1 minute because you've again been a little too hyperactive for me. "\
            "Sorry about that, but I seek your understanding that this is an anti-spam measure, and I have a lot of other people to talk to as well! \U0001F604",
         3: "I won't respond for 15 minutes because of I've been overwhelmed by you. Sorry about that, but try to tone down a little yeah? \U0001F604",
         4: "Hey. You've been warned. I won't respond for 1 hour. Tone down or else... \U0001F621",
         5: "I'm done being Mr.NiceGuy. I won't reply to your commands for 1 day.",
         6: "Really? Haven't learnt your lesson eh? You will be ignored for 1 week.",
         7: "Congratulations on making it this far. I never thought anyone would ever reach this stage. You are the kind of person I'm trying to prevent. Goodbye for a long time!",
        },
    'start':
        "Hi there! Add me into group chats and use /newgame@DERPAssassinBot to start a new game with your friends! "\
        "Make sure that all players must first have a private chat with the bot first before joining, "\
        "so that I can PM classified information to each player. Use /rules to find out how this game is played."\
        "/agents will give more info about each agent's ability and stats. "\
        "/story gives the lore of the game. Have lots of fun!",

    'story':
        "Long ago, the world \U0001F30E	lived together in harmony. Then, everything changed "\
        "when the evil organisation known as \U0001F525PYRO attacked! They were hellbent "\
        "on seeing the world burn\U0001F525\U0001F525\U0001F525. Only the "\
        "Division for Enforcing Realistic Peace (D.E.R.P)\U0001F530 can stop them. "\
        "Thus, D.E.R.P agents have been sent to infiltrate "\
        "the secret base \U0001F3EF of PYRO and assassinate \U0001F3F9 its leaders. However, word has it "\
        "that some agents have defected to the fiery side. So, will PYRO prevail and "\
        "leave the world in ashes, or will D.E.R.P save the world from catastrophe?",

    'support':
        "If you have any feedback or suggestions / discovered bugs in the game / would like to join me "\
        "in further development (One man army at the moment, I don't mind extra hands, "\
        "but you won't get paid \U0001F61D), you may PM @Anyhowclick \U0001F603"\
        "You may refer to @DerpAssUpdates for server maintenance times and upcoming features as well!\n\n"\
        "Source code will be made available on GitHub soon \U0001F601!",

    'summary':
        {
            'agent': "%s\n",
            'agentStart': "%s: <b>%s</b>\n",
            'alive': "%s <b>(%d hp)</b>\n",
            'aliveStart': "<b>\U0001F60E Survivors \U0001F60E</b>\n",
            'deadDERP': "%s <b>(\U0001F530 DERP agent!)</b>\n",
            'deadPYRO': "%s <b>(\U0001F525 PYRO agent!)</b>\n",
            'deadPYROVIP': "%s <b>(\U0001F31F VIP!!)</b>\n",
            'DERPintro': "Here are your allies:\n",
            'endIntro': "Here's who belonged to each team:\n",
            'intro': "<b>\U0001F47C\U0001F3FE PLAYERS STATUSES \U0001F47C\U0001F3FE</b>\n\n",
            'teamDERP': "<b>TEAM DERP</b> \U0001F530\n",
            'teamPYRO': "\n<b>TEAM PYRO</b> \U0001F525\n",
            'deadStart': "\n<b>\U00002620 Assassinated \U00002620</b>\n",
            'VIP': "%s (\U0001F31F VIP)\n",
        },

    'teamDERP':
        "You are a DERP \U0001F530 agent! Identify and kill all VIPs!",

    'teamPYRO':
        "You are a PYRO \U0001F525 agent! Identify and protect all VIPs!",

    'timeUp':
        "Time is up!",

    'update':
        "To be updated!",

    'VIP':
        "%s (<b>%s</b>) is one of the VIPs (or the only one)!",

    'VIPself':
        "You are one of the \U0001F31F VIPs (or the only one), and thus, a PYRO \U0001F525 agent! "\
        "Find other PYRO agents and get them to protect you!",

    'yes':
        "Yes",
    }

