from app.prcverb import processVerb

WRD = 'gelmek'

def prcSrc(src):
    s = src.split('.')
    ret = []
    for i in s:
        if ret:
            ret.append(ret[len(ret)-1] + '.' + i)
        else:
            ret.append(i)
    return ret

def getFirstSrc(src):
    s = src.split('.')
    return s[0]

ks = ['Aor','Cont','Ind','Nec','Can','Fut','Neg','Pot','Pt','OTH']
pdict = {}
odict = {}
for k in ks:
    odict[k] = ['',0]

p = processVerb(WRD)

for a in p:
    parents = prcSrc(a['src'])
    first = getFirstSrc(a['src'])
    for q in parents:
        if q in pdict:
            pdict[q] = pdict[q] + 1
        else:
            pdict[q] = 1
    
    if first not in odict:
        first = 'OTH'
    odict[first][1] = odict[first][1] + 1
    if len(odict[first][0])==0 or len(odict[first][0]) > len(a['infl']):
        odict[first][0] = a['infl']

print("Parents' dict ::")
for k in sorted(pdict.keys()):
    print(f"{k}\t{pdict[k]}")
print("Representants' dict ::")
for k in sorted(odict.keys()):
    print(f"{k}\t{odict[k]}")
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