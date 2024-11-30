from app.prcverb import processVerb
from app.constants import *

WRD = 'gelmek'

p = processVerb(WRD)
g = getInflectionGroups(p,'verb')
for c in g:
    print(f"{c} :: {g[c]["head"]} , {len(g[c]["infl"])}")

'''
Aor     ['arar', 13]
Can     ['arayamam', 48]		drop -m  :: arayama
Cont    ['arıyor', 13]
Fut     ['arayacak', 112]
Ind     ['aramış', 13]
Nec     ['aramalı', 12]
Neg     ['aramam', 65]			drop -m  :: arama
Pot     ['arayabildi', 48]		drop -di :: arayabil
Pt      ['aradı', 100]
OTH     ['ara', 26]
'''