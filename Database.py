from Messages import LANGEMOTES, setLang, ZH, IN, EN, send_message, ALL_LANGS
import sqlite3
import telepot
import asyncio
from telepot.namedtuple import *
DB, LANG, SPAM, BLOCKED, STRIKE = {},{},{},{},{}

def setup():
    conn = sqlite3.connect('DERPAssPreferences.db')
    db = conn.cursor()
    # Create table
    db.execute("""
       CREATE TABLE settings
       (ID text PRIMARY KEY,lang text)
       """)
    # Save (commit) the changes
    conn.commit()
    # Close connection
    conn.close()
    return

def load_preferences():
    global LANG
    conn = sqlite3.connect('DERPAssPreferences.db')
    db = conn.cursor()
    # Load all saved preferences in LANG
    db.execute('''SELECT ID, LANG FROM settings''')
    for row in db.fetchall():
        #Codes are gotten from ISO standard
        if row[1] == 'ZH':
            LANG[row[0]] = ZH
        elif row[1] == 'IN':
            LANG[row[0]] = IN
        else:
            LANG[row[0]] = EN
    conn.close()
    return

# Function to group elements together by iterating through sequence
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# Let user select their preferred language, store in database
async def set_lang(bot,userID,start=False,extra=None):
    #start variable is to see if welcome message is to be included
    #extra option is to allow only the admin to reply to the message
    keyboard = []
    for group in chunker(ALL_LANGS,3):
        result = []
        for element in group:
            result.append(InlineKeyboardButton(text=LANGEMOTES[element],
                                               callback_data=(element+'@@' if start else element)))
        keyboard.append(result)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await send_message(bot,userID,setLang,
                       reply_markup = markup)
    return

def save_lang(ID,choice):
    #Save into offline DB
    conn = sqlite3.connect('DERPAssPreferences.db')
    db = conn.cursor()
    #Check if language is to be updated, or inserted as a new entry
    db.execute('SELECT ID FROM settings WHERE ID = ?',(ID,))
    item = db.fetchone()
    if item: # Means there is an existing entry, so update value
        db.execute("""
        UPDATE settings
        SET LANG = ?
        WHERE ID = ?
        """,(choice,ID))
    else:
        db.execute('INSERT INTO settings VALUES (?,?)', (ID,choice))
    conn.commit()
    conn.close()
    #Finally, save preference in LANG database
    if choice == 'ZH':
        LANG[ID] = ZH
    elif choice == 'IN':
        LANG[ID] = IN
    else:
        LANG[ID] = EN
    return LANG[ID]['welcomeChoice']
