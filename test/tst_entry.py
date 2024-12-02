from app.classes.entry import Entry

from app.constants import *

tv = ["yakalamak", "to wash", "verb", None]
tn = ["yakma", "incineration", "noun", None]

def testRecord(record):
    print(f"orig :: {record}")
    e = Entry(record[0], record[1], record[2], record[3])
    e.calcInflections()
    g = e.getInflections()
    for p in g:
        print(p)
        for c in g[p]:
            print(f"{c} :: {g[p][c]["head"]} , {len(g[p][c]["infl"])}")
        
print("Test verb ::")
testRecord(tv)
print("Test noun ::")
testRecord(tn)
