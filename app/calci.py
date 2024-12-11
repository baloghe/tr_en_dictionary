from app.classes.entry import Entry
from app.classes.group import Group

def rearrInflections(inEntries, inInflection2Head, inSharedInflections, inSharedGroups, inHead2Entry):
    keysToDel = []
    for (k,v) in inInflection2Head.items():
        v = list(set(v))                            #head='kızmış' pertains to different entries!
        hcnt = len(list(inHead2Entry[v[0]].keys())) #namely 'kız' and 'kızmak'
        if len(v) > 1 or hcnt > 1:
            #shared inflections to be moved to a different dict
            keysToDel.append(k)
            groupID = '#'.join(v)
            inSharedInflections[k] = {'heads': v , 'groupID': groupID}
            if groupID not in inSharedGroups.keys():
                inSharedGroups[groupID] = [k]
            else:
                inSharedGroups[groupID].append(k)
        else:
            #single head goes back to where it was
            inInflection2Head[k] = v
    #remove items from inInflection2Head pointing to more than one Entry
    keysToDel = list(set(keysToDel))
    for k in keysToDel:
        rem = inInflection2Head.pop(k, None)

    #identify groups
    simpleCnt = 0
    groups = {}
    voidheads = []
    # Single (simple) groups from Head->Entry mapping
    for (h,e) in inHead2Entry.items():
        if len(list(e.items())) ==1:
            for (ent, gg) in e.items():    
                origtext = inEntries[ent].getOrig()
                actgrp = {'id': h, 'head': '', 'page': [{'orig': origtext, 'inflGrps': gg, 'mbytp': inEntries[ent].getMeaningsByTypes()}]}
                ilist = []      # list of inflections
                alterhead = ''  # alternative head in case original head is a shared one and has to be dropped
                for i in inEntries[ent].getInflectionGroup(gg):
                    if i not in inSharedInflections:
                        ilist.append(i)
                        if len(alterhead)==0 or len(alterhead) >= len(i):
                            alterhead = i
                if not ilist:
                    if len(inEntries[ent].getInflections()) == 0:
                        actgrp['head'] = origtext
                    else:
                        voidheads.append('.'.join([origtext,h]))
                elif h in ilist:
                    actgrp['head'] = h
                else:
                    actgrp['head'] = alterhead
                #in case we found a head, it should be removed from the inflection list
                if actgrp['head'] and actgrp['head'] in ilist:
                    ilist.remove(actgrp['head'])
                actgrp['infls'] = ilist
                #print(f"single {pg} -> {len(ilist)} inflections")
                groups[actgrp['id']] = Group(actgrp['id'],actgrp['head'],actgrp['page'],actgrp['infls'])
                simpleCnt = simpleCnt+1
    
    # Shared groups from inSharedGroups
    sharedCnt = 0
    for gid in list(inSharedGroups.keys()):
        #print(f"gid: {gid}")
        ilist = inSharedGroups[gid] # list of inflections
        potentries = {} # e.g. {'kar': ['Poss.Ind', 'OTH'], 'karın': ['Ind']}
        for i in ilist:
            heads = inSharedInflections[i]['heads']
            #print(heads)
            for h in heads:
                es = inHead2Entry[h] #e.g. {'kar': ['Poss.Ind'], 'karın': ['Ind']}
                for (k,g) in es.items():
                    #should check if the link is reasonable: i should appear in the potential entry's inflection list!
                    chk = inEntries[k].getInflectionGroup(g)
                    if i in chk:
                        if k in list(potentries.keys()):
                            potentries[k] = potentries[k] + g
                        else:
                            potentries[k] = g
        # normalize potentries:
        for k in list(potentries.keys()):
            potentries[k] = list(set(potentries[k]))

        # render entry info into pages :: [{'orig': origtext, 'inflGrps': gg, 'mbytp': inEntries[ent].getMeaningsByTypes()}]
        pages = []
        for k in sorted(list(potentries.keys())):
            orig = inEntries[k].getOrig()
            gg = potentries[k]
            mbytp = inEntries[k].getMeaningsByTypes()
            pages.append({'orig': orig, 'inflGrps': gg, 'mbytp': mbytp})

        # select head
        head = ilist[0]
        for i in sorted(ilist):
            if len(head)==0 or len(head) >= len(i):
                head = i
        # remove head from inflection list
        if head:
            ilist.remove(head)

        # create Group object:
        groups[gid] = Group(gid,head,pages,ilist)
        sharedCnt = sharedCnt + 1

    print(f"Groups created: {simpleCnt} simple and {sharedCnt} shared groups")
    if len(voidheads) > 0:
        print(f"{len(voidheads)} simple groups got entirely shared, e.g. {voidheads[0]}")

    return groups

def addHeadToInflection(inInflection2Head, infl, head):
    if infl in inInflection2Head.keys():
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

def calcInflections(inEntries):
    SHARED_INFLECTIONS = {}
    SHARED_GROUPS = {}
    INFLECTION_TO_HEAD = {}
    HEAD_TO_ENTRY = {}
    for o in inEntries:
        # inEntries[o].calcInflections()
        try:
            inEntries[o].calcInflections()
        except:
            print(f"ERROR: no inflection could be calculated for Entry={o}")
        else:
            # add word itself as an inflection pointing to the Entry
            t = inEntries[o].getOrig()
            addHeadToInflection(INFLECTION_TO_HEAD,t,t)
            addEntryToHead(HEAD_TO_ENTRY,t,'OTH',t)
            # add inflections and heads
            alli = inEntries[o].getInflections()
            for tp,x in alli.items():
                #print(f"tp={tp} , alli[tp]={alli[tp]}")
                for k in alli[tp].keys():
                    head = alli[tp][k]["head"]
                    addEntryToHead(HEAD_TO_ENTRY,head,k,t)
                    for i in alli[tp][k]["infl"]:
                        addHeadToInflection(INFLECTION_TO_HEAD, i['infl'], head)
                    
    # distinct links and identify shared inflections
    outGroups = rearrInflections(inEntries, INFLECTION_TO_HEAD, SHARED_INFLECTIONS, SHARED_GROUPS, HEAD_TO_ENTRY)
    return outGroups
