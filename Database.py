from bsddb3 import db
import struct

class Database():
    self.queries = dict()
    self.results = list()

    def __init__(self, queries):
        pass

    def _getKey(self, case):
        return str(struct.unpack('>l', case[0])[0])

    def _dateQuery(self):
        dbfile = "./indexes/da.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        for query in self.queries['date']:
            op, date = query.split()
            result = set()
            line = cur.set_range(struct.pack('>l', date))

            # Get passed the ads with date equal to the desired date to be greater than
            if op == '>':
                while self._getKey(line) == date:
                    line = cur.next()
            
            # Handles all operators, after the previous while loop considering the ">" case
            while eval(self._getKey(line) + query):
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

            self.results.add(result)

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
        line = cur.set_range(struct.pack('>l', date))
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


    def _priceQuery(self):
        dbfile = "./indexes/pr.idx"
        dbase = db.DB()
        dbase.open(dbfile, None, db.DB_BTREE)
        cur = dbase.cursor()

        for query in self.queries['price']:
            op, price = query.split()
            result = set()
            line = cur.set_range(struct.pack('>l', int(price)))

            # Get passed the ads with price equal to the desired price to be greater than
            if op == '>':
                while self._getKey(line) == price:
                    line = cur.next()
            
            # Handles all operators, after the previous while loop considering the ">" case            
            while eval(self._getKey(line) + query):
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

            self.results.add(result)

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
        end = cur.last()
        line = cur.first()
        while line != end:
            if self._getKey(line) in self.queries['term']:
                result.add(line[1])
            line = cur.next()
        
        self.results.add(result)
        dbase.close()
        

    def _checkPrices(self):
        prices = self.queries['price']
        g = list()
        l = list()
        corrected = list()
        for p in prices:
            op, price = p.split()
            price = (int) price
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
        

    def get(self, queries):
        self.queries = queries

        try:
            self._checkDates()
            self._checkPrices()
        except ValueError:
            # query is invalid, will return nothing -- pass for now? 
            pass

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
            self.queries['price'] = ['>= 0']
            self._priceQuery()

        if queries['term']:
            self._termQuery()

        return set.intersection(*self.results)

        