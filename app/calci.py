from app.classes.entry import Entry

def addHeadToInflection(inInflection2Head, infl, head):
    if infl in inInflection2Head:
        inInflection2Head[infl].append(head)
    else:
        inInflection2Head[infl] = [head]

def addEntryToHead(inHead2Entry, head, src, orig):
    if head in inHead2Entry:
        #print(inHead2Entry)
        #print(f"head: {head} , src: {src}, orig: {orig}")
        if orig in inHead2Entry[head]:
            if src not in inHead2Entry[head][orig]:
                inHead2Entry[head][orig].append(src)
        else:
            inHead2Entry[head][orig] = [src]
    else:
        inHead2Entry[head] = {orig:[src]}

def calcInflections(inEntries, inInflection2Head, inHead2Entry):
    for o in inEntries:
        try:
            inEntries[o].calcInflections()
        except:
            print(f"ERROR: no inflection could be calculated for Entry={o}")
        else:
            # add word itself as an inflection pointing to the Entry
            t = inEntries[o].getOrig()
            addHeadToInflection(inInflection2Head,t,t)
            addEntryToHead(inHead2Entry,t,'OTH',t)
            # add inflections and heads
            alli = inEntries[o].getInflections()
            for tp,x in alli.items():
                #print(f"tp={tp} , alli[tp]={alli[tp]}")
                for k in alli[tp].keys():
                    head = alli[tp][k]["head"]
                    addEntryToHead(inHead2Entry,head,k,t)
                    for i in alli[tp][k]["infl"]:
                        addHeadToInflection(inInflection2Head, i["infl"], head)
                    
    # distinct links        
    for i in inInflection2Head:
        inInflection2Head[i] = list(set(inInflection2Head[i]))
        