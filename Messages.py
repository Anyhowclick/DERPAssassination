import telepot
from collections import OrderedDict

ALL_LANGS = ['EN','IT','BR']#'IN',ZH']

LANGEMOTES = {
    'EN': '\U0001F1EC\U0001F1E7',
    'IT': '\U0001F1EE\U0001F1F9',
    'BR': '\U0001F1E7\U0001F1F7',
    #'ZH': '\U0001F1E8\U0001F1F3',
    #'IN': '\U0001F1EE\U0001F1E9',
    }

setLang = 'Choose your preferred language:'

EN = {
    'about':
        "<b>About the game</b>\n"\
        "This game was inspired by Spyfall, Overwatch and Werewolf.\n\n"\
        "<b>About the developer</b>\n"\
        "You may contact me at @Anyhowclick! I specially want to thank "\
        "the people listed below who helped me in their capacity!\n\n"\
        "<b>Translators</b>\n"\
        "Italian: @MatteoIlGrande\n"\
        "Português do Brasil: @Liozek, @Alchimicus",

    'abilityUsed':
        "<b>Ability used!</b>",

    'abilityNotUsed':
        "<b>Ability not used!</b>",

    'acknowledgement': "Ok.",

    'agentDesc': "You are <b>%s</b>!\n",
    
    'agentDescription':
            "<b>Name:</b> %s\n"\
            "<b>Class:</b> %s\n"\
            "<b>Health:</b> <code>%d</code>\n"\
            "<b>Damage:</b> <code>%d</code>\n"\
            "<b>Ability:</b> %s\n"\
            "<b>Ability cooldown:</b> %s",

    'agentDescriptionHealer':
            "<b>Name:</b> %s\n"\
            "<b>Class:</b> %s\n"\
            "<b>Health:</b> <code>%d</code>\n"\
            "<b>Damage:</b> <code>%d</code>\n"\
            "<b>Heal Amount:</b> <code>%d</code>\n"\
            "Note that self-heal is only 50%% effective, and healers can choose only to either damage "\
            "or heal agents, not both in the same turn.\n"\
            "<b>Ability:</b> %s\n"\
            "<b>Ability cooldown:</b> %s",

    'agents': OrderedDict([
        #For the agents button, and when allocated
        #Offense class
        #Format is agent: [name,class,hp,dmg,ultCD,desc,ultCD]
        ('#baa', ['Dracule','\U0001F981 Offense',100,25,'2 turns',
                  "Recover a portion of your health when attacking."]),

        ('#bab', ['Grim','\U0001F981 Offense',100,22,'3 turns',
                  "Attack up to 3 agents, dealing 25 damage per target."]),

        ('#bac', ['Jordan','\U0001F981 Offense',100,22,'5 turns',
                  "Combine your health with your target and split it equally!"]),

        ('#bad', ['Novah', '\U0001F981 Offense',100,22,'5 turns',
                  "Sacrifice some hp to deal extra damage."]),
    
        ('#bae', ['Saitami','\U0001F981 Offense',100,25,'4 turns',
                  "Leave your target with 1 hp remaining (fatal if powered up!)"]),
    
        ('#baf', ['Sonhae','\U0001F981 Offense',85,30,'3 turns',
                  "Throw C4 explosives at an opponent to deal great damage!"]),

        ('#bag', ['Taiji','\U0001F981 Offense',100,25,'3 turns',
                  "Deflect all damage targeted at you back to attackers for 1 turn (excludes some abilities)."]),

        #Tank class
        ('#bba', ['Aspida','\U0001F98D Tank',130,20,'3 turns',
                  "Provide a shield (lasting 1 turn) to 1 agent"]),

        ('#bbb', ['Hamia','\U0001F98D Tank',130,20,'2 turns',
                  "Increase damage reduction of 1 agent by 50%."]),

        ('#bbc', ['Harambe','\U0001F98D Tank',130,20,'3 turns',
                  "Bite the bullet for an agent for 1 turn! All damage meant for the agent will be directed"\
                  "to you instead. Furthermore, you will recover 25% of all damage taken this turn."]),

        ('#bbd', ['Impilo','\U0001F98D Tank',130,20,'4 turns',
                  "Recover 20 hp or 20% of remaining health, whichever is higher. "\
                  "You also have increased damage reduction for 1 turn.",]),
    
        #Healer class
        #Note: They have an additional attribute (healAmt), so....
        #Format is agent: [name,class,hp,dmg,heal,ultCD,desc,ultCD]
        ('#bca', ['Elias','\U0001F54A Healer',90,17,10,'2 turns',
                  "Reveal which team an agent is from!"]),

    #'grace': ['Grace','\U0001F54A Healer',90,17,10,7,
    #          "Resurrect a dead agent with half of their base health."],
        ('#bcb', ['Prim','\U0001F54A Healer',90,17,10,'3 turns',
                  "Cause an agent's ability to be available for use for him/her next turn."]),

        ('#bcc', ['Ralpha','\U0001F54A Healer',90,17,10,'4 turns',
                  "Heal an agent to 80% of his base health (70% if used on yourself)."]),

        ('#bcd', ['Sanar','\U0001F54A Healer',90,17,10,'3 turns',
                  "Heal up to 3 agents (50% effectiveness on healing yourself still applies)."]),

    #'yunos': ['Yunos','\U0001F54A Healer',90,17,10,3,
    #          "Give energy shields to a maximum of 3 agents."],
    
        #Support class
        ('#bda', ['Anna','\U0001F436 Support',100,20,'2 turns',
                  "Power up an agent (Target agent will have increased damage, heal amount (if applicable), "\
                  "and abilities powered up (if possible), for 1 turn."]),

        ('#bdb', ['Jigglet','\U0001F436 Support',100,20,'3 turns',
                  "Lull an agent to sleep, rendering that agent useless for 1 turn."]),

        ('#bdc', ['Munie','\U0001F436 Support',100,20,'3 turns',
                  "Cause an agent to be invulnerable to taking damage and negative effects for 1 turn."]),
    
    #'puppenspieler': ['Puppenspieler','\U0001F436 Support',100,20,4,
    #                  "Control an agent for 1 turn. That agent's ability may be used as well (if available)."],
    
    #'simo': ['Simo','\U0001F436 Support',100,20,2,
    #         "Fire a shield-piercing bullet, breaking the shield of an agent (and so deals extra damage). "\
    #         "If the agent is not shielded, then the bullet does slightly lower damage."],

    #Special case for Wanda, because her ult is variable
        ('#bdd', ['Wanda','\U0001F436 Support',100,20,'Depends on target chosen. 3 turns for non-healers, 4 for healers.',
                  "Prevent an agent from being healed for 1 turn. In addition, if the agent is a healer, "\
                  "he/she will be unable to heal others."]),
        ]),
    
    'allotSuccess':
        "Roles and teams have been allocated! Who's who:\n",

    'attHealOption':
        {'att': "Attack \U0001F5E1",
         'heal': "Heal \U0001F489",
         'ult': "Ability \U00002728",
         },

    'choiceAccept':
        "Choice accepted: <b>%s</b>",

    'combat':
        {
            'deflect': "%s deflects the attack from %s!\n",
            'die': "%s <b>has been assassinated</b> \U00002620!!\n",
            'failHeal': "%s failed to heal %s! \U0001F61E\n",
            'failHealSelf': "%s tried to self-\U0001F489, but failed! \U0001F61E\n",
            'failShield': "%s couldn't shield %s!\n",
            'heal': "%s has %d hp after \U0001F489 from %s!\n",
            'hurt': "%s \U0001F52A %s!\n",
            'intro': "<b>\U00002694 ROUND %d \U00002694</b>\n",
            'invuln': "%s was attacked by %s, but is invulnerable!\n",
            'KO': "<b>You have been assassinated \U0001F480!!</b>",
            'protect': "%s's attack diverts to %s!\n",
            'res': "You have been <b>raised from the dead \U0001F3FB!</b> Get back into the fight \U0001F3FB!!",
            'recover': "%s recovers %d hp!\n",
            'selfAtt': "%s self-inflicts damage! \U0001F635\n",
            'selfHeal': "%s now has %d hp after self-\U0001F489!\n",
            'sleepAtt': "%s is \U0001F634, and so failed to \U0001F52A!\n",
            'sleepUlt': "%s is \U0001F634 and thus couldn't use his/her ability!\n",
            'shieldBroken': "%s's \U0001F6E1 was broken by %s!\n",
            'shieldIntact': "%s damaged %s's shield (%d energy \U000026A1 left)!\n",
            'shieldFailHeal': " %s's shield failed to heal %s!\n",
            'shieldHeal': " %s now has %d hp after being healed by %s's shield!\n",
            'teamDERP': 'on <b>team DERP \U0001F530</b>',
            'teamPYRO': 'on <b>team PYRO \U0001F525</b>',
            'teamPYROVIP': 'a \U0001F31F <b>VIP</b> on <b>team PYRO \U0001F525</b>',
            'ult':
                {
                    'Anna': "%s has been made stronger by %s this turn!\n",
                    'AnnaSelf': "%s is stronger this turn!\n",
                    'Aspida': "%s \U0001F6E1 (<b>%d</b> energy \U000026A1) %s\n",
                    'AspidaSelf': "%s \U0001F6E1 herself (<b>%d</b> energy \U000026A1)\n",
                    'Dracule': "%s's attack, if successful, recovers health this turn!\n",
                    'Elias': "%s knows which team %s is on! \U0001F60F\n",
                    'EliasSelf': "%s revealed his own identity to himself, which is sort of pointless, but well...\n",
                    'EliasPrivate': "%s is %s",
                    'EliasSelfPrivate': "You don't know which team you're on? \U0001F611 "\
                                        "Perhaps you're too lazy to scroll up. Oh well... you're %s",
                    'Grim': '%s \U0001F52B at %s!\n',
                    'Harambe': "%s protects %s this turn! He also recovers 25%% of all damage dealt to him!\n",
                    'Hamia': "%s increased %s's damage reduction this turn!\n",
                    'Impilo': "%s has increased damage reduction and recovered %d health!\n",
                    'ImpiloFailHeal': "%s has increased damage reduction, but failed to recover health! \U0001F61E\n",
                    'Jigglet': "%s caused %s to \U0001F634!\n",
                    'JiggletSelf': "%s fell asleep U0001F634!\n",
                    'Jordan': "%s \U0001F494 split health with %s! Both agents now have %d hp!\n",
                    'JordanSelf': "%s's ability failed!\n",
                    'Munie': '%s caused %s to be invulnerable this turn!\n',
                    'MunieSelf': "%s is invulnerable this turn!\n",
                    'NovahNOK': "%s tried to activate his ability but has insufficient health!\n",
                    'NovahOK': "%s sacrificed 5 hp to deal extra damage!\n",
                    'Prim': "%s caused %s's ability to be usable next turn!\n",
                    'PrimSelf': "%s tried, but failed, to use her ability on herself!\n",
                    'Ralpha': "%s restored 80%% of %s's health! \U0001F48A\n",
                    'RalphaSelf': "%s restored 70%% of his own health! \U0001F48A\n",
                    'revealFail': "Sorry, %s is invulnerable! ¯\_(ツ)_/¯",
                    'Saitami': "%s got hit by %s's divinity bullet, and so has 1 hp left!\n",
                    'SaitamiPower': "%s's powered up, so his fatality bullet kills %s!\n",
                    'Sonhae': "%s threw C4 explosives at %s!\n",
                    'Taiji': "%s will deflect all incoming damage to his attackers this turn!\n",
                    'Wanda': "%s prevented %s from being healed \U0001F48A this turn!\n",
                    'WandaSelf': "For unknown reasons, %s prevented herself from being healed \U0001F48A this turn!\n",
                    'WandaHealer': "%s prevented %s from being healed \U0001F48A and from healing others \U00002695 this turn!\n",
                },
            
            'ultInvuln': "%s tried to use his/her ability on %s, but %s is invulnerable!\n",

        },
    'config':
        {'back': "\U0001F519",
         'done': "See you soon!",
         'exit': "Exit \U000023CF",
         'intro': "What would you like to change for group <b>%s</b>?",
         'lang':'\U0001F30D Language',
         },
    
    'countdownNoRemind': "<b>%d</b> seconds left to join the game!",

    'countdownRemind':
        "<b>%d</b> seconds left to join the game! Make sure "\
        "that you have a private chat open with me (tap/click: @DERPAssassinBot) before "\
        "using the /join@DERPAssassinBot command!",

    'countdownChoice':
        "<b>%d</b> seconds left for surviving agents to execute their plans!",

    'countdownToPhase1':
        "\n<b>%d</b> seconds left for discussion!",

    'countdownToPhase2':
        "Surviving agents are given <b>%d</b> seconds to carry out their actions!",

    'delay':
        "\nGame will start in 5s! Agents, prepare for battle!\n",

    'donate':
        "Thank you for supporting the development of this game. Below are the following ways you can donate.\n"\
        "1. Ethereum address: <code>0xb4c82ff1a2b63cd1585c7b849604ad40a6d3ab35</code> \n"\
        "2. Litecoin address: <code>LcpU4jwZN5oLsC3p9EPekkcxyRYJpiBFUw</code> \n"\
        "It's fine if you don't, just enjoy the game!",

    'existingGame':
        "A game is running at the moment!",

    'endGame':
        {'draw': "\nNeither side prevailed this time... the game <b>ENDS IN A DRAW!</b>",
         'rareDraw': "\nSomehow both teams have the same health, so the game <b>ENDS IN A DRAW!</b>",
         'DERP.KO': "\nAlas, the PYRO agents proved to be too hot \U0001F525 to handle! <b>TEAM PYRO \U0001F525 WINS!</b>",
         'DERPWin': "<b>TEAM DERP \U0001F530 WINS!</b>",
         'PYRO.KO': "\nThe cool guys have chilled \U00002744 the evil-doers into oblivion! <b>TEAM DERP \U0001F530 WINS!</b>",
         'PYROVIP.KO': "\nAll VIP targets were iced \U00002744! <b>TEAM DERP \U0001F530 WINS!</b>",
         'PYROWin': "<b>TEAM PYRO \U0001F525 WINS!</b>",
         'tooLong': "This game has gone long enough! Team with the most health wins!",
         'tooLongSummary': "Team DERP: <b>%d hp</b>\nTeam PYRO: <b>%d hp</b>\n",
        },

    'error': "Something went wrong. You may contact @Anyhowclick if the error persists.",
    
    'failStart':
        {'lackppl':"Not enough players, can't start the game!",},

    'failTalk':
        "Talk with me privately first, %s! Tap/click: @DERPAssassinBot",

    'findOutChar':
        "Choose your agent.\n"\
        "\U0001F981 Offense agents have higher damage.\n"\
        "\U0001F98D Tanks have higher health.\n"\
        "\U0001F54A Healers can heal others.\n"\
        "\U0001F436 Support agents' abilities aid teammates.\n",

    'gifs': #File_ids of gifs stored on telegram servers
        {'drawVidID': "BQADBQADGAADtFzTEYTmkivEF03PAg",
         'DERPVidID': "BQADBQADGgADtFzTEZqVI4tYFx3MAg",
         'PYROVidID': "BQADBQADGQADtFzTEZ5k3pNuPxYKAg",
         },

    'groups':
        "Here are groups you may be interested to join:\n\n",

    'groupsMemberCount':
        "<b>%s members</b>\n\n",

    'info':
        "What would you like to know?",

    'initialise':
        "Initialising...",

    'invalidCommand':
        "Invalid command.",

    'invalidText':
        "Sorry, I don't understand what you said.",

    'isInGame':
        "You're already in a game, or in the midst of joining one!",

    'joinGame':
        {'Max':
             "<b>%s</b> has joined the game. Player limit reached! \n",
         'notMax':
             "<b>%s</b> has joined the game. Currently <b>%d</b> players.\n"\
             "<b>%d</b> players minimum, <b>%d</b> maximum",
         },

    'joinToUser':
        "You have successfully joined the game!",

    'killGame':
        "Game has been killed!",

    'killGameAgents':
        "Sorry, there was a problem. The game has been terminated by a group admin.",

    'leaveGame': "<b>%s</b> left the game!\n",
    'leaveGame1': "The game stopped as <b>%s</b> left.\n",

    'lonely':
        "Find some friends to play with, by joining any of the groups found in the menu!",

    'maintenance':
        {'shutdown': "The bot is <b>closed for maintenance.</b> Refer to @DerpAssUpdates for "\
                     "the latest information!\n\n",
         'status': "Bot status: %s",
         },

    'menu':
        {'about':'\U00002139 About',
         'agents':'\U0001F63C Agents',
         'back': '\U0001F519',
         'donate':'\U0001F4B5 Donate',
         'global':'\U0001F30F Global',
         'groups':'\U0001F465 Groups',
         'info': '\U00002753 How to play',
         'lang':'\U0001F30D Language',
         'modes': '\U0001F3AE Game modes',
         'personal': '\U0001F464 Personal',
         'rate': '\U00002B50 Rate',
         'rules': '\U0001F4C3 Rules',
         'soon': 'Coming soon!',
         'stats': '\U0001F3C5 Stats',
         'support': '\U0001F6A8 Help',
         'upgrades': '\U0001F199 Upgrades',
         },
    
    'newGame':
        "\n%s started a new game! /join@DERPAssassinBot to join.\n"\
        "Talk to me first, if you haven't! Click/tap: @DERPAssassinBot.\n"\
        "<b>%d</b> players minimum, <b>%d</b> maximum\n",

    'newGameToUser':
        "You have successfully started a game!",

    'nextGameNotify':
        "You will be notified when a game starts in <b>%s</b>!",

    'nextGameNotifyNoTitle':
        "You will be notified when a game starts!",

    'nextGameNoUsername':
        '\nA new game has started in <b>%s</b>\n',

    'no':
        "No",

    'none':
        "I'm done choosing!",

    'notGroup':
        "This command is only enabled in group chats.",
    
    'notGroupAdmin':
        "Only group admins are enabled to run this command.",
    
    'notPrivateChat':
        "This command is only enabled in private chats.",

    'okStart':
        "Beginning assignment of roles and agents...",

    'powerUp':
        {   
            'eat': "\U0001F60B Eating",
            'no': "You have decided not to eat the power-up. \U0001F910",
            'noEat': "\U0001F910 Not eating",
            'intro': "<b>Power-Up Available!</b>\n",
            'yes': "You have decided to eat the power-up. \U0001F60B",
            'zero': "No one wanted the power up.\n",
            'DmgX':
                {'bad':
                    "{names} \U0001F5E1 \U0001F53D by <b>{percent:.2f}%</b>!",
                'desc':
                     "\U0001F347: \U0001F53C or \U0001F53D damage.\n"\
                     "Recommended: <b>{}</b> agents\n"\
                     "<b>{}</b> agents will be eating it.",
                 'good':
                     "{names} \U0001F5E1 \U0001F53C by <b>{percent:.2f}%</b>!",
                },
            
            'Health':
                {'bad':
                    "\U0001F53D <b>%d</b> \U00002764!",
                'desc':
                    "\U0001F34E: \U0001F53C or \U0001F53D hp.\n"\
                    "{} agents will be eating it.",
                 'good':
                     "\U0001F53C <b>%d</b> \U00002764!",
                },
            
            'LoD':
                "\U0001F351: Restores health to full \U0001F607, or brings death \U00002620.\n"\
                "<b>%s</b> \U0001F351's available. Who wants to eat it?\n\n",
        },

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
              'Jigglet': "Who do you want to \U0001F634?",
              'Jordan': "Who would you like to \U0001F494 split health with?",
              'Munie': "Choose someone to be invulnerable.",
              'Prim': "Pick someone to enable his ability to be available next turn.",
              'Ralpha': "Whose health would you like to restore? \U0001F36D",
              'Sanar': "to heal! \U0001F496",
              'Saitami': "Who would you like to use your divinity bullet \U0001F52B on?",
              'Sonhae': "Who would you like to see explode \U0001F600?",
              'Wanda': "Pick someone to prevent him/her from being healed (and healing others).",
              },
         },

    'rate':
        'You may leave a review for this bot <a href="https://telegram.me/storebot?start=derpassassinbot">here</a>! '\
        'Thank you for doing so! \U0001F60A ',      
    
    'rules':
        {'sent':"Check below!",
         'fileID':"AgADBQADxacxGxZ3-VSOUGZoMvVlvL8byjIABLilrrw2eJwN9L4DAAEC",
         },

    'spam':
        {1:"I won't respond for %.1f minutes (unless you're in a game). This is an anti-spam preventive measure. Sorry about that! \U0001F605",
         2:"\U0001F910",
         },

    'stats':
        {
            'des':
                "\nNo. of active games: <code>{}</code>\n"\
                "No. of active players: <code>{}</code>\n\n",
            
            'global':
                "Total no. of players: <code>{d[players]}</code>\n"\
                "Total no. of groups: <code>{d[groups]}</code>\n"\
                "Games played \U0001F579: <code>{p[0]}</code>\n"\
                "Games won as \U0001F530 DERP: <code>{d[derpWins]}</code> <code>({p[1]:.2f})%</code>\n"\
                "Draws: <code>{d[drawsNormal]}</code> <code>({p[2]:.2f})%</code>\n"\
                "Games won as \U0001F525 PYRO: <code>{d[pyroWins]}</code> <code>({p[3]:.2f})%</code>\n"\
                "Best agent \U0001F396: <b>{d[bestNormalAgent][name]}</b> <code>{d[bestNormalAgent][rate]:.3f}</code> wins per game\n"\
                "Best \U0001F525 PYRO agent: <b>{d[pyroNormalWins][name]}</b> <code>{d[pyroNormalWins][rate]}</code> wins\n"\
                "Best \U0001F530 DERP agent: <b>{d[derpNormalWins][name]}</b> <code>{d[derpNormalWins][rate]}</code> wins\n"\
                "Best survivor: <b>{d[normalSurvivor][name]}</b> <code>{d[normalSurvivor][rate]}%</code>\n"\
                "Highest damage dealer: <b>{d[mostDmgNormal][name]}</b> <code>{d[mostDmgNormal][rate]}</code> \U00002694 in a game\n"\
                "Best healing dealer:  <b>{d[mostHealAmt][name]}</b> <code>{d[mostHealAmt][rate]}</code> \U0001F489 in a game\n"\
                "Best assassin \U0001F575\U0001F3FD: <b>{d[mostPplKilled][name]}</b> <code>{d[mostPplKilled][rate]}</code> agents\n"\
                "Best medic \U0001F47C\U0001F3FB: <b>{d[mostPplHealed][name]}</b> <code>{d[mostPplHealed][rate]}</code> agents\n"\
                "Last updated: <code>{d[lastUpdated]} GMT</code>\n",
            
            'local':
                "Games played \U0001F579: <code>{d[normalGamesPlayed]}</code>\n"\
                "Games won as \U0001F530 DERP: <code>{d[derpNormalWins]}</code> <code>({p[0]:.2f})%</code>\n"\
                "Draws: <code>{d[drawsNormal]}</code> <code>({p[1]:.2f})%</code>\n"\
                "Games won as \U0001F525 PYRO: <code>{d[pyroNormalWins]}</code> <code>({p[2]:.2f})%</code>\n"\
                "Games survived: <code>{d[normalGamesSurvived]}</code> <code>({p[3]:.2f})%</code>\n"\
                "Total agents killed \U0001F480: <code>{d[mostPplKilled]}</code>\n"\
                "Total agents healed \U0001F47C\U0001F3FB: <code>{d[mostPplHealed]}</code>\n"\
                "Highest damage \U00002694: <code>{d[mostDmgNormal]}</code>\n"\
                "Highest heal amount \U0001F48A: <code>{d[mostHealAmt]}</code>\n",

            'normal':
                "Agents healed \U0001F47C\U0001F3FB: {tup[0]}\n"\
                "Agents killed \U0001F480: <code>{tup[1]}</code>\n"\
                "Healing \U0001F48A done: <code>{d[healAmt]}</code>\n"\
                "Damage \U00002694 done: <code>{d[dmg]}</code>",
            
            'query':"Which stats would you like to see?",
        },
    
    'start':
        "Hi there! Add me into group chats and use /normalgame@DERPAssassinBot to start a new game with your friends! "\
        "All players must first talk to me privately, so I can talk back to them!\n"\
        "Explore the menu below to learn more about the game, or join a group to quickly get started!",

    'support':
        "If you have any feedback or suggestions / discovered bugs in the game / would like to join me "\
        "in further development (I don't mind extra hands, "\
        "but you won't get paid \U0001F61D), you may leave your feedback <a href='https://t.me/joinchat/AAAAAD-uDcr_i1DMwwAybg'>in this support group</a> "
        "\U0001F603. You may also refer to @DerpAssUpdates for server maintenance times and upcoming features!\n\n"\
        "Here's the <a href='https://github.com/Anyhowclick/DERPAssassination'>source code</a> for this game! \U0001F601",

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
        "\nYou are a DERP \U0001F530 agent! Identify and kill all VIPs!",

    'teamPYRO':
        "\nYou are a PYRO \U0001F525 agent! Identify and protect all VIPs!",

    'timeUp':
        "Time is up!",

    'update':
        "To be updated!",

    'VIP':
        "\n\n%s (<b>%s</b>) is one of the VIPs (or the only one)!",

    'VIPself':
        "\n\nYou are one of the \U0001F31F <b>VIPs</b> (or the only one), and thus, a <b>PYRO \U0001F525 agent!</b> "\
        "Find other PYRO agents and get them to protect you!",

    'welcomeChoice':
        "English selected!",

    'yes':
        "Yes",
    }

