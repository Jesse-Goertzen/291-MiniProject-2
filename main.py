import re

#d:a,c,l
def pdates(path, output="./output/pdate.txt"):
    with open(output, 'w') as d:
        with open(path, 'r') as r:
            for l in r:
                if re.search("<ad>(.*)</ad>", l) is not None:
                    date = re.search("<date>(.*)</date>", l).group(1)
                    aid  = re.search("<aid>(.*)</aid>", l).group(1)
                    cat  = re.search("<cat>(.*)</cat>", l).group(1).lower()
                    loc  = re.search("<loc>(.*)</loc>", l).group(1).lower()
                    d.write("%s:%s,%s,%s\n" % (date, aid, cat, loc))


# p:a,c,l
def prices(path, output="./output/prices.txt"):
    with open(output, 'w') as d:
        with open(path, 'r') as r:
            for l in r:
                if re.search("<ad>(.*)</ad>", l) is not None:
                    price = re.search("<price>(.*)</price>", l).group(1)
                    aid   = re.search("<aid>(.*)</aid>", l).group(1)
                    cat   = re.search("<cat>(.*)</cat>", l).group(1)
                    loc   = re.search("<loc>(.*)</loc>", l).group(1)
                    d.write("%s:%s,%s,%s\n" % (price, aid, cat, loc))


# a:ad
def ads(path, output="./output/ads.txt"):
    with open(output, 'w') as d:
        with open(path, 'r') as r:
            for l in r:
                if re.search("<ad>(.*)</ad>", l) is not None:
                    a = re.search("<aid>(.*)</aid>", l).group(1)
                    d.write("%s:%s" % (a, l))


def tests():
    inputs = ["./10records.txt", "./1000records.txt"]
    mods = ["10", "1000"]
    for i in range(len(inputs)):
        pdates(inputs[i], "./output/pdate"  + mods[i] + ".txt")
        prices(inputs[i], "./output/prices" + mods[i] + ".txt")
        ads(inputs[i], "./output/ads" + mods[i] + ".txt")

tests()