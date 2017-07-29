## Python code for the game DERP:Assassination on Telegram.

This game was first conceptualised in October 2016. It is a solo project thus far. Version 2 was recently released. Description of the files are listed below.

- Admin.py
  - Basic spam detection, updating of groups information, and toggling of maintenance status.
- Agent.py
  - Contains common attributes shared by every agent character, such as health, damage, attack methods, reset_for_next_round() etc.
- AgentClasses.py
  - A subclass of agent, to differentiate between the 4 classes: Offense, Tank, Healer and Support.
- CallbackHandler.py
  - Handles all callback queries from all games.
- ChatManager.py
  - Router to commandHandler.
- CommandHandler.py
  - Contains all non-game related commmands
- DatabaseStats.py
  - Getting and adding of a new person's / group's information, retrieving from Globals.QUEUE, autosave of database every 10 mins, updating of global stats, saving / loading of database and saving of languauge.
- Game.py
  - Game object to facilitate the game.
- GameHandler.py
  - Handles game-related commands, namely /join, /killgame and /newgame
- Globals.py
  - Contains global variables to be accessed by other python files, such as DBP, DBG and QUEUE.
- Heroes.py
  - Subclass of AgentClasses. Each individual agent and ability is stored here. 'Heroes' is used because 'Agent' was used already xD
- KeyboardQuery.py
  - Generation of different keyboards based on query received
- Main.py
  - Run this file with a bot API token obtained from theBotFather.
- Messages.py
  - Contains all text messages to be sent by the bot. Will contain the translations as well.
- PowerUp.py
  - Contains power-up attributes.
- README.md
  - This document!
- Shield.py
  - Shield object for an agent.
- StatsFormat.py
  - Sample JSON format of information stored for globalStats, localStats and grpStats.

## Changelog 29/7/17 DERP:Assassination V2 release on 3/7/17 ##
- Menu to replace most /commands
- Power-up event!
- Storing and displaying statistics

## Changelog 28/4/17 ##
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