IT = {
    'about':
        "<b>Riguardo il gioco</b>\n"\
        "Questo gioco è stato ispirato da Spyfall, Overwatch e Werewolf.\n\n"\
        "<b>Riguardo lo sviluppatore</b>\n"\
        "Puoi contattarmi su @Anyhowclick!\n"\
        "<b>Riguardo il traduttore</b>\n"\
        "Puoi contattarmi su @MatteoIlGrande!",

    'abilityUsed':
        "<b>Abilità usata!</b>",

    'abilityNotUsed':
        "<b>Abilità non usata!</b>",

    'acknowledgement': "Ok.",

    'agentDesc': "Tu sei <b>%s</b>!\n",
    
    'agentDescription':
            "<b>Nome:</b> %s\n"\
            "<b>Classe:</b> %s\n"\
            "<b>Vita:</b> <code>%d</code>\n"\
            "<b>Danno:</b> <code>%d</code>\n"\
            "<b>Abilità:</b> %s\n"\
            "<b>Cooldown Abilità:</b> %s",

    'agentDescriptionHealer':
            "<b>Nome:</b> %s\n"\
            "<b>Classe:</b> %s\n"\
            "<b>Vita:</b> <code>%d</code>\n"\
            "<b>Danno:</b> <code>%d</code>\n"\
            "<b>Quantità di Guarigione:</b> <code>%d</code>\n"\
            "Nota che curare sè stessi è solo efficace al 50%%,"\
            "e i curatori possono solo scegliere di curare o attaccare agenti, non entrambi nello stesso turno.\n"\
            "<b>Abilità:</b> %s\n"\
            "<b>Cooldown Abilità:</b> %s",

    'agents': OrderedDict([
        #For the agents button, and when allocated
        #Offense class
        #Format is agent: [name,class,hp,dmg,ultCD,desc,ultCD]
        ('#baa', ['Dracule','\U0001F981 Offensiva',100,25,'2 turni',
                  "Recupera una parte della tua salute mentre attacchi."]),

        ('#bab', ['Grim','\U0001F981 Offensiva',100,22,'3 turni',
                  "Attacca fino a 3 agenti contemporaneamente, causando 25 danni per bersaglio."]),

        ('#bac', ['Jordan','\U0001F981 Offensiva',100,22,'5 turni',
                  "Fondi la tua vita col bersaglio e dividetela equamente!"]),

        ('#bad', ['Novah', '\U0001F981 Offensiva',100,22,'5 turni',
                  "Sacrifica qualche hp per fare danno extra."]),
    
        ('#bae', ['Saitami','\U0001F981 Offensiva',100,25,'4 turni',
                  "Lascia il tuo bersaglio con 1hp rimanente (fatale se potenziata!)"]),
    
        ('#baf', ['Sonhae','\U0001F981 Offensiva',85,30,'3 turni',
                  "Lancia esplosivi C4 al tuo bersaglio per infliggere danni ingenti!"]),

        ('#bag', ['Taiji','\U0001F981 Offensiva',100,25,'3 turni',
                  "Devia tutti i danni diretti a te agli attaccanti per 1 turno (esclude alcune abilità)."]),

        #Tank class
        ('#bba', ['Aspida','\U0001F98D Difensiva',130,20,'3 turni',
                  "Provvede uno scudo (che dura 1 turno) a 1 agente"]),

        ('#bbb', ['Hamia','\U0001F98D Difensiva',130,20,'2 turni',
                  "Aumenta la riduzione dei danni di un agente del 50%"]),

        ('#bbc', ['Harambe','\U0001F98D Difensiva',130,20,'3 turni',
                  "Fai da scudo a un agente per 1 turno! Tutti i danni indirizzati all'agente verranno deviati a te."\
                  "Inoltre, recupererai 25% di tutti i danni presi in questo turno."]),

        ('#bbd', ['Impilo','\U0001F98D Difensiva',130,20,'4 turni',
                  "Recupera 20 hp oppure 20% della tua vita rimanente, qualunque sia maggiore. "\
                  "Hai la riduzione dei danni aumentata per 1 turno.",]),
    
        #Healer class
        #Note: They have an additional attribute (healAmt), so....
        #Format is agent: [name,class,hp,dmg,heal,ultCD,desc,ultCD]
        ('#bca', ['Elias','\U0001F54A Curatore',90,17,10,'2 turni',
                  "Rivela di che team è un agente!"]),

    #'grace': ['Grace','\U0001F54A Healer',90,17,10,7,
    #          "Resuscita un agente morto con metà della vita base."],
        ('#bcb', ['Prim','\U0001F54A Curatore',90,17,10,'3 turni',
                  "Causa a un'abilità di un agente di essere disponibile per lui/le nel prossimo turno."]),

        ('#bcc', ['Ralpha','\U0001F54A Curatore',90,17,10,'4 turni',
                  "Cura un agente fino all'80% della sua vita base (70% se usato su se stessi)"]),

        ('#bcd', ['Sanar','\U0001F54A Curatore',90,17,10,'3 turni',
                  "Cura fino a 3 agenti (sempre 50% di efficacia se usata su se stessi)."]),

    #'yunos': ['Yunos','\U0001F54A Curatore',90,17,10,'3 turni',
    #          "Distribuisce scudi di forza fino a un massimo di 3 agenti."],
    
        #Support class
        ('#bda', ['Anna','\U0001F436 Supporto',100,20,'2 turni',
                  "Potenzia un agente (L'agente bersagliato avrà danni aumentati, "\
                  "cure aumentate (se applicabile). e abilità potenziate (se possibile), per 1 turno."]),

        ('#bdb', ['Jigglet','\U0001F436 Supporto',100,20,'3 turni',
                  "Addormenta un agente, rendendolo inoffensivo per 1 turno."]),

        ('#bdc', ['Munie','\U0001F436 Supporto',100,20,'3 turni',
                  "Rende un'agente invulnerabile ai danni e effetti negativi per 1 turno."]),
    
    #'puppenspieler': ['Puppenspieler','\U0001F436 Supporto',100,20,4,
    #                  "Control an agent for 1 turn. That agent's ability may be used as well (if available)."],
    
    #'simo': ['Simo','\U0001F436 Supporto',100,20,2,
    #         "Fire a shield-piercing bullet, breaking the shield of an agent (and so deals extra damage). "\
    #         "If the agent is not shielded, then the bullet does slightly lower damage."],

    #Special case for Wanda, because her ult is variable
        ('#bdd', ['Wanda','\U0001F436 Supporto',100,20,'Depends on target chosen. 3 turni for non-healers, 4 for healers.',
                  "Previene un agente dal venir curato per 1 turno. Inoltre, se l'agente è un curatore, "\
                  "non sarà in grado di curare altri."]),
        ]),
    
    'allotSuccess':
        "I ruoli e i team sono stati distribuiti! Chi è chi:\n",

    'attHealOption':
        {'att': "Attacca \U0001F5E1",
         'heal': "Cura \U0001F489",
         'ult': "Abilità \U00002728",
         },

    'choiceAccept':
        "Scelta accettata: <b>%s</b>",

    'combat':
        {
            'deflect': "%s devia gli attacchi da %s!\n",
            'die': "%s <b>è stato assassinato</b> \U00002620!!\n",
            'failHeal': "%s ha fallito nel curare %s! \U0001F61E\n",
            'failHealSelf': "%s ha tentato di auto-\U0001F489, ma ha fallito! \U0001F61E\n",
            'failShield': "%s non ha potuto proteggere %s!\n",
            'heal': "%s ha %d hp dopo la cura da %s!\n",
            'hurt': "%s \U0001F52A %s!\n",
            'intro': "<b>\U00002694 ROUND %d \U00002694</b>\n",
            'invuln': "%s è stato attaccato da %s, ma è invulnerabile!\n",
            'KO': "<b>Sei stato assassinato \U0001F480!!</b>",
            'protect': "l'attacco di %s viene deviato a %s!\n",
            'res': "You have been <b>raised from the dead \U0001F3FB!</b> Get back into the fight \U0001F3FB!!",
            'recover': "%s recupera %d hp!\n",
            'selfAtt': "%s si auto-infligge danno! \U0001F635\n",
            'selfHeal': "%s ora ha %d hp dopo l'auto-\U0001F489!\n",
            'sleepAtt': "%s è \U0001F634, e quindi ha fallito a \U0001F52A!\n",
            'sleepUlt': "%s è \U0001F634 e quindi non ha potuto usare la sua abilità!\n",
            'shieldBroken': "lo \U0001F6E1 di %s è stato distrutto da %s!\n",
            'shieldIntact': "%s ha danneggiato lo scudo di %s (%d energia \U000026A1 rimanente)!",
            'shieldFailHeal': "lo scudo di %s ha fallito a curare %s!\n",
            'shieldHeal': "%s ha ora %d hp dopo esser stata curato dallo scudo di %s!\n",
            'teamDERP': 'nel <b>team DERP \U0001F530</b>',
            'teamPYRO': 'nel <b>team PYRO \U0001F525</b>',
            'teamPYROVIP': 'un \U0001F31F <b>VIP</b> nel <b>team PYRO \U0001F525</b>',
            'ult':
                {
                    'Anna': "%s è stato reso più forte da %s per questo turno!\n",
                    'AnnaSelf': "%s è più forte questo turno\n",
                    'Aspida': "%s \U0001F6E1 (<b>%d</b> energia \U000026A1) %s\n",
                    'AspidaSelf': "%s \U0001F6E1 se stesso (<b>%d</b> energia \U000026A1)\n",
                    'Dracule': "l'attacco di %s, se riuscito, gli recupera vita questo turno!\n",
                    'Elias': "%s conosce di che team è %s! \U0001F60F\n",
                    'EliasSelf': "%s ha rivelato la sua identità a se stesso, cosa alquanto inutile, però...\n",
                    'EliasPrivate': "%s è %s",
                    'EliasSelfPrivate': "Non ricordi di che team fai parte? \U0001F611 "\
                                        "Forse sei troppo pigro per scorrere su. Vabbè.. sei un %s ",
                    'Grim': '%s \U0001F52B a %s!\n',
                    'Harambe': "%s protegge %s questo turno! Inoltre, recupererà il 25%% di tutto il danno inflitto a lui!\n",
                    'Hamia': "%s ha aumentato la riduzione dei danni di %s per questo turno!\n",
                    'Impilo': "%s ha riduzione dei danni aumentata e ha recuperato %d punti vita!\n",
                    'ImpiloFailHeal': "%s ha riduzione dei danni aumentata, ma ha fallito a recuperare vita! \U0001F61E\n",
                    'Jigglet': "%s ha causato %s di \U0001F634!\n",
                    'JiggletSelf': "%s si è addormentato U0001F634!\n",
                    'Jordan': "%s \U0001F494 si è diviso la vita con %s! Entrambi gli agenti hanno %d punti vita, ora!\n",
                    'JordanSelf': "l'abilità di %s è fallita!\n",
                    'Munie': '%s ha reso %s invulnerabile questo turno!\n',
                    'MunieSelf': "%s è invulnerabile questo turno!\n",
                    'NovahNOK': "%s ha provato ad attivare la sua abilità ma ha vita insufficiente!\n",
                    'NovahOK': "%s ha sacrificato 5 punti vita per infliggere danni extra questo turno!\n",
                    'Prim': "%s ha reso l'abilità di %s disponibile per il prossimo turno!\n",
                    'PrimSelf': "%s ha provato, ma ha fallito, nell'usare l'abilità su se stesso!\n",
                    'Ralpha': "%s ha recuperato 80%% della vita di %s! \U0001F48A\n",
                    'RalphaSelf': "%s ha recuperato il 70%% della propria vita \U0001F48A\n",
                    'revealFail': "Spiacente, %s è invulnerabile! ¯\_(ツ)_/¯",
                    'Saitami': "%s è stato colpito dal proiettile divino di %s, e ha quindi solo 1hp rimanente!\n",
                    'SaitamiPower': "%s è stato potenziato, e quindi il suo proiettile fatale uccide %s!\n",
                    'Sonhae': "%s ha tirato gli esplosivi C4 ad %s!\n",
                    'Taiji': "%s devierà tutti i danni in arrivo verso i suoi attaccanti questo turno!\n",
                    'Wanda': "%s ha impedito a %s di curarsi \U0001F48A questo turno!\n",
                    'WandaSelf': "Per motivi oscuri e sconosciuti, %s ha impedito a se stesso di curarsi \U0001F48A questo turno!\n",
                    'WandaHealer': "%s ha impedito a %s dal curarsi \U0001F48A e di curare altri \U00002695 questo turno!\n",
                },
            
            'ultInvuln': "%s ha provato ad usare la sua abilità su %s, ma %s è invulnerabile!\n",

        },
    'config':
        {'back': "\U0001F519",
         'done': "Ci vediamo presto!",
         'exit': "Esci \U000023CF",
         'intro': "Cosa vorresti cambiare per il gruppo <b>%s</b>?",
         'lang':'\U0001F30D Lingua',
         },
    
    'countdownNoRemind': "<b>%d</b> secondi rimasti per entrare in partita!",

    'countdownRemind':
        "<b>%d</b> secondi rimanenti per entrare in partita! Accertati che "\
        "hai avuto una chat privata aperta con me (clicca: @DERPAssassinBot) prima "\
        "di usare il comando /join@DERPAssassinBot!",

    'countdownChoice':
        "<b>%d</b> secondi rimanenti per gli agenti sopravvissuti per eseguire i loro piani!",

    'countdownToPhase1':
        "\n<b>%d</b> secondi rimanenti per discutere!",

    'countdownToPhase2':
        "Agli agenti sopravvissuti vengono dati <b>%d</b> secondi per svolgere le loro azioni!",

    'delay':
        "\nLa partita inizierà fra 5 secondi! Agenti, preparatevi per la battaglia!\n",

    'donate':
        "Ti ringrazio per sostenere lo sviluppo di questo gioco. Qui sotto ci sono i modi in cui puoi donare. \n"\
        "1. Indirizzo Ethereum: <code>0xb4c82ff1a2b63cd1585c7b849604ad40a6d3ab35</code> \n"\
        "2. Indirizzo Litecoin: <code>LcpU4jwZN5oLsC3p9EPekkcxyRYJpiBFUw</code> \n"\
        "Va bene se non vuoi, basta che ti diverta!",

    'existingGame':
        "Una partita è già in corso al momento!",

    'endGame':
        {'draw': "\nNessuna squadra ha prevalso questa partita... la partita <b>FINISCE IN PARITÀ!</b>",
         'rareDraw': "\nIn qualche modo entrambi i team hanno la stessa vita, e quindi la partita <b>FINISCE IN PARITÀ!</b>",
         'DERP.KO': "\nAhimè, gli agenti PYRO si sono dimostrati troppo caldi \U0001F525 da gestire! <b>IL TEAM PYRO \U0001F525 VINCE!</b>",
         'DERPWin': "<b>IL TEAM DERP \U0001F530 VINCE!</b>",
         'PYRO.KO': "\nI ragazzi freddi hanno rinfrescato \U00002744 i cattivi fino all'oblio! <b>IL TEAM DERP \U0001F530 VINCE!</b>",
         'PYROVIP.KO': "\nTutti i target VIP sono stati freddati \U00002744! <b>IL TEAM DERP \U0001F530 VINCE!</b>",
         'PYROWin': "<b>IL TEAM PYRO \U0001F525 VINCE!</b>",
         'tooLong': "Questa partita è andata avanti abbastanza a lungo! Il team con più vita ha vinto!",
         'tooLongSummary': "Team DERP: <b>%d hp</b>\nTeam PYRO: <b>%d hp</b>\n",
        },

    'error': "Qualcosa è andato storto. Puoi contattare @Anyhowclick se l'errore persiste.",
    
    'failStart':
        {'lackppl':"Non ci sono abbastanza giocatori, non posso iniziare la partita!",},

    'failTalk':
        "Contattami prima in privato, %s! Clicca: @DERPAssassinBot",

    'findOutChar':
        "Scegli il tuo agente.\n"\
        "\U0001F981 Gli agenti Offensivi hanno più danno d'attacco.\n"\
        "\U0001F98D Quelli Difensivi hanno più vita.\n"\
        "\U0001F54A I Curatori possono curare gli altri (o se stessi).\n"\
        "\U0001F436 Gli agenti di Supporto hanno abilità che aiutano i compagni di squadra.\n",

    'gifs': #File_ids of gifs stored on telegram servers
        {'drawVidID': "BQADBQADGAADtFzTEYTmkivEF03PAg",
         'DERPVidID': "BQADBQADGgADtFzTEZqVI4tYFx3MAg",
         'PYROVidID': "BQADBQADGQADtFzTEZ5k3pNuPxYKAg",
         },

    'groups':
        "Ecco i gruppi nel quale potresti essere interessato a unirti:\n\n",

    'groupsMemberCount':
        "<b>%s membri</b>\n\n",

    'info':
        "Cosa vorresti conoscere?",

    'initialise':
        "Initialising...",

    'invalidCommand':
        "Comando non valido.",

    'invalidText':
        "Scusami, non ho capito cosa hai detto.",

    'isInGame':
        "Sei già in partita, o in mezzo a una partita che sta per iniziare!",

    'joinGame':
        {'Max':
             "<b>%s</b> è entrato in partita. Limite di giocatori raggiunto! \n",
         'notMax':
             "<b>%s</b> è entrato in partita. Attualmente <b>%d</b> giocatori in partita.\n"\
             "<b>%d</b> giocatori minimo, <b>%d</b> massimo",
         },

    'joinToUser':
        "Ti sei unito con successo!",

    'killGame':
        "La partita è stata arrestata!",

    'killGameAgents':
        "Scusami, c'è stato un problema. La partita è stata interrotta da un admin del gruppo.",

    'leaveGame': "<b>%s</b> è uscito dalla partita!\n",
    'leaveGame1': "La partita si è interrotta siccome sono rimasti solo <b>%s</b> giocatori.\n",

    'lonely':
        "Trova qualche amico con cui giocare, unendoti a qualsiasi dei gruppi che puoi trovare nel menu!",

    'maintenance':
        {'shutdown': "Il bot è <b>fermo per manutenzione.</b> Controlla su @DerpAssUpdates "\
                     "per aggiornamenti!\n\n",
         'status': "Bot status: %s",
         },

    'menu':
        {'about':'\U00002139 Informazioni',
         'agents':'\U0001F63C Agenti',
         'back': '\U0001F519',
         'donate':'\U0001F4B5 Dona',
         'global':'\U0001F30F Globali',
         'groups':'\U0001F465 Gruppi',
         'info': '\U00002753 Come giocare',
         'lang':'\U0001F30D Lingua',
         'modes': '\U0001F3AE Modalità di gioco',
         'personal': '\U0001F464 Personali',
         'rate': '\U00002B50 Vota',
         'rules': '\U0001F4C3 Regole',
         'soon': 'Prossimamente!',
         'stats': '\U0001F3C5 Statistiche',
         'support': '\U0001F6A8 Aiuto',
         'upgrades': '\U0001F199 Potenziamenti',
         },
    
    'newGame':
        "\n%s ha iniziato una nuova partita! /join@DERPAssassinBot per unirti.\n"\
        "Avviami prima in privato, se non l'hai fatto! Clicca: @DERPAssassinBot.\n"\
        "<b>%d</b> giocatori minimo, <b>%d</b> massimo\n",

    'newGameToUser':
        "Hai iniziato una nuova partita con successo!",

    'nextGameNotify':
        "Verrai avvisato quando una partita inizierà in <b>%s</b>!",

    'nextGameNotifyNoTitle':
        "Verrai notificato quando una partita inizierà!",

    'nextGameNoUsername':
        '\nUna nuova partita è stata iniziata in <b>%s</b>\n',

    'no':
        "No",

    'none':
        "Ho finito di scegliere!",

    'notGroup':
        "Questo comando è abilitato solo per le chat di gruppo.",
    
    'notGroupAdmin':
        "Solo gli admin del gruppo sono autorizzati a usare questo comando.",
    
    'notPrivateChat':
        "Questo comando è abilitato solo per le chat private.",

    'okStart':
        "Iniziando l'assegnazione dei ruoli e agenti...",

    'powerUp':
        {   
            'eat': "\U0001F60B Mangia",
            'no': "Hai deciso di non mangiare il potenziamento. \U0001F910",
            'noEat': "\U0001F910 Non mangiare",
            'intro': "<b>Potenziamento Disponibile!</b>\n",
            'yes': "Hai deciso di mangiare il potenziamento. \U0001F60B",
            'zero': "Nessuno ha voluto il potenziamento.\n",
            'DmgX':
                {'bad':
                    "{names} \U0001F5E1 \U0001F53D del <b>{percent:.2f}%</b>!",
                'desc':
                     "\U0001F347: \U0001F53C or \U0001F53D danno.\n"\
                     "Consigliato: <b>{}</b> agenti\n"\
                     "<b>{}</b> agenti lo mangeranno.",
                 'good':
                     "{names} \U0001F5E1 \U0001F53C del <b>{percent:.2f}%</b>!",
                },
            
            'Health':
                {'bad':
                    "\U0001F53D <b>%d</b> \U00002764!",
                'desc':
                    "\U0001F34E: \U0001F53C or \U0001F53D hp.\n"\
                    "<b>{}</b> agenti lo mangeranno.",
                 'good':
                     "\U0001F53C <b>%d</b> \U00002764!",
                },
            
            'LoD':
                "\U0001F351: Restores health to full \U0001F607, or brings death \U00002620.\n"\
                "<b>%s</b> \U0001F351's available. Who wants to eat it?\n\n",
        },

    'query':
        {'canUlt': "La tua abilità è disponibile! Vorresti usarla?",
         'doWhat': "Cosa vorresti fare questo turno?",
         'doWhatNext': "Cos'altro vorresti fare? \U0001F601",
         'attack': "Chi vorresti attaccare?",
         'heal': "Chi vorresti curare?",
         'select':
             {1: "Seleziona il tuo %dst bersaglio ",
              2: "Seleziona il tuo %dnd bersaglio ",
              3: "Seleziona il tuo %drd bersaglio ",
              4: "Seleziona il tuo %dth bersaglio ", #To take note that anything more should fall under this case, so set min(4,num) in code
              },
         'ult':
             {'Anna': "Seleziona qualcuno da potenziare!",
              'Aspida': "A chi vorresti dotare di uno scudo per questo turno?",
              'Elias': "A chi vorresti conoscere l'identità?",
              'Grim': "a cui SPARARE! \U0001F52B",
              'Hamia': "Scegli qualcuno a cui aumentare la riduzione dei danni. \U0001F590\U0001F3FE",
              'Harambe': "Chi vorresti \U0001F6E1 proteggere?",
              'Jigglet': "Chi vorresti \U0001F634?",
              'Jordan': "Con chi vorresti \U0001F494 dividere la vita?",
              'Munie': "Scegli qualcuno da rendere invulnerabile.",
              'Prim': "Scegli qualcuno a cui rendere l'abilità disponibile nel prossimo turno.",
              'Ralpha': "A chi vorresti rigenerare la vita? \U0001F36D",
              'Sanar': "da curare! \U0001F496",
              'Saitami': "A chi vorresti sparare col tuo proiettile divino \U0001F52B?",
              'Sonhae': "Chi vorresti far esplodere \U0001F600?",
              'Wanda': "Scegli qualcuno per prevenire che venga curato (e curi altri).",
              },
         },

    'rate':
        'Puoi lasciare una recensione per questo bot <a href="https://telegram.me/storebot?start=derpassassinbot">qui</a>! '\
        'E grazie mille per il gesto! \U0001F60A ',      
    
    'rules':
        {'sent':"Controlla sotto!",
         'fileID':"AgADBQADxacxGxZ3-VSOUGZoMvVlvL8byjIABLilrrw2eJwN9L4DAAEC",
         },

    'spam':
        {1:"Non risponderò per %.1f minuti (a meno che tu sia in una partita). Questa è una misura preventiva anti-spam. Ci scusiamo per l'eventuale disagio! \U0001F605",
         2:"\U0001F910",
         },

    'stats':
        {
            'des':
                "\nNo. of active games: <code>{}</code>\n"\
                "No. of active players: <code>{}</code>\n\n",
            
            'global':
                "Numero totale di giocatori: <code>{d[players]}</code>\n"\
                "Numero totale di gruppi: <code>{d[groups]}</code>\n"\
                "Partite giocate \U0001F579: <code>{p[0]}</code>\n"\
                "Partite vinte da \U0001F530 DERP: <code>{d[derpWins]}</code> <code>({p[1]:.2f})%</code>\n"\
                "Disegna: <code>{d[drawsNormal]}</code> <code>({p[2]:.2f})%</code>\n"\
                "Partite vinte da \U0001F525 PYRO: <code>{d[pyroWins]}</code> <code>({p[3]:.2f})%</code>\n"\
                "Migliore agenti \U0001F396: <b>{d[bestNormalAgent][name]}</b> <code>{d[bestNormalAgent][rate]:.3f}</code> vittorie per partita\n"\
                "Migliore agente \U0001F525 PYRO: <b>{d[pyroNormalWins][name]}</b> <code>{d[pyroNormalWins][rate]}</code> vittorie\n"\
                "Migliore agente \U0001F530 DERP: <b>{d[derpNormalWins][name]}</b> <code>{d[derpNormalWins][rate]}</code> vittorie\n"\
                "Miglior superstite: <b>{d[normalSurvivor][name]}</b> <code>{d[normalSurvivor][rate]}%</code>\n"\
                "Migliore attaccante: <b>{d[mostDmgNormal][name]}</b> <code>{d[mostDmgNormal][rate]}</code> \U00002694 in una partita\n"\
                "Migliore curatore: <b>{d[mostHealAmt][name]}</b> <code>{d[mostHealAmt][rate]}</code> \U0001F489 in una partita\n"\
                "Migliore assassino \U0001F575\U0001F3FD: <b>{d[mostPplKilled][name]}</b> <code>{d[mostPplKilled][rate]}</code> agenti\n"\
                "Best medico \U0001F47C\U0001F3FB: <b>{d[mostPplHealed][name]}</b> <code>{d[mostPplHealed][rate]}</code> agenti\n"\
                "Ultimo aggiornamento: <code>{d[lastUpdated]} GMT</code>\n",
            
            'local':
                "Partite giocate \U0001F579: <code>{d[normalGamesPlayed]}</code>\n"\
                "Partite vinte da \U0001F530 DERP: <code>{d[derpNormalWins]}</code> <code>({p[0]:.2f})%</code>\n"\
                "Disegna: <code>{d[drawsNormal]}</code> <code>({p[1]:.2f})%</code>\n"\
                "Partite vinte da \U0001F525 PYRO: <code>{d[pyroNormalWins]}</code> <code>({p[2]:.2f})%</code>\n"\
                "Partite sopravvissute: <code>{d[normalGamesSurvived]}</code> <code>({p[3]:.2f})%</code>\n"\
                "Totale agenti uccisi \U0001F480: <code>{d[mostPplKilled]}</code>\n"\
                "Totale agenti curati \U0001F47C\U0001F3FB: <code>{d[mostPplHealed]}</code>\n"\
                "Danno maggiore \U00002694: <code>{d[mostDmgNormal]}</code>\n"\
                "Cura maggiore \U0001F48A: <code>{d[mostHealAmt]}</code>\n",

            'normal':
                "Agenti curati \U0001F47C\U0001F3FB: {tup[0]}\n"\
                "Agenti uccisi \U0001F480: <code>{tup[1]}</code>\n"\
                "Cura \U0001F48A: <code>{d[healAmt]}</code>\n"\
                "Danno \U00002694: <code>{d[dmg]}</code>",
            
            'query':"Quali statistiche vorresti vedere?",
        },
    
    'start':
        "Ciao! Aggiungimi in una chat di gruppo e usa /normalgame@DERPAssassinBot per iniziare una nuova partita con i tuoi amici! "\
        "Tutti i giocatori devono prima parlarmi in privato, così sarò in grado di scrivergli quando necessario!\n"\
        "Esplora il menù sottostante per sapere di più riguardo il gioco, o entra in un gruppo per iniziare rapidamente!",

    'support':
        "Se hai qualche parere o suggerimenti / scoperto bug nel gioco / vorresti aiutarmi nella programmazione "\
        "in further development (ma non verrai pagato \U0001F61D), puoi scrivermi su @Anyhowclick \U0001F603.\n"\
        "Puoi controllare @DerpAssUpdates per le manutenzioni programmate e le prossime funzionalità in arrivo!\n\n"\
        "<a href='https://github.com/Anyhowclick/DERPAssassination'>Ecco il codice sorgente del gioco!</a> \U0001F601",

    'summary':
        {
            'agent': "%s\n",
            'agentStart': "%s: <b>%s</b>\n",
            'alive': "%s <b>(%d hp)</b>\n",
            'aliveStart': "<b>\U0001F60E Sopravvissuti \U0001F60E</b>\n",
            'deadDERP': "%s <b>(\U0001F530 Agente DERP!)</b>\n",
            'deadPYRO': "%s <b>(\U0001F525 Agente PYRO!)</b>\n",
            'deadPYROVIP': "%s <b>(\U0001F31F VIP!!)</b>\n",
            'DERPintro': "Ecco i tuoi alleati:\n",
            'endIntro': "Ecco la lista di giocatori e il loro team di origine:\n",
            'intro': "<b>\U0001F47C\U0001F3FE STATO DEI GIOCATORI \U0001F47C\U0001F3FE</b>\n\n",
            'teamDERP': "<b>TEAM DERP</b> \U0001F530\n",
            'teamPYRO': "\n<b>TEAM PYRO</b> \U0001F525\n",
            'deadStart': "\n<b>\U00002620 Assassinati \U00002620</b>\n",
            'VIP': "%s (\U0001F31F VIP)\n",
        },

    'teamDERP':
        "\nSei un agente DERP! \U0001F530 Identifica e uccidi tutti i VIP!",

    'teamPYRO':
        "\nSei un agente PYRO! \U0001F525 Identifica e proteggi tutti i VIP!",

    'timeUp':
        "Il tempo è scaduto!",

    'update':
        "Da aggiornare!",

    'VIP':
        "\n\n%s (<b>%s</b>) è uno dei VIP (o l'unico)!",

    'VIPself':
        "\n\nSei uno dei \U0001F31F <b>VIPs</b> (o l'unico), e quindi, un agente <b>PYRO! \U0001F525 </b> "\
        "Trova gli altri agenti PYRO per farti proteggere da loro!",

    'welcomeChoice':
        "Italian selezionato!",

    'yes':
        "Si",
    }

