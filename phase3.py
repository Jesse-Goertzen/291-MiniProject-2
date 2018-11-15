import bsddb3
import re

# I have a feeling this is gonna require a lot of regex....

class Parser():

    def _dateQuery(self, string):
        match = re.search("date\s*(<|<=|>|>=|=)\s*(\d{4}/\d{2}/\d{2})", string)
        if match:
            return match.group(1)
        else:
            return None 

    def _priceQuery(self, string):
        match = re.search("price\s*(<|<=|>|>=|=)\s*(\d+)", string)
        if match:
            return match.group(1)
        else:
            return None
    
    def _locationQuery(self, string):
        match = re.search("location\s*=\s*([0-9a-zA-Z_-])", string)
        if match:
            return match.group(1).lower()
        else:
            return None
    
    def _catQuery(self, string):
        match = re.search("cat\s*=\s*([0-9a-zA-Z_-])", string)
        if match:
            return match.group(1).lower()
        else:
            return None

    def _termQuery(self, string):
        #not implemented
        return None

    def _subQueries(self, string):
        queries = dict()
        match = re.search("")