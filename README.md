# DERP:Assassination
## Python code for the game DERP:Assassination on Telegram.

This game was first conceptualised in October 2016. It has been a solo project up till this point (Jan 2017), so the code that I've written may not the best methods used. There's definitely room for improvement in terms of data structures and parsing / processing messages sent, so there'll be changes over time.
Nevertheless, I hope what's explained below will make my code easier to read, and if not, most of the codes have been commented to give a somewhat better understanding. 

- Admin.py
  - Basic spam detection, and contains the function to check whether someone is an admin of a group
- Agent.py
  - Contains common attributes shared by every agent character, such as health, damage, attack methods, reset_for_next_round() etc.
- AgentClasses.py
  - A subclass of agent, to differentiate between the 4 classes: Offense, Tank, Healer and Support
- CallbackHandler.py
  - Handles all callback queries (/agents command)
- ChatManager.py
- CommandHandler.py
- Database.py
- Game.py
- GameHandler.py
- Heroes.py
- Main.py
- Messages.py
- README.md
- Shield.py

### (To be continued)
