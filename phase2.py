from bsddb3 import db
import re

# Dunno if we'll need this but I had the idea and wanted to make it just incase
from time import sleep
from os import system
def boolInput(string, clear=True):
    while True:
        if clear:
            system('cls||clear')
        sel = input(string + '[y/n]\n\r').lower()
        if sel == y:
            return True
        elif sel == n:
            return False
        else:
            print("Invalid selection, try again.")
            sleep(0.75)

def adsHash(name="./indexes/ad.idx"):
    database = db.DB()
    database.open(name, None, db.DB_HASH, db.DB_CREATE)
    with open("./output/ads.txt", 'r') as f:
        for l in f:
            match = re.search("(\\d{10}):(.*)",l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data, db.DB_KEYFIRST)


