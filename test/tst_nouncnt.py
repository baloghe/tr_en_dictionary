from app.prcnoun import processNoun
from app.constants import *

WRD = 'kar'

p = processNoun(WRD)

for c in p:
    print(f"{c} :: {p[c]["head"]} , {len(p[c]["infl"])}")


'''
Ind             ['karmış'     , 13]
OTH             ['kar'        , 30]
Pl              ['karlar'     , 31]
Pl.Ind          ['karlarmış'  , 13]
Pl.Poss         ['karlarım'   , 50]
Pl.Poss.Ind     ['karlarımmış', 70]
Poss            ['karım'      , 50]
Poss.Ind        ['karımmış'   , 70]
'''
