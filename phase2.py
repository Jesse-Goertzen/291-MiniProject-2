from bsddb3 import db
import re

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
            match = re.search("(\\d{4}/\\d{2}/\\d{2}):(.*)", l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()

def pricesBtree(name="./indexes/pr.idx"):
    database = db.DB()
    database.open(name, None, db.DB_CREATE|db.DB_BTREE)
    with open("./output/prices.txt", 'r') as f:
        for l in f:
            match = re.search("(\\d*):(.*)", l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()
    
def termsBtree(name="./indexes/te.idx"):
    database = db.DB()
    database.open(name, None, db.DB_BTREE|db.DB_CREATE)
    with open("./output/terms.txt", 'r') as f:
        for l in f: 
            match = re.search("(.*):(.*)", l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()
