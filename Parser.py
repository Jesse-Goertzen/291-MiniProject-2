import re

class Parser():
    string = ""

    def __init__(self):
        pass

    # returns: (operator {str}, date {date})
    # Use findall and have operator and date in one group, then do another regex to create a tuple for each date query 
    def _dateQuery(self):
        match = re.findall("date\s*(<|<=|>|>=|=)\s*(\d{4}/\d{2}/\d{2})", self.string)
        self.string = re.sub("date\s*(<|<=|>|>=|=)\s*\d{4}/\d{2}/\d{2}", "", self.string)
        if match:
            ret = []
            for s in match:
                if s[0] == '=':
                    s = ("==", s[1])  
                ret.append(' '.join(str(c) for c in s))
            return ret
        else:
            return []

    # returns: (operator {str}, price {int})
    def _priceQuery(self):
        match = re.findall("price\s*(<|<=|>|>=|=)\s*(\d+)", self.string)
        self.string = re.sub("price\s*(<|<=|>|>=|=)\s*\d+", "", self.string)
        if match:
            ret = []
            for s in match:
                if s[0] == '=':
                    s = ("==", s[1])  
                ret.append(' '.join(str(c) for c in s))
            return ret
        else:
            return []
    
    def _locQuery(self):
        match = re.findall("location\s*=\s*([0-9a-zA-Z_-]+)", self.string)
        self.string = re.sub("location\s*=\s*[0-9a-zA-Z_-]+", "", self.string)
        return match if match else []
    
    def _catQuery(self):
        match = re.findall("cat\s*=\s*([0-9a-zA-Z_-]+)", self.string)
        self.string = re.sub("cat\s*=\s*[0-9a-zA-Z_-]+", "", self.string)
        return match if match else []

    # Maybe have the other methods return the query with the sub query removed,
    # then after all other methods are called the only thing left is a term query?
    def _termQuery(self):
        match = re.findall("[a-zA-Z0-9_-]+%?", self.string)
        self.string = re.sub("[a-zA-Z0-9_-]+%?", "", self.string)
        return match if match else []

    def parse(self, string):
        self.string = string
        queries = dict()
        queries["date"] = self._dateQuery()
        queries["price"] = self._priceQuery()
        queries["loc"] = self._locQuery()
        queries["cat"] = self._catQuery()
        queries["term"] = self._termQuery()
        # q = {k:v for k,v in queries.items() if v is not None}
        return queries

if __name__ == "__main__":
    p = Parser()
    qs = [
        "camera",
        "camera%",
        "date        <= 2018/11/05",
        "date           >      2018/11/05",
        "price = 20",
        "price >=         20",
        "location=       edmonton     date=2018/11/07",
        "cat=art-collectibles       camera",
        "camera date>=           2018/11/05              date<=2018/11/07 price > 20                 price < 40"
    ]

    for q in qs:
        print(p.parse(q))
