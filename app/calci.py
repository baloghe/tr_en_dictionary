from app.classes.entry import Entry

def calcInflections(inEntries, inInflection2Entry):
    for o in inEntries:
        try:
            inEntries[o].calcInflections()
        except:
            print(f"ERROR: no inflection could be calculated for Entry={o}")
        else:
            # add word itself as an inflection pointing to the Entry
            t = inEntries[o].getOrig()
            if t in inInflection2Entry:
                inInflection2Entry[t].append(t)
            else:
                inInflection2Entry[t] = [t]
            # add inflections
            for i,s in inEntries[o].getInflections().items():
                if i in inInflection2Entry:
                    inInflection2Entry[i].append(t)
                else:
                    inInflection2Entry[i] = [t]
                    
    # distinct links        
    for i in inInflection2Entry:
        inInflection2Entry[i] = list(set(inInflection2Entry[i]))
        