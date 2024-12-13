from app.classes.entry import Entry
from app.calci import calcInflections

from app.constants import *

tv = ["yakalamak", "to wash", "verb", None]
tn = ["yakma", "incineration", "noun", None]
tadj = ["aksi", "opposite", "adj", None]
tadv = ["aksine", "on the contrary", "adv", None]

ENTRIES = {}

def createEntry(record):
    print(f"orig :: {record}")
    e = Entry(record[0], record[1], record[2], record[3])
    e.calcInflections()
    g = e.getInflections()
    print("createEntry ::")
    for p in g:
        print(p)
        for c in g[p]:
            print(f"{c} :: {g[p][c]["head"]} , {len(g[p][c]["infl"])}")
    return e

def testCalcI(record):
    e = createEntry(record)
    ENTRIES = {}
    ENTRIES[e.getOrig()] = e
    #print(e)
    grps = calcInflections(ENTRIES)
    for g in grps.keys():
        print(f"{g} -> {len(grps[g].getInflections())}, valid: {grps[g].isValid()}")


print("Test verb ::")
testCalcI(tv)

print("Test noun ::")
testCalcI(tn)

print("Test adjective ::")
testCalcI(tadj)

print("Test adverb ::")
testCalcI(tadv)
