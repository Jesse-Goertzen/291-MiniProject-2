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

    with open(output, 'r+') as f:
        lines = sorted(set(f.readlines()))
        f.seek(0)
        f.writelines(lines)
        f.truncate()

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
    
    with open(output, 'r+') as f:
        lines = sorted(set(f.readlines()))
        f.seek(0)
        f.writelines(lines)
        f.truncate()


# a:ad
def ads(path, output="./output/ads.txt"):
    with open(output, 'w') as d:
        with open(path, 'r') as r:
            for l in r:
                if re.search("<ad>(.*)</ad>", l) is not None:
                    a = re.search("<aid>(.*)</aid>", l).group(1)
                    d.write("%s:%s" % (a, l))

    with open(output, 'r+') as f:
        lines = sorted(set(f.readlines()))
        f.seek(0)
        f.writelines(lines)
        f.truncate()

def terms(path, output="./output/terms.txt"):
    with open(path, 'r') as f:
        with open(output, 'w') as o:
            for line in f:
                if re.search("<ad>(.*)</ad>", line) is not None:
                    aid = re.search("<aid>(.*)</aid>", line).group(1)
                    term1 = re.sub("[^0-9a-zA-Z-_]", " ", re.sub("&.*?;", "", re.sub("&amp;", " ", re.search("<ti>(.*)</ti>", line).group(1).lower()))).split()
                    term2 = re.sub("[^0-9a-zA-Z-_]", " ", re.sub("&.*?;", "", re.sub("&amp;", " ", re.search("<desc>(.*)</desc>", line).group(1).lower()))).split()
                    for term in term1:
                        term = re.search("([0-9a-zA-Z-_]+)", term)
                        if term is not None:
                            if len(term.group(1)) > 2:
                                o.write(term.group(1) + ":" + aid + '\n')
                    for term in term2:
                        term = re.search("([0-9a-zA-Z-_]+)", term)
                        if term is not None:
                            if len(term.group(1)) > 2:
                                o.write(term.group(1) + ":" + aid + '\n')

# Now we can simply do: {from phase1 import init} then call to create all files based on the path to whatever records we're using
def init(path):
    terms(path)
    pdates(path)
    prices(path)
    ads(path)

def tests():
    inputs = ["./10records.txt", "./1000records.txt"]
    mods = ["10", "1000"]
    for i in range(len(inputs)):
        pdates(inputs[i], "./output/pdate"  + mods[i] + ".txt")
        prices(inputs[i], "./output/prices" + mods[i] + ".txt")
        ads(inputs[i], "./output/ads" + mods[i] + ".txt")
        terms(inputs[i], "./output/terms" + mods[i] + ".txt")