BR = {
    'about':
        "<b>Sobre o jogo</b>\n"\
        "Este jogo foi inspirado em Spyfall, Overwatch e Werewolf.\n\n"\
        "<b>Sobre o desenvolvedor</b>\n"\
        "Pode entrar em contato em @Anyhowclick!\n"\
        "<b>Tradutores</b>\n"\
        "Italiano: @MatteoIlGrande\n"\
        "Português do Brasil: @Liozek, @Alchimicus",

    'abilityUsed':
        "<b>Habilidade usada!</b>",

    'abilityNotUsed':
        "<b>Habilidade não usada!</b>",

    'acknowledgement': "Ok.",

    'agentDesc': "You are <b>%s</b>!\n",
    
    'agentDescription':
            "<b>Nome:</b> %s\n"\
            "<b>Classe:</b> %s\n"\
            "<b>Energia:</b> <code>%d</code>\n"\
            "<b>Dano:</b> <code>%d</code>\n"\
            "<b>Habilidade:</b> %s\n"\
            "<b>Recarga da habilidade:</b> %s",

    'agentDescriptionHealer':
            "<b>Nome:</b> %s\n"\
            "<b>Classe:</b> %s\n"\
            "<b>Energia:</b> <code>%d</code>\n"\
            "<b>Dano:</b> <code>%d</code>\n"\
            "<b>Quantidade de Cura:</b> <code>%d</code>\n"\
            "Observe que autocura tem uma eficácia de 50%%, e os médicos somente podem escolher entre causar dano"\
            "ou curar agentes, mas não ambos em um mesmo turno.\n"\
            "<b>Habilidade:</b> %s\n"\
            "<b>Recarga da habilidade:</b> %s",

    'agents': OrderedDict([
        #For the agents button, and when allocated
        #Offense class
        #Format is agent: [name,class,hp,dmg,ultCD,desc,ultCD]
        ('#baa', ['Dracule','\U0001F981 Ataque',100,25,'2 turnos',
                  "Recupera parte da energia quando ataca."]),

        ('#bab', ['Grim','\U0001F981 Ataque',100,22,'3 turnos',
                  "Ataca até 3 agentes, causando 25 de dano por alvo."]),

        ('#bac', ['Jordan','\U0001F981 Ataque',100,22,'5 turnos',
                  "Combine sua energia com seu alvo e a divida igualmente!"]),

        ('#bad', ['Novah', '\U0001F981 Ataque',100,22,'5 turnos',
                  "Doe energia para causar dano extra."]),
    
        ('#bae', ['Saitami','\U0001F981 Ataque',100,25,'4 turnos',
                  "Deixe seu alvo com 1 de energia (fatal se energizado!)"]),
    
        ('#baf', ['Sonhae','\U0001F981 Ataque',85,30,'3 turnos',
                  "Atire explosivos C4 em um oponente para causar muito dano!"]),

        ('#bag', ['Taiji','\U0001F981 Ataque',100,25,'3 turnos',
                  "Desvia de volta os danos direcionados para quem os causou por 1 turno (exclui algumas habilidades)"]),

        #Tank class
        ('#bba', ['Aspida','\U0001F98D Defesa',130,20,'3 turnos',
                  "Providencia um escudo (dura 1 turno) para 1 agente"]),

        ('#bbb', ['Hamia','\U0001F98D Defesa',130,20,'2 turnos',
                  "Aumenta a redução do dano em 50% para 1 agente."]),

        ('#bbc', ['Harambe','\U0001F98D Defesa',130,20,'3 turnos',
                  "Dê cobertura a 1 agente por 1 turno! Todo o dano direcionado a ele será absorvido por você."\
                  "Além disso, você irá recuperar 25% de todo o dano sofrido neste turno."]),

        ('#bbd', ['Impilo','\U0001F98D Defesa',130,20,'4 turnos',
                  "Recupere 20 de energia ou 20% da energia restante, o que for maior. "\
                  "Você também aumenta a redução de dano por 1 turno.",]),
    
        #Healer class
        #Note: They have an additional attribute (healAmt), so....
        #Format is agent: [name,class,hp,dmg,heal,ultCD,desc,ultCD]
        ('#bca', ['Elias','\U0001F54A Médico',90,17,10,'2 turnos',
                  "Revela a qual time um agente pertence!"]),

    #'grace': ['Grace','\U0001F54A Médico',90,17,10,7,
    #          "Ressuscita um agente com metada da energia base dele."],
        ('#bcb', ['Prim','\U0001F54A Médico',90,17,10,'3 turnos',
                  "Faz com que a habilidade de um agente esteja disponível para ele ou ela no próximo turno."]),

        ('#bcc', ['Ralpha','\U0001F54A Médico',90,17,10,'4 turnos',
                  "Cura um agente em até 80% da sua energia base (70% se usado em você)."]),

        ('#bcd', ['Sanar','\U0001F54A Médico',90,17,10,'3 turnos',
                  "Cura até 3 agentes (eficácia de 50% se usado em você)."]),

    #'yunos': ['Yunos','\U0001F54A Médico',90,17,10, '3 turnos',
    #          "Distribui escudos de energia a, no máximo, 3 agentes."],
    
        #Support class
        ('#bda', ['Anna','\U0001F436 Suporte',100,20,'2 turnos',
                  "Energiza um agente (Aumenta o dano, a quantidade de cura, se aplicável, "\
                  "e as habilidades são energizadas, se possível, por 1 turno)."]),

        ('#bdb', ['Jigglet','\U0001F436 Suporte',100,20,'3 turnos',
                  "Adormece um agente por 1 turno, tornando-o inofensivo por 1 turno."]),

        ('#bdc', ['Munie','\U0001F436 Suporte',100,20,'3 turnos',
                  "Torna 1 agente protegido contra danos e efeitos negativos por 1 turno."]),
    
    #'puppenspieler': ['Puppenspieler','\U0001F436 Suporte',100,20,4,
    #                  "Control an agent for 1 turn. That agent's ability may be used as well (if available)."],
    
    #'simo': ['Simo','\U0001F436 Suporte',100,20,2,
    #         "Fire a shield-piercing bullet, breaking the shield of an agent (and so deals extra damage). "\
    #         "If the agent is not shielded, then the bullet does slightly lower damage."],

    #Special case for Wanda, because her ult is variable
        ('#bdd', ['Wanda','\U0001F436 Suporte',100,20,'Depende dos alvos escolhidos. 4 turnos para médicos e 3 turnos para os demais.',
                  "Impede que 1 agente seja curado por 1 turno. Caso este agente seja um médico, "\
                  "não poderá curar outros agentes."]),
        ]),
    
    'allotSuccess':
        "Papéis e times definidos! Quem é quem:\n",

    'attHealOption':
        {'att': "Ataque \U0001F5E1",
         'heal': "Cura \U0001F489",
         'ult': "Habilidade \U00002728",
         },

    'choiceAccept':
        "Opção escolhida: <b>%s</b>",

    'combat':
        {
            'deflect': "%s desvia o ataque de %s!\n",
            'die': "%s <b>foi assassinado</b> \U00002620!!\n",
            'failHeal': "%s não conseguiu curar %s! \U0001F61E\n",
            'failHealSelf': "%s tentou se auto-\U0001F489, mas não conseguiu!\n",
            'failShield': "%s não conseguiu proteger %s!\n",
            'heal': "%s tem %d de energia após receber cura de %s!\n",
            'hurt': "%s \U0001F52A %s!\n",
            'intro': "<b>\U00002694 RODADA %d \U00002694</b>\n",
            'invuln': "%s foi atacado por %s, mas está protegido!\n",
            'KO': "<b>Você foi assassinado(a) \U0001F480!!</b>",
            'protect': "O ataque de %s foi desviado para %s!\n",
            'res': "You have been <b>raised from the dead \U0001F3FB!</b> Get back into the fight \U0001F3FB!!",
            'recover': "%s recupera %d de energia!\n",
            'selfAtt': "%s causa dano em si mesmo! \U0001F635\n",
            'selfHeal': "%s agora tem %d de energia depois da auto-\U0001F489!\n",
            'sleepAtt': "%s está \U0001F634, e não pôde \U0001F52A!\n",
            'sleepUlt': "%s está \U0001F634 e não pôde usar sua habilidade!\n",
            'shieldBroken': "O %s \U0001F6E1 foi destruído por %s!\n",
            'shieldIntact': "%s causou dano ao escudo de %s (%d energia \U000026A1 restante)!\n",
            'shieldFailHeal': "O escudo de %s não conseguiu curara %s!\n",
            'shieldHeal': "%s tem agora %d de energia após ser curado pelo escudo de %s!\n",
            'teamDERP': 'em <b>team DERP \U0001F530</b>',
            'teamPYRO': 'em <b>team PYRO \U0001F525</b>',
            'teamPYROVIP': 'um \U0001F31F <b>VIP</b> no <b>time PYRO \U0001F525</b>',
            'ult':
                {
                    'Anna': "%s foi fortalecido por %s neste turno!\n",
                    'AnnaSelf': "%s está mais forte neste turno!\n",
                    'Aspida': "%s \U0001F6E1 (<b>%d</b> energia \U000026A1) %s\n",
                    'AspidaSelf': "%s \U0001F6E1 a sim mesma (<b>%d</b> energia \U000026A1)\n",
                    'Dracule': "Caso tenha sucesso, o ataque de %s recupera energia neste turno!\n",
                    'Elias': "%s sabe a qual time %s pertence! \U0001F60F\n",
                    'EliasSelf': "%s revelou a si mesmo sua identidade (o que é bem inútil), mas, enfim...\n",
                    'EliasPrivate': "%s é %s",
                    'EliasSelfPrivate': "Não sabe a qual time pertence? \U0001F611 "\
                                        "Talvez esteja com preguiça de correr as mensagens anteriores. Enfim, você é %s",
                    'Grim': '%s \U0001F52B em %s!\n',
                    'Harambe': "%s protege %s neste turno! Irá recuperar 25%% de todo o dano causado a ele!\n",
                    'Hamia': "%s intensificou a redução de dano de %s neste turno!\n",
                    'Impilo': "%s intensificou a redução de dano e recuperou a energia de %d!\n",
                    'ImpiloFailHeal': "%s intensificou a redução de dano, mas não conseguir recuperar a energia! \U0001F61E\n",
                    'Jigglet': "%s fez %s \U0001F634!\n",
                    'JiggletSelf': "%s dormiu U0001F634!\n",
                    'Jordan': "%s \U0001F494 dividiu sua energia com %s! Agora ambos agentes têm %d de energia!\n",
                    'JordanSelf': "A habilidade de %s falhou!\n",
                    'Munie': '%s protegeu %s neste turno!\n',
                    'MunieSelf': "%s está protegido nesten turno!\n",
                    'NovahNOK': "%s tentou ativar sua habilidade, mas não tem energia suficiente!\n",
                    'NovahOK': "%s sacrificou 5 de energia para causar dano extra neste turno!\n",
                    'Prim': "%s fez com que %s pudesse usar sua habilidade no próximo turno!\n",
                    'PrimSelf': "%s tentou, mas não conseguiu usar em si mesma sua habilidade!\n",
                    'Ralpha': "%s recupertou 80%% da energia de %s! \U0001F48A\n",
                    'RalphaSelf': "%s recuperou 70%% de sua própria energia! \U0001F48A\n",
                    'revealFail': "Foi mal, mas %s está protegido. ¯\_(ツ)_/¯",
                    'Saitami': "%s foi atingido pela bala divina de %s, e agora só tem 1 de energia restante!\n",
                    'SaitamiPower': "%s atirou explosivos C4 em %s!\n",
                    'Sonhae': "%s threw C4 explosives at %s!\n",
                    'Taiji': "%s irá desviar de volta todos os danos para quem o atacar neste turno!\n",
                    'Wanda': "%s evitou que %s fosse curado \U0001F48A neste turno!\n",
                    'WandaSelf': "Por razões desconhecemos, %s evitou que fosse curado \U0001F48A neste turno!\n",
                    'WandaHealer': "%s evitou que %s fosse curado \U0001F48A e que cure outros \U00002695 neste turno!\n",
                },
            
            'ultInvuln': "%s tentou usar sua habilidade em %s, mas %s está protegido!\n",

        },
    'config':
        {'back': "\U0001F519",
         'done': "Até logo!",
         'exit': "Sair \U000023CF",
         'intro': "O que gostaria de alterar no grupo <b>%s</b>?",
         'lang':'\U0001F30D Idioma',
         },
    
    'countdownNoRemind': "<b>%d</b> segundos restantes para entrar na partida!",

    'countdownRemind':
        "<b>%d</b> segundos restantes para entrar na partida! Verifique "\
        "se já tem uma conversa privada comigo (vá em @DERPAssassinBot) antes de acessar o /join@DERPAssassinBot!",

    'countdownChoice':
        "<b>%d</b> segundos para que os agentes sobreviventes executem seus planos!",

    'countdownToPhase1':
        "\n<b>%d</b> segundos para discussão!",

    'countdownToPhase2':
        "Os agentes sobreviventes têm <b>%d</b> segundos para executar suas ações!",

    'delay':
        "\nA partida vai começar em 5 segundos! Agentes, estejam preparados!\n",

    'donate':
        "Obrigado por dar suporte ao desenvolvimento desse jogo. Abaixo estão as seguintes formas em que você pode doar.\n"\
        "1. Ethereum address: <code>0xb4c82ff1a2b63cd1585c7b849604ad40a6d3ab35</code> \n"\
        "2. Litecoin address: <code>LcpU4jwZN5oLsC3p9EPekkcxyRYJpiBFUw</code> \n"\
        "Está tudo bem se não puder, só aproveite o jogo!",

    'existingGame':
        "Uma partida está em andamento agora!",

    'endGame':
        {'draw': "\nNenhum lado venceu desta vez. O jogo <b>TERMINOU EM EMPATE!</b>",
         'rareDraw': "\nDe alguma forma os dois times têm a mesma energia, então o jogo <b>TERMINOU EM EMPATE!</b>",
         'DERP.KO': "\nNossa, os agentes da PYRO provaram que são quentes demais \U0001F525 para suportar! <b>TIME PYRO \U0001F525 VENCE!</b>",
         'DERPWin': "<b>TEAM DERP \U0001F530 VENCE!</b>",
         'PYRO.KO': "\nO pessoal de cabeça fria congelou \U00002744 no mar do esquecimento os criminosos! <b>TIME DERP \U0001F530 VENCE!</b>",
         'PYROVIP.KO': "\nTodos os VIPs se foram \U00002744! <b>TIME DERP \U0001F530 VENCEU!</b>",
         'PYROWin': "<b>TIME PYRO \U0001F525 VENCEU!</b>",
         'tooLong': "Esse jogo ficou por muito tempo inativo! O time com mais energia ganhou!",
         'tooLongSummary': "Time DERP: <b>%d hp</b>\nTime PYRO: <b>%d hp</b>\n",
        },

    'error': "Algo de errado aconteceu. Fale com @Anyhowclick se o erro continuar.",
    
    'failStart':
        {'lackppl':"Sem jogadores suficientes, não se pode iniciar o jogo!",},

    'failTalk':
        "Fale comigo no privado primeiro, %s! Aqui: @DERPAssassinBot",

    'findOutChar':
        "Escolha seu agente.\n"\
        "\U0001F981 Agentes de ataque causam maior dano.\n"\
        "\U0001F98D Os fortes têm mais energia.\n"\
        "\U0001F54A Médicos podem curar outros agentes.\n"\
        "\U0001F436 Agentes de suporte têm hablidades para ajudar o time.\n",

    'gifs': #File_ids of gifs stored on telegram servers
        {'drawVidID': "BQADBQADGAADtFzTEYTmkivEF03PAg",
         'DERPVidID': "BQADBQADGgADtFzTEZqVI4tYFx3MAg",
         'PYROVidID': "BQADBQADGQADtFzTEZ5k3pNuPxYKAg",
         },

    'groups':
        "Aqui estão os grupos que você talvez queira entrar:\n\n",

    'groupsMemberCount':
        "<b>%s membros</b>\n\n",

    'info':
        "O que você gostaria de saber?",

    'initialise':
        "Initialising...",

    'invalidCommand':
        "Comando inválido.",

    'invalidText':
        "Desculpe, eu não entendi o que você disse.",

    'isInGame':
        "Você já está em um jogo, ou acabou de entrar em um!",

    'joinGame':
        {'Max':
             "<b>%s</b> entrou no jogo. Limite de jogadores atingido!\n",
         'notMax':
             "<b>%s</b> entrou no jogo. No momento <b>%d</b> jogadores.\n"\
             "<b>%d</b> minimo de jogadores, <b>%d</b> máximo",
         },

    'joinToUser':
        "Você entrou no jogo!",

    'killGame':
        "O jogo foi cancelado!",

    'killGameAgents':
        "Desculpe, temos um problema. O jogo foi cancelado por um administrador do grupo.",

    'leaveGame': "<b>%s</b> saiu do jogo!\n",
    'leaveGame1': "O jogo parou quando <b>%s</b> saiu.\n",

    'lonely':
        "Encontre alguns amigos para jogar com você, entrando em qualquer um desses grupos que podem ser encontrados no menu!",

    'maintenance':
        {'shutdown': "O bot está <b>parado para manutenção.</b> Acesse @DerpAssUpdates para "\
                     "ter mais notícias!\n\n",
         'status': "Bot status: %s",
         },

    'menu':
        {'about':'\U00002139 Sobre',
         'agents':'\U0001F63C Agentes',
         'back': '\U0001F519',
         'donate':'\U0001F4B5 Doe',
         'global':'\U0001F30F Global',
         'groups':'\U0001F465 Grupos',
         'info': '\U00002753 Como jogar',
         'lang':'\U0001F30D Idioma',
         'modes': '\U0001F3AE Modos de jogo',
         'personal': '\U0001F464 Pessoal',
         'rate': '\U00002B50 Avalie',
         'rules': '\U0001F4C3 Regras',
         'soon': 'Em breve!',
         'stats': '\U0001F3C5 Estatísticas',
         'support': '\U0001F6A8 Ajuda',
         'upgrades': '\U0001F199 Melhorias',
         },
    
    'newGame':
        "\n%s começou um novo jogo! /join@DERPAssassinBot para entrar.\n"\
        "Me mande uma mensagem primeiro, se você ainda não fez isso! Aqui: @DERPAssassinBot.\n"\
        "Mínimo de <b>%d</b> jogadores, máximo de <b>%d</b>\n",

    'newGameToUser':
        "Você começou um novo jogo!",

    'nextGameNotify':
        "Você será notificado quando o jogo começar em <b>%s</b>!",

    'nextGameNotifyNoTitle':
        "Você será notificado quando o jogo começar!",

    'nextGameNoUsername':
        '\nUm novo jogo começou em <b>%s</b>\n',

    'no':
        "Não",

    'none':
        "Eu acabei de escolher!",

    'notGroup':
        "Esse comando só está habilitado em grupos.",
    
    'notGroupAdmin':
        "Somente os administradores do grupo podem usar esse comando.",
    
    'notPrivateChat':
        "Esse comando só está disponível em chats privados.",

    'okStart':
        "Definindo papéis e times dos agentes...",

    'powerUp':
        {   
            'eat': "\U0001F60B Usar",
            'no': "Você decidiu não usar o bônus. \U0001F910",
            'noEat': "\U0001F910 Não usar",
            'intro': "<b>Power-Up Disponível!</b>\n",
            'yes': "Você decidiu usar o bônus. \U0001F60B",
            'zero': "Ninguém quis o bônus.\n",
            'DmgX':
                {'bad':
                    "{names} \U0001F5E1 \U0001F53D em <b>{percent:.2f}%</b>!",
                'desc':
                     "\U0001F347: \U0001F53C or \U0001F53D dano.\n"\
                     "Recomendado: <b>%s</b> agentes\n"\
                     "<b>{}</b> agentes vão usar.",
                 'good':
                     "{names} \U0001F5E1 \U0001F53C em <b>{percent:.2f}%</b>!",
                },
            
            'Health':
                {'bad':
                    "\U0001F53D <b>%d</b> \U00002764!",
                'desc':
                    "\U0001F34E: \U0001F53C or \U0001F53D hp.\n"\
                    "{} agents will be eating it.",
                 'good':
                     "\U0001F53C <b>%d</b> \U00002764!",
                },
            
            'LoD':
                "\U0001F351: Restores health to full \U0001F607, or brings death \U00002620.\n"\
                "<b>%s</b> \U0001F351's available. Who wants to eat it?\n\n",
        },

    'query':
        {'canUlt': "Habilidade disponível! Deseja usar?",
         'doWhat': "O que gostaria de fazer neste turno?",
         'doWhatNext': "O que gostaria de fazer agora? \U0001F601",
         'attack': "Quem você gostaria de atacar?",
         'heal': "Quem você gostaria de curar?",
         'select':
             {1: "Selecione seu %dst alvo ",
              2: "Selecione seu %dnd alvo ",
              3: "Selecione seu %drd alvo ",
              4: "Selecione seu %dth alvo ", #To take note that anything more should fall under this case, so set min(4,num) in code
              },
         'ult':
             {'Anna': "Escolha alguém para receber um bônus!",
              'Aspida': "A quem você gostaria de dar um escudo neste turno?",
              'Elias': "De quem gostaria que a identidade fosse revelada?",
              'Grim': "para ATIRAR! \U0001F52B",
              'Hamia': "Escolha alguém para intensificar sua redução de danos. \U0001F590\U0001F3FE",
              'Harambe': "Quem você gostaria de \U0001F6E1 proteger?",
              'Jigglet': "Quem você gostaria que \U0001F634?",
              'Jordan': "Com quem você gostaria de \U0001F494 dividir sua energia?",
              'Munie': "Escolha alguém para proteger.",
              'Prim': "Escolha alguém para ter sua habilidade ativada no próximo turno.",
              'Ralpha': "De quem você gostaria de restaurar a energia? \U0001F36D",
              'Sanar': "de curar! \U0001F496",
              'Saitami': "Em quem gostaria de atirar sua bala divina \U0001F52B?",
              'Sonhae': "Quem você gostaria de explodir \U0001F600?",
              'Wanda': "Escolha alguém que não poderá ser curado (e nem curar os outros).",
              },
         },

    'rate':
        '<a href="https://telegram.me/storebot?start=derpassassinbot">Você pode avaliar esse bot</a>! '\
        'Eu agradeço por isso! \U0001F60A',      
    
    'rules':
        {'sent':"Veja abaixo!",
         'fileID':"AgADBQADxacxGxZ3-VSOUGZoMvVlvL8byjIABLilrrw2eJwN9L4DAAEC",
         },

    'spam':
        {1:"Não irei lhe responder por %.1f minutos (a não ser que você esteja em um jogo). Isso é uma medida anti-spam. Desculpe por isso!",
         2:"\U0001F910",
         },

    'stats':
        {
            'des':
                "\nNo. of active games: <code>{}</code>\n"\
                "No. of active players: <code>{}</code>\n\n",
            
            'global':
                "Número total de jogadores: <code>{d[players]}</code>\n"\
                "Número total de grupos: <code>{d[groups]}</code>\n"\
                "Partidas jogadas \U0001F579: <code>{p[0]}</code>\n"\
                "Jogos que ganhou como \U0001F530 DERP: <code>{d[derpWins]}</code> <code>({p[1]:.2f})%</code>\n"\
                "Empates: <code>{d[drawsNormal]}</code> <code>({p[2]:.2f})%</code>\n"\
                "Jogos que ganhou como \U0001F525 PYRO: <code>{d[pyroWins]}</code> <code>({p[3]:.2f})%</code>\n"\
                "Melhor agente \U0001F396: <b>{d[bestNormalAgent][name]}</b> <code>{d[bestNormalAgent][rate]:.3f}</code> vitórias por jogo\n"\
                "Melhor \U0001F525 agente PYRO:: <b>{d[pyroNormalWins][name]}</b> <code>{d[pyroNormalWins][rate]}</code> vitórias\n"\
                "Melhor \U0001F530 agente DERP:: <b>{d[derpNormalWins][name]}</b> <code>{d[derpNormalWins][rate]}</code> vitórias\n"\
                "Melhor sobrevivente: <b>{d[normalSurvivor][name]}</b> <code>{d[normalSurvivor][rate]}%</code>\n"\
                "Maior causador de dano: <b>{d[mostDmgNormal][name]}</b> <code>{d[mostDmgNormal][rate]}</code> \U00002694 em um jogo\n"\
                "Quem mais restarou energia:  <b>{d[mostHealAmt][name]}</b> <code>{d[mostHealAmt][rate]}</code> \U0001F489 em um jogo\n"\
                "Melhor assassino \U0001F575\U0001F3FD: <b>{d[mostPplKilled][name]}</b> <code>{d[mostPplKilled][rate]}</code> agentes\n"\
                "Melhor médico \U0001F47C\U0001F3FB: <b>{d[mostPplHealed][name]}</b> <code>{d[mostPplHealed][rate]}</code> agentes\n"\
                "Atualizado pela última vez em: <code>{d[lastUpdated]} GMT</code>\n",
            
            'local':
                "Partidas jogadas \U0001F579: <code>{d[normalGamesPlayed]}</code>\n"\
                "Jogos que ganhou como \U0001F530 DERP: <code>{d[derpNormalWins]}</code> <code>({p[0]:.2f})%</code>\n"\
                "Empates: <code>{d[drawsNormal]}</code> <code>({p[1]:.2f})%</code>\n"\
                "Jogos que ganhou como \U0001F525 PYRO: <code>{d[pyroNormalWins]}</code> <code>({p[2]:.2f})%</code>\n"\
                "Partidas como sobrevivente: <code>{d[normalGamesSurvived]}</code> <code>({p[3]:.2f})%</code>\n"\
                "Número de agentes assassinados \U0001F480: <code>{d[mostPplKilled]}</code>\n"\
                "Número de agentes curados \U0001F47C\U0001F3FB: <code>{d[mostPplHealed]}</code>\n"\
                "Maior dano causado \U00002694: <code>{d[mostDmgNormal]}</code>\n"\
                "Maior quantidade de energia recuperada \U0001F48A: <code>{d[mostHealAmt]}</code>\n",

            'normal':
                "Agentes curados \U0001F47C\U0001F3FB: {tup[0]}\n"\
                "Agentes mortos \U0001F480: <code>{tup[1]}</code>\n"\
                "Cura \U0001F48A feito: <code>{d[healAmt]}</code>\n"\
                "Dano \U00002694 feito: <code>{d[dmg]}</code>",
            
            'query':"Quais estatísticas você gostaria de ver?",
        },
    
    'start':
        "Olá! Me adicione em algum grupo e envie /normalgame@DERPAssassinBot para começar um novo jogo com seus amigos!  "\
        "Todos os jogadores devem me mandar uma mensagem no privado, aí eu poderei respondê-los!\n"\
        "Explore o menu para saber mais e aprender sobre o jogo, ou entre em um grupo para começar logo!",

    'support':
        "Se você tem um feedback ou sugestão ou se descobriu bugs no jogo ou ainda se gostaria de participar do "\
        "desenvolvimento do jogo (mas você não será pago \U0001F61D), você pode me mandar uma mensagem aqui  "\
        "@Anyhowclick \U0001F603.\n"\
        "Você deve ir para @DerpAssUpdates para checar por manutenções e atualizações futuras!\n\n"\
        "<a href='https://github.com/Anyhowclick/DERPAssassination'>Aqui está o código fonte para o jogo!</a>\U0001F601",

    'summary':
        {
            'agent': "%s\n",
            'agentStart': "%s: <b>%s</b>\n",
            'alive': "%s <b>(%d hp)</b>\n",
            'aliveStart': "<b>\U0001F60E Sobreviventes \U0001F60E</b>\n",
            'deadDERP': "%s <b>(\U0001F530 Agente DERP!)</b>\n",
            'deadPYRO': "%s <b>(\U0001F525 Agente PYRO!)</b>\n",
            'deadPYROVIP': "%s <b>(\U0001F31F VIP!!)</b>\n",
            'DERPintro': "Aqui estão seus aliados:\n",
            'endIntro': "Quem pertencia a cada time:\n",
            'intro': "<b>\U0001F47C\U0001F3FE SITUAÇÃO DOS JOGADORES \U0001F47C\U0001F3FE</b>\n\n",
            'teamDERP': "<b>TIME DERP</b> \U0001F530\n",
            'teamPYRO': "\n<b>TIME PYRO</b> \U0001F525\n",
            'deadStart': "\n<b>\U00002620 Assassinou \U00002620</b>\n",
            'VIP': "%s (\U0001F31F VIP)\n",
        },

    'teamDERP':
        "\nVocê é um agente DERP \U0001F530! Encontre e destrua todos os VIPs!",

    'teamPYRO':
        "\nVocê é um agente PYRO \U0001F525! Encontre e proteja todos os VIPs!",

    'timeUp':
        "Tempo esgotado!",

    'update':
        "Em atualização!",

    'VIP':
        "\n\n%s (<b>%s</b>) é um dos VIPs!",

    'VIPself':
        "\n\nVocê é um dos \U0001F31F <b>VIPs</b> e, portanto, é um agente <b>PYRO \U0001F525!</b> "\
        "Descubra os demais agentes PYRO e convença-os a protegê-lo(a)!",

    'welcomeChoice':
        "Português do Brasil selecionado!",

    'yes':
        "Sim",
    }

async def send_message(bot,ID,message,parse_mode='HTML',reply_markup=None,disable_web_page_preview=True):
    try:
        result = await bot.sendMessage(ID,message,
                                       parse_mode=parse_mode,
                                       reply_markup=reply_markup,
                                       disable_web_page_preview=disable_web_page_preview)
    except telepot.exception.BotWasBlockedError:
        return

    except telepot.exception.TelegramError:
        return
    return result

async def edit_message(editor,message,reply_markup=None,parse_mode='HTML',disable_web_page_preview=True):
    try:
        result = await editor.editMessageText(message,
                                              reply_markup=reply_markup,
                                              parse_mode=parse_mode,
                                              disable_web_page_preview=disable_web_page_preview)
    except telepot.exception.TelegramError:
        try:
            result = await editor.editMessageReplyMarkup(reply_markup=reply_markup)
        except telepot.exception.TelegramError:
            return
        except AttributeError:
            return

    except AttributeError:
        return

    return result
