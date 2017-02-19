# DERP:Assassination

## Upcoming changes, last updated 19/2/17
- Raise minimum players from 2 to 3 (TBC)
- Add support group link in /support

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

## Python code for the game DERP:Assassination on Telegram.

This game was first conceptualised in October 2016. It has been a solo project up till this point (Jan 2017), so the code that I've written may not the best methods used. There's definitely room for improvement in terms of data structures and parsing / processing messages sent, so there'll be changes over time.
Nevertheless, I hope what's explained below will make my code easier to read, and if not, most of the codes have been commented to give a somewhat better understanding. 

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
