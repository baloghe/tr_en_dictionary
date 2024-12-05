from app.prcverb import processVerb
from app.constants import *

WRD = 'ısıtmak'

p = processVerb(WRD)

infl = {}

for c in p:
    print(f"{c} :: {p[c]["head"]} , {len(p[c]["infl"])}")
    for i in p[c]["infl"]:
        s = i["src"]
        if s in infl:
            infl[s] = infl[s] + 1
        else:
            infl[s] = 1
for g in sorted(list(infl.keys())):
    print(f"{g} :: {infl[g]}")

'''
Aor     ['gelir'     , 19]
Can     ['gelemem'   , 48]   -> delete last letter
Cont    ['geliyor'   , 13]
Fut     ['gelecek'   , 112]
Ind     ['gelmiş'    , 13]
Nec     ['gelmeli'   , 12]
Neg     ['gelme'     , 47]
Neg.Fut ['gelmeyecek', 112]
Neg.Pt  ['gelmedi'   , 106]
OTH     ['gel'       , 33]
Pot     ['gelebildi' , 54]  -> delete last 2 letters
Pt      ['geldi'     , 106]
'''
