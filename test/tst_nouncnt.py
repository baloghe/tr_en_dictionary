from app.prcnoun import processNoun

WRD = 'kar'

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

ks = ['Ind','Pl.Ind','Pl.Poss.Ind','Pl.Poss','Pl','Poss.Ind','Poss','OTH']
pdict = {}
odict = {}
for k in ks:
    odict[k] = ['',0]

p = processNoun(WRD)
print(f"first: {p[0]}")
print(f"missing src: {list(filter(lambda x: 'src' not in x or x['src']==None, p))}")

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
Ind             ['karmış'     , 13]
OTH             ['kar'        , 30]
Pl              ['karlar'     , 31]
Pl.Ind          ['karlarmış'  , 13]
Pl.Poss         ['karlarım'   , 50]
Pl.Poss.Ind     ['karlarımmış', 70]
Poss            ['karım'      , 50]
Poss.Ind        ['karımmış'   , 70]
'''