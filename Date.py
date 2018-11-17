
class Date():
    def __init__(self, string):
        self.date = string
        self.year, self.month, self.day = string.split('/')

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __le__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day <= other.day:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __gt__(self, other):
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day > other.day:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __ge__(self, other):
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
            elif self.month == other.month:
                if self.day >= other.day:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return self.date != other.date

    def __repr__(self):
        return str(self.date)

    def __str__(self):
        return str(self.date)