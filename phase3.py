import bsddb3
import re
import Date

# I have a feeling this is gonna require a lot of regex....

class Parser():
    string = ""

    # returns: (operator {str}, date {date})
    # Use findall and have operator and date in one group, then do another regex to create a tuple for each date query 
    def _dateQuery(self):
        match = re.findall("date\s*(<|<=|>|>=|=)\s*(\d{4}/\d{2}/\d{2})", self.string)
        self.string = re.sub("date\s*(<|<=|>|>=|=)\s*\d{4}/\d{2}/\d{2}", "", self.string)
        return match if match else None


    # returns: (operator {str}, price {int})
    def _priceQuery(self):
        match = re.findall("price\s*(<|<=|>|>=|=)\s*(\d+)", self.string)
        self.string = re.sub("price\s*(<|<=|>|>=|=)\s*\d+", "", self.string)
        return match if match else None
    
    def _locationQuery(self):
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
        match = re.findall("[a-zA-Z0-9_-]*%?")
        self.string = re.sub("[a-zA-Z0-9_-]*%?", "", self.string)
        return match if match else None

    def parse(self, string):
        self.string = string
        queries = dict()
        queries["date"] = self._dateQuery()
        queries["prices"] = self._priceQuery()
        queries["loc"] = self._locQuery()
        queries["cat"] = self._catQuery()
        queries["terms"] = self._termQuery()
        for q in queries:
            if queries[q] is None:
                del queries[q]

        return queries