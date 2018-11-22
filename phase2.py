from bsddb3 import db
import re
import struct

def adsHash(name="./indexes/ad.idx"):
    database = db.DB()
    database.open(name, None, db.DB_HASH, db.DB_CREATE)
    with open("./output/ads.txt", 'r') as f:
        for l in f:
            match = re.search("([0-9a-zA-Z-_]+):(.*)",l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()

def datesBtree(name="./indexes/da.idx"):
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(name, None, db.DB_CREATE, db.DB_BTREE)
    with open("./output/pdate.txt", 'r') as f:
        for l in f:
            match = re.search("(\d{4}/\d{2}/\d{2}):(.*)", l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()

def pricesBtree(name="./indexes/pr.idx"):
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(name, None, db.DB_CREATE, db.DB_BTREE)
    curs = database.cursor()
    with open("./output/prices.txt", 'r') as f:
        for l in f:
            match = re.search("(.*):(.*)", l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)

    # curs.close()
    # curs = database.cursor()
    # iterr = curs.first()
    # while iterr:
    #    # print(iterr)
    #     print(struct.unpack('>l', iterr[0]))
    #     iterr = curs.next()
    # curs.close()

    database.close()
    
def termsBtree(name="./indexes/te.idx"):
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(name, None, db.DB_CREATE, db.DB_BTREE)
    with open("./output/terms.txt", 'r') as f:
        for l in f: 
            match = re.search("([0-9a-zA-Z-_]+):(.*)", l)
            key, data = match.group(1).encode(), match.group(2)
            database.put(key, data)
    database.close()


def init():
    termsBtree()
    pricesBtree()
    datesBtree()
    adsHash()

#  Test to iterate and print all values that were put into the database. Put loop before database.close()
#    curs = database.cursor()
#    iterr = curs.first()
#    while iterr:
#        print(iterr)
#        iterr = curs.next()
#    curs.close()

init()