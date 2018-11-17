import bsddb3
import re
from Date import Date

# I have a feeling this is gonna require a lot of regex....

class Parser():
    string = ""

    def __init__(self):
        pass

    # returns: (operator {str}, date {date})
    # Use findall and have operator and date in one group, then do another regex to create a tuple for each date query 
    def _dateQuery(self):
        match = re.findall("date\s*(<|<=|>|>=|=)\s*(\d{4}/\d{2}/\d{2})", self.string)
        self.string = re.sub("date\s*(<|<=|>|>=|=)\s*\d{4}/\d{2}/\d{2}", "", self.string)
        for i, m in enumerate(match):
            match[i] = (m[0], Date(m[1]))
        if len(match) == 1:
            match = match[0]
        return match if match else None


    # returns: (operator {str}, price {int})
    def _priceQuery(self):
        match = re.findall("price\s*(<|<=|>|>=|=)\s*(\d+)", self.string)
        self.string = re.sub("price\s*(<|<=|>|>=|=)\s*\d+", "", self.string)
        if len(match) == 1:
            match = match[0]
        return match if match else None
    
    def _locQuery(self):
        match = re.search("location\s*=\s*([0-9a-zA-Z_-]+)", self.string)
        self.string = re.sub("location\s*=\s*[0-9a-zA-Z_-]+", "", self.string)
        return match.group(1).lower() if match else None
    
    def _catQuery(self):
        match = re.search("cat\s*=\s*([0-9a-zA-Z_-]+)", self.string)
        self.string = re.sub("cat\s*=\s*[0-9a-zA-Z_-]+", "", self.string)
        return match.group(1).lower() if match else None

    # Maybe have the other methods return the query with the sub query removed,
    # then after all other methods are called the only thing left is a term query?
    def _termQuery(self):
        match = re.findall("[a-zA-Z0-9_-]+%?", self.string)
        self.string = re.sub("[a-zA-Z0-9_-]+%?", "", self.string)
        if len(match) == 1:
            match = match[0]
        return match if match else None

    def parse(self, string):
        self.string = string
        queries = dict()
        queries["date"] = self._dateQuery()
        queries["price"] = self._priceQuery()
        queries["loc"] = self._locQuery()
        queries["cat"] = self._catQuery()
        queries["term"] = self._termQuery()
        q = {k:v for k,v in queries.items() if v is not None}
        return q

if __name__ == "__main__":
    p = Parser()
    qs = [
        "camera",
        "camera%",
        "date        <= 2018/11/05",
        "date           >      2018/11/05",
        "price < 20",
        "price >=         20",
        "location=       edmonton     date=2018/11/07",
        "cat=art-collectibles       camera",
        "camera date>=           2018/11/05              date<=2018/11/07 price > 20                 price < 40"
    ]

    for q in qs:
        print(p.parse(q))