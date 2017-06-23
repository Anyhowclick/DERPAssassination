import asyncio
'''
DBP will be used to store queries and info from PERSONS
DBG will be used to store group game instances
LOCALID and GRPID stores personal and group statistics respectively
GLOBAL_STATS stores global statistics
LANG will store languages used by people / group (object)
QUEUE is a global queue to handle writing into different python dicts (thread safety)
Refer to StatsFormat for the type of statistics stored for GLOBALSTATS
'''

def init():
    global DBP, DBG, LANG, LOCALID, GRPID, GLOBAL_STATS, SPAM, QUEUE, STATS
    global MAINTENANCE
    
    DBP, DBG, LANG, LOCALID, GRPID, GLOBAL_STATS, SPAM = {},{},{},{},{},{},{}
    QUEUE = asyncio.Queue() #Item placed is of format: (dictionary,key,value)
    MAINTENANCE = True
