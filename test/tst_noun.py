from app.prcnoun import processNoun

for w in ['saç']:
    pn = processNoun(w)
    #print(f"{w} -> {pn}")
    tofind = 'saçım'
    srcTofind = 'Gen'
    found = []
    srcFound = []
    
    for g in pn.keys():
        for i in pn[g]['infl']:
            #print(i)
            if tofind:
                if i['infl'] == tofind:
                    found.append(i)
            if srcTofind:
                if i['src'] == srcTofind:
                    srcFound.append(i)
    print(f"{tofind} -> {found}")
    print(f"{srcTofind} -> {srcFound}")
