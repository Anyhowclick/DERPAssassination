## Python code for the game DERP:Assassination on Telegram.

This game was first conceptualised in October 2016. It has been a solo project up till now. After half a year of development, I considered switching to Node.js / Golang, but decided to stick to Python still. For now, the code that I've written may not be pretty, so I'm planning to rewrite a fair chunk of it, this time taking into consideration future expansions.

For now, I hope what's explained below will make my code easier to read, and if not, most of the codes have been commented to give a somewhat better understanding. 

- Admin.py
  - Basic spam detection, and contains the function to check whether someone is an admin of a group
- Agent.py
  - Contains common attributes shared by every agent character, such as health, damage, attack methods, reset_for_next_round() etc.
- AgentClasses.py
  - A subclass of agent, to differentiate between the 4 classes: Offense, Tank, Healer and Support. It also contains query handling methods, which honestly should be separated into another file.
- CallbackHandler.py
  - Handles all callback queries (/agents command) and queries from all games.
- ChatManager.py
  - Router to commandHandler.
- CommandHandler.py
  - Contains all non-game related commmands (/about, /support etc.)
- Database.py
  - To store variables accessible to other files. Most important is DB, because it stores game objects and agent objects.
- Game.py
  - Game object to facilitate the game.
- GameHandler.py
  - Handles game-related commands, namely /join, /killgame and /newgame
- Heroes.py
  - Subclass of AgentClasses. Each individual agent and ability is stored here. 'Heroes' is used because 'Agent' was used already xD
- Main.py
  - Run this file with a bot API token obtained from theBotFather.
- Messages.py
  - Contains all text messages to be sent by the bot. Will contain the translations as well.
- README.md
  - This document!
- Shield.py
  - Shield object for an agent. *Newest feature*

##Changelog 28/4/17 ##
- Decreased Harambe's health from 150hp to 130hp
- Saitami's ability powered up by Anna = instant KO
- New hero: Jigglet!
- New /rules --> self-designed image =)

## Changelog 15/3/17 1806 hrs
- Fixed HTML tag for "failed to join..." (just had to change method to send_message)
- Improved /rules command: Show TL:DR version in grp chats, full version obtained privately
- Ralpha nerfed: Restore 80% health on others / 70% on self (before was 100% / 80% respectively)

## Changelog 12/3/17 2228 hrs
- Adding Bahasa Indo in Messages.py
- Improved /nextgame command: Notification now occurs when a game starts, not when one ends!
- Added /group command to show groups which people can join
- Fixed a bug where Prim's ability failed to work for some characters (has to do with ordering in the dictionary in Game.py)
- Hamia now gives 50% dmg reduction! Also, Anna will boost this amount to 70%! His ability cooldown has been increased to 2 turns to balance this buff.
- Added auto-updated script (called with the special command in CommandHandler.py, routed to ChatManager.py for scheduling every hour, which calls the main function found in Admin.py). The script updates no. of members found in groups, and in the future, stats in the database
- Improved /killgame command (Forgot to remove users from DB, resulting in them being unable to join any other subsequent games)

## Changelog 3/3/17 1200 hrs
- Names are now clickable, and first names are used instead of usernames. Also, only agent names are shown in the combat log.
- Allocation of heroes to players has been made more random.
- Health shows 1 hp instead of 0 hp in cases where actual health of player is 0.something hp
- Removed /future command
- Majority of commands will be 'disabled' and instead show maintenance message upon incoming fixes / updates
- Hero Elias is made compulsory for games with >= 5 people; but not included in games with 3-4 people
- Dracule's lifesteal decreased from 100% to 60%
- Minimum number of players raised from 2 to 3
- Added link for support group.
  
## Changelog 19/2/17 1930 hrs
What's new:
  - Preparation for multi-language support
  - New /leave command in GameHandler.py
  - Used a bit more emojis in Messages.py (English version)
  - Replaced "COMBAT" with round number
  - Bot now sends fewer messages by editing previous messages whenever applicable. (To prevent hitting API limits)
  - Fixed a bug involving the scenario where Harambe shields himself, dies and recovers negative health
  - Minor bug fixes (Spelling errors, wrong caps etc.)
  
## Changelog 13/2/17 0051 hrs
What's new:
  - Tweaked ratio of VIPs to DERP agents (1:1.5 to 2 instead of 1:1)
  - Rules were edited accordingly to reflect the tweaked ratio
  - Tweaked timer that auto-adjusts based on no. of survivors and no. of rounds elapsed
  - Shorter combat logs by no longer showing remaining hp and the word "damages" for normal attacks in combat log. Remaining hp will be displayed only in summary message

## Changelog 28/1/17 0142 hrs
What's new:
- sendMessage and editMessageText now have a wrapper function called send_message and edit_message respectively, found under Messages.py for exception handling.
- Timer has been set to at least 90s for discussion time.
- Added source code link in /support and main group link in /start commands
- Minor text fixes.
