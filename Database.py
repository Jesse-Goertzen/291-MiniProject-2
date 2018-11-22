from bsddb3 import db
from tabulate import tabulate
from Parser import Parser
from textwrap import fill
import struct
import re

debug = True

class Database():
    queries = dict()
    results = list()
    p = Parser()

    def __init__(self):
        self.output = False # Brief output by default

    def _dateQuery(self):
        dbfile = "./indexes/da.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        for query in self.queries['date']:
            op, date = query.split()
            result = set()
            line = cur.set_range(date.encode())
            line = (line[0].decode(), line[1].decode())

            # Get passed the ads with date equal to the desired date to be greater than
            if op == '>':
                while line[0] == date:
                    line = cur.next()
                    if line is None:
                        break #this is probs an issue if you try and find greater than last date
                    else: 
                        line = (line[0].decode(), line[1].decode())
            if op == '<':
                line = cur.prev()
                if line is None:
                    break
                else:
                    line = (line[0].decode(), line[1].decode())
            
            # there absolutely has to be a better way to do this...but it works?
            # basically cur.set_range() will put us at the first matching date, but we needa look at all
            # the dates that are equal to the requriment too, not just the first one then go backwards
            # so this if: {...} puts the cursor at the last date equal to the requirement
            if op == '<=':  
                line = cur.next()
                if line is None:
                    line = cur.prev()
                    line = (line[0].decode(), line[1].decode())
                    break
                else:
                    line = (line[0].decode(), line[1].decode())
                while line[0] == date:
                    line = cur.next()
                    if line is None:
                        line = cur.prev()
                        line = (line[0].decode(), line[1].decode())
                        break
                    else:
                        line = (line[0].decode(), line[1].decode())
                
                line = cur.prev()
                line = (line[0].decode(), line[1].decode())
                
            # Handles all operators, after the previous while loop considering the ">" case
            while eval("'%s' %s '%s'" % (line[0], op, date)):
                aid, cat, loc = line[1].split(',')

                # Add the aid to result set if no location or catagory is specified,
                # or there are no catagories and the location matches
                # or there are no locations and the catagory matches
                # or both are specified and match
                if self.numLoc == 0 and self.numCat == 0:
                    result.add(aid)
                elif (self.numLoc > 0 and loc in self.queries['loc']) and self.numCat == 0:
                    result.add(aid)
                elif (self.numCat > 0 and cat in self.queries['cat']) and self.numLoc == 0:
                    result.add(aid)
                elif ((self.numCat > 0 and cat in self.queries['cat']) 
                        and (self.numLoc > 0 and loc in self.queries['loc'])):
                    result.add(aid)
                else:
                    pass

                # TODO: Figure out if we need to handle == any differently
                if op == '>' or op == '>=' or op == '==':
                    line = cur.next()
                else: # < or <=
                    line = cur.prev()

                if line is None:
                    break
                else:
                    line = (line[0].decode(), line[1].decode())

            self.results.append(result)

        dbase.close()


    def _betweenDates(self):
        dbfile = "./indexes/da.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        lower, upper = '', ''        
        for d in self.queries['date']:
            if d.split()[0] == '>=' or d.split()[0] == '>':
                lower = d
            else:
                upper = d
        
        result = set()
        lop, ldate = lower.split()
        line = cur.set_range(struct.pack('>l', ldate))
        while eval(self._getKey(line) + lower + 'and' + self._getKey(line) + upper):
            aid, cat, loc = line[1].split(',')

            # Add the aid to result set if no location or catagory is specified,
            # or there are no catagories and the location matches
            # or there are no locations and the catagory matches
            # or both are specified and match
            if self.numLoc == 0 and self.numCat == 0:
                result.add(aid)
            elif (self.numLoc > 0 and loc in self.queries['loc']) and self.numCat == 0:
                result.add(aid)
            elif (self.numCat > 0 and cat in self.queries['cat']) and self.numLoc == 0:
                result.add(aid)
            elif ((self.numCat > 0 and cat in self.queries['cat']) 
                    and (self.numLoc > 0 and loc in self.queries['loc'])):
                result.add(aid)
            else:
                pass
            
            line = cur.next()

        self.results.append(result)
        dbase.close()

    # TODO: Unfuck this. For some reason the cursor is putting us at random spots. Obviously something 
    #       nasty with the keys... but I can't be assed to figure it out. Everything else works flawlessly (jynx)
    def _priceQuery(self):
        dbfile = "./indexes/pr.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        for query in self.queries['price']:
            op, price = query.split()
            result = set()
            line = cur.set_range(price.encode())
            line = (line[0].decode(), line[1].decode())

            # Get passed the ads with price equal to the desired price to be greater than
            if op == '>':
                while line[0].lstrip() == price:
                    line = cur.next()
                    if line is None:
                        break
                    else:
                        line = (line[0].decode(), line[1].decode())

            if op == '<':
                line = cur.prev()
                if line is None:
                    return
                else:
                    line = (line[0].decode(), line[1].decode())

            # there absolutely has to be a better way to do this...but it works?
            # basically cur.set_range() will put us at the first matching date, but we needa look at all
            # the dates that are equal to the requriment too, not just the first one then go backwards
            # so this if: {...} puts the cursor at the last date equal to the requirement
            if op == '<=':  
                line = cur.next()
                if line is None:
                    line = cur.prev()
                    line = (line[0].decode(), line[1].decode())
                    break
                else:
                    line = (line[0].decode(), line[1].decode())
            
                while line[0] == price:
                    line = cur.next()
                    if line is None:
                        line = cur.prev()
                        line = (line[0].decode(), line[1].decode())
                        break
                    else:
                        line = (line[0].decode(), line[1].decode())
                
                line = cur.prev()
                line = (line[0].decode(), line[1].decode())
            
            # Handles all operators, after the previous while loop considering the ">" case            
            while eval("%s %s %s" % (line[0].lstrip(), op, price)):
                aid, cat, loc = line[1].split(',')

                # Add the aid to result set if no location or catagory is specified,
                # or there are no catagories and the location matches
                # or there are no locations and the catagory matches
                # or both are specified and match
                if self.numLoc == 0 and self.numCat == 0:
                    result.add(aid)
                elif (self.numLoc > 0 and loc in self.queries['loc']) and self.numCat == 0:
                    result.add(aid)
                elif (self.numCat > 0 and cat in self.queries['cat']) and self.numLoc == 0:
                    result.add(aid)
                elif ((self.numCat > 0 and cat in self.queries['cat']) 
                        and (self.numLoc > 0 and loc in self.queries['loc'])):
                    result.add(aid)
                else:
                    pass

                if op == '>' or op == '>=' or op == '==':
                    line = cur.next()
                else: # < or <=
                    line = cur.prev()

                if line is None:
                    break
                else:
                    line = (line[0].decode(), line[1].decode())

            self.results.append(result)

        dbase.close()


    def _betweenPrices(self):
        dbfile = "./indexes/pr.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        lower, upper = '', ''
        for p in self.queries['price']:
            if p.split()[0] == '>=' or p.split()[0] == '>':
                lower = p
            else:
                upper = p

        result = set()
        lop, lprice = lower.split()
        line = cur.set_range(struct.pack(int(lprice)))
        if lop == '>':
            while self._getKey(line) == lprice:
                line = cur.next()
        
        while eval(self._getKey(line) + lower + ' and ' + self._getKey(line) + upper):
            aid, cat, loc = line[1].split(',')

            # Add the aid to result set if no location or catagory is specified,
            # or there are no catagories and the location matches
            # or there are no locations and the catagory matches
            # or both are specified and match
            if self.numLoc == 0 and self.numCat == 0:
                result.add(aid)
            elif (self.numLoc > 0 and loc in self.queries['loc']) and self.numCat == 0:
                result.add(aid)
            elif (self.numCat > 0 and cat in self.queries['cat']) and self.numLoc == 0:
                result.add(aid)
            elif ((self.numCat > 0 and cat in self.queries['cat']) 
                    and (self.numLoc > 0 and loc in self.queries['loc'])):
                result.add(aid)
            else:
                pass
            
            line = cur.next()

        self.results.append(result)
        dbase.close()


    def _termQuery(self):
        dbfile = "./indexes/te.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        result = set()
        line = cur.first()
        line = (line[0].decode(), line[1].decode())
        while True:
            if line[0] in self.queries['term']:
                result.add(line[1])
            line = cur.next()
            if line is None:
                break
            else:
                line = (line[0].decode(), line[1].decode())
        
        self.results.append(result)
        dbase.close()
        

    def _checkPrices(self):
        prices = self.queries['price']
        g = list()
        l = list()
        corrected = list()
        for p in prices:
            op, price = p.split()
            price = int(price)
            if op == '==':
                if len(prices) > 1:
                    raise ValueError # Cant have a price equal to something, AND have other conditions on it
                self.queries['price'] = [p]
                return
            elif op == '>=' or op == '>':
                g.append((price, p))
            else:
                l.append((price, p))
        g.sort(key=lambda x : x[0])
        l.sort(key=lambda x : x[0])
        try:
            if l[-1][0] < g[0][0]:
                # No results? impossible price range. e.g. price < 15 and price > 20
                # Not sure what to do, need to make a quick impossible query throw or something.
                raise ValueError
        except IndexError:
            pass
        if g:
            corrected.append(g[-1][1])
        if l:
            corrected.append(l[0][1])
        if corrected:
            self.queries['price'] = corrected


    def _checkDates(self):
        dates = self.queries['date']
        g = list()
        l = list()
        corrected = list()
        for d in dates:
            op, date = d.split()
            if op == '==':
                if len(dates) > 1:
                    raise ValueError # Cant have a date equal to something, AND have other conditions on it
                self.queries['date'] = [p]
                return
            elif op == '>=' or op == '>':
                g.append((date, d))
            else:
                l.append((date, d))
        g.sort(key=lambda x : x[0])
        l.sort(key=lambda x : x[0])
        try:
            if l[-1][0] < g[0][0]:
                # No results? impossible date range. e.g. date < 2018/11/01 and date > 2018/11/02
                # Not sure what to do, need to make a quick impossible query throw or something.
                raise ValueError
        except IndexError:
            pass
        if g:
            corrected.append(g[-1][1])
        if l:
            corrected.append(l[0][1])
        if corrected:
            self.queries['date'] = corrected
        

    def _adQuery(self, ads):
        dbfile = "./indexes/ad.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_HASH)
        cur = dbase.cursor()

        result = list()
        line = cur.first()
        line = (line[0].decode(), line[1].decode())
        while True:
            if line[0] in ads:
                data = line[1]
                if self.output: # full output
                    r = list(re.search("<aid>(.*)</aid><date>(.*)</date><loc>(.*)</loc><cat>(.*)</cat><ti>(.*)</ti><desc>(.*)</desc><price>(.*)</price>", data).groups())
                    r[4], r[5] = fill(r[4], 32), fill(r[5], 48)
                    result.append(r)
                else:
                    r = list(re.search("<aid>(.*)</aid>.*<ti>(.*)</ti>", data).groups())
                    r[1] = fill(r[1], 120)
                    result.append(r)

            line = cur.next()
            if line is None:
                break
            else:
                line = (line[0].decode(), line[1].decode())
            

        return result

    def get(self, string):
        self.results = []
        self.queries = self.p.parse(string)

        self._checkDates()
        self._checkPrices()

        self.numLoc = len(self.queries['loc'])
        self.numCat = len(self.queries['cat'])
        numPrice    = len(self.queries['price'])
        numDate     = len(self.queries['date'])

        if numPrice > 0 and numDate == 0:
            if numPrice == 2:
                self._betweenPrices()
            else:
                self._priceQuery()
        elif numDate > 0 and numPrice == 0:
            if numDate == 2:
                self._betweenDates()
            else:
                self._dateQuery()
        elif numDate > 0 and numPrice > 0:
            if numDate == 2:
                self._betweenDates
            else:   
                self._dateQuery()
            if numPrice == 2:
                self._betweenPrices()
            else:
                self._priceQuery()
        else:
            self.queries['date'] = ['>= 0000/00/00']
            self._dateQuery()

        if self.queries['term']:
            self._termQuery()

        result = self._adQuery(set.intersection(*self.results))

        if self.output:
            print(tabulate(result, headers=['Ad ID', 'Date', 'Location', 'Catagory', 'Title', 'Description', 'Price'], tablefmt="fancy_grid"))
            print("Number of Results = " + len(result))
        else:
            print(tabulate(result, headers=['Ad ID', 'Title'], tablefmt="fancy_grid"))
            print("Number of Results = %d" % len(result))
    
    # Set output type, returns the status of the update. e.g. 'False' if user doesnt enter brief or full, true otherwise
    def setOutput(self, flag):
        self.output = flag
