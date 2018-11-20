from bsddb3 import db
import re
import Date
from Parser import Parser
import struct

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
        database.open(dbfile, None, db.DB_BTREE)
        curs = database.cursor()
        # line under must be changed from "thing" to whatver key you want such as "date"
        print(parsedq["price"])
       # curs = database.cursor() 
       # aint nobody knows what happens beyond this point
       # !WARNING! !WARNING!
 #       iterr = curs.first()
 #       while iterr:
 #           print(iterr)
 #           iterr = curs.next()
 #       curs.close()
        curs = database.cursor()
        result = curs.set_range(struct.pack('>l', int(parsedq["price"][0][1])))

        # testing for logic with inequalities
        # first is the >, else is <. Each individually therefore would have their own while loops for when >=
        if parsedq["price"][0][0][0] == ">":
            
            # loop is for when >= is the string, might not have to bother with making sure its an equal sign...
            # while loops through all the same values
            if (len(parsedq["price"][0][0]) > 1) and (parsedq["price"][0][0][1] == "="):
                while struct.unpack('>l', result[0])[0] == int(parsedq["price"][0][1]):
                    print(struct.unpack('>l', result[0])[0])
                    result = curs.next()
            while result != None:
                # while loops through all the same values to make sure there are none that are equal
                while struct.unpack('>l', result[0])[0] == int(parsedq["price"][0][1]):
                    result = curs.next()
            
            # if int(result[0].decode("utf-8")) < int(parsedq["price"][0][1]):
            #     break
            # struct.unpack('>l', iterr[0])[0]
            # struct.pack('>l', key)
                print(struct.unpack('>l', result[0])[0])
                result = curs.next()
        else:
            # issue, 100 pulls 130 as the first value. Could hard code solution but not gonna hit up notes tonight
            # i thought it grabbed smallest or equal value, guess it does greater or equal? yolo
            # also not copying the code down tonight but it works for less than! <
            while result != None:
                print(struct.unpack('>l', result[0])[0])
                result = curs.prev()
#    curs = database.cursor()
    #    print(type(parsedq["date"][0]))
    #    result = curs.set_range(((str(parsedq["date"][0][1]).encode("utf-8"))))
    #    if len of pasredq '>=' is 2 then
    #        while date == date:
    #            if result[0].decode("utf-8") < (parsedq["date"][0][1]):
    #                break
    #            print(result[0].decode("utf-8"))
    #            result = curs.next()   
    #    while result != None:
    #        if result[0].decode("utf-8") < (parsedq["date"][0][1]):
    #            break
    #        print(result[0].decode("utf-8"))
    #        result = curs.next()


 #       curs = database.cursor()
 #       result = curs.set_range((str(parsedq["term"][0])).encode("utf-8"))
 #       while result != None:
            #if result[0].decode("utf-8") > (parsedq["term"][0]):
            #    break
 #           print(result[1].decode("utf-8"))
  #          result = curs.next()
main()
