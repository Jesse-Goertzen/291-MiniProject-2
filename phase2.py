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
    database.open(name, None, db.DB_CREATE|db.DB_HASH)
    with open("./output/ads.txt", 'r') as f:
        for l in f:
            match = re.search("(\\d{10}):(.*)",l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()

def datesBtree(name="./indexes/da.idx"):
    database = db.DB()
    database.open(name, None, db.DB_CREATE|db.DB_BTREE)
    with open("./output/pdates.txt", 'r') as f:
        for l in f:
            match = re.search("(\\d{4}/\\d{2}/\\d{2}):(.*)")
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()

def pricesBtree(name="./indexes/pr.idx"):
    database = db.DB()
    database.open(name, None, db.DB_CREATE|db.DB_BTREE)
    with open("./output/prices.txt", 'r') as f:
        for l in f:
            match = re.search("(\\d*):(.*)")
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()