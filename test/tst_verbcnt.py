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

def getSlot(parents, keys):
    ret = ''
    for k in keys:
        for p in parents:
            if not ret and k==p:
                ret = k
            #print(f"p={p} - k={k} - ret={ret}")
    if not ret:
        ret = 'OTH'
    return ret

ks = ['Aor','Cont','Ind','Nec','Can','Fut','Neg.Fut','Neg.Pt','Neg','Pot','Pt','OTH']
pdict = {}
odict = {}
for k in ks:
    odict[k] = ['',0]

p = processVerb(WRD)

for a in p:
    parents = prcSrc(a['src'])
    for q in parents:
        if q in pdict:
            pdict[q] = pdict[q] + 1
        else:
            pdict[q] = 1
    
    slot = getSlot(parents, ks)
    odict[slot][1] = odict[slot][1] + 1
    if len(odict[slot][0])==0 or len(odict[slot][0]) > len(a['infl']):
        odict[slot][0] = a['infl']

print("Parents' dict ::")
for k in sorted(pdict.keys()):
    print(f"{k}\t{pdict[k]}")
print("Representants' dict ::")
for k in sorted(odict.keys()):
    print(f"{k}\t{odict[k]}")
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
