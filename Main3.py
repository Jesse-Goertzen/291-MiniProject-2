from bsddb3 import db
import re
import Date
from Parser import Parser

# datebase.get(b'stuff')
# only returns a value

# curs.set(b'stuff')
# returns the associated key/value pair

# examples:
# Starting_Name = input("Enter the Starting_Name: ")
# result = curs.set_range(Starting_Name.encode("utf-8")) 

# if (str(result[0].decode("utf-8")[0:len(Ending_Name)]) < Ending_Name):     check if name comes before ending_name

def main():
    while True:
        #query = input("Let me no whut your query is: ").lower()
        p = Parser()
        parsedq = p.parse(input("Let me no whut your query is: ").lower())
        dbfile = "./indexes/pr.idx"
        database = db.DB()
        #database.set_flags(db.DB_DUP)
        database.open(dbfile, None, db.DB_BTREE, db.DB_CREATE)
        curs = database.cursor()
        print(parsedq["price"])
       # curs = database.cursor()
        iterr = curs.first()
        while iterr:
            print(iterr)
            iterr = curs.next()
        curs.close()
        curs = database.cursor()
        result = curs.set_range((parsedq["price"][1]).encode("utf-8"))
        while result != None:
            if int(result[0].decode("utf-8")) < int(parsedq["price"][1]):
                break
            print(result[0].decode("utf-8"))
            result = curs.next()


main()
