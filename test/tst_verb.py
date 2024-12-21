from app.prcverb import processVerb

#for w in ['çıkarmak', 'edebileceğim', 'aramak', 'kaçmak', 'hatırlamak']:
for w in ['kalmak']:
    pn = processVerb(w)
    #print(f"{w} -> {pn}")
    tofind = 'kalırım'
    srcTofind = 'Aor'
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
    print(f"{srcFound} -> {srcFound}")
