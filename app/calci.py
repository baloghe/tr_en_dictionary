#from app.classes.entry import Entry
from app.classes.group import Group
from app.constants import *

def rearrInflections(inEntries, inInflection2Head, inSharedInflections, inSharedGroups, inHead2Entry, inExactList):
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
                # if k=="ekmek":
                #     print(f"inSharedGroups :: {groupID} created with {k} ")
            else:
                inSharedGroups[groupID].append(k)
                # if k=="ekmek":
                #     print(f"inSharedGroups :: {k} added to {groupID}")
        else:
            #single head goes back to where it was
            inInflection2Head[k] = v
            # if k=="ekmek":
            #     print(f"inSharedGroups :: {k} single head goes back to where it was: {v} ")
    #remove items from inInflection2Head pointing to more than one Entry
    keysToDel = list(set(keysToDel))
    for k in keysToDel:
        rem = inInflection2Head.pop(k, None)
        # if k=="ekmek":
        #     print(f"remove items from inInflection2Head :: {k} removed ")

    # if "ekmek" in inInflection2Head:
    #     print(f"inInflection2Head contains ekmek")
    # if "ekmek" in inSharedInflections:
    #     print(f"inSharedInflections contains ekmek")
    # if "ekmek" in inSharedGroups:
    #     print(f"inSharedGroups contains ekmek")
    # if "ekmek" in inHead2Entry:
    #     print(f"inHead2Entry contains ekmek, no. entries: {len(list(inHead2Entry['ekmek'].items()))}")

    #identify groups
    simpleCnt = 0
    surplusCnt = 0
    groups = {}
    voidheads = []
    surplusGroups = []
    # Single (simple) groups from Head->Entry mapping
    for (h,e) in inHead2Entry.items():
        if len(list(e.items())) ==1:
            for (ent, gg) in e.items():
                origtext = inEntries[ent].getOrig()
                actgrp = {'id': h, 'head': '', 'page': [{'orig': origtext, 'inflGrps': gg, 'mbytp': inEntries[ent].getMeaningsByTypes()}]}
                ilist = []      # list of inflections
                exact = []      # exact spelling needed
                alterhead = ''  # alternative head in case original head is a shared one and has to be dropped
                for i in inEntries[ent].getInflectionGroup(gg):
                    # if i=="ekmek":
                    #     print(f"{i} found in inEntries['{ent}'].getInflectionGroup('{gg}') ")
                    if i not in inSharedInflections:
                        ilist.append(i)
                        # if i=="ekmek":
                        #     print(f"{h} found in inEntries['{ent}'].getInflectionGroup('{gg}') , {i} added to ilist")
                        if len(alterhead)==0 or len(alterhead) >= len(i):
                            alterhead = i
                        if i in inExactList:
                            exact.append(i)
                # if h=="ekmek":
                #     print(f"ilist({h})={ilist}")
                if not ilist:
                    # if h=="ekmek":
                    #     print(f"no ilist generated for {h} ")
                    if len(inEntries[ent].getInflections()) == 0:
                        actgrp['head'] = origtext
                        # if h=="ekmek":
                        #     print(f"no ilist -> {origtext} set as head for a group")
                    else:
                        voidheads.append('.'.join([origtext,h]))
                #elif h in ilist:
                elif h not in inSharedInflections:
                    actgrp['head'] = h
                    # if h=="ekmek":
                    #     print(f"{h} is not -> {h} set as head for a group")
                elif h in inSharedInflections:
                    actgrp['head'] = alterhead
                    # if h=="ekmek":
                    #     print(f"head {alterhead} chosen instead of {h} ::  ilist.len={len(ilist)}")
                #in case we found a head, it should be removed from the inflection list
                if actgrp['head'] and actgrp['head'] in ilist:
                    ilist.remove(actgrp['head'])
                    # if actgrp['head']=="ekmek":
                    #     print(f"{actgrp['head']} removed from ilist ")
                
                # more than <constants.MOBI_MAX_INFLECTIONS> inflections => create new group and limit ilist in <constants.MOBI_MAX_INFLECTIONS>
                if(len(ilist) > MOBI_MAX_INFLECTIONS):
                    ilist2 = ilist[MOBI_MAX_INFLECTIONS:]
                    ilist = ilist[:MOBI_MAX_INFLECTIONS]
                    head2 = ilist2[0]
                    for i in sorted(ilist2):
                        if len(head2)==0 or len(head2) >= len(i):
                            head2 = i
                    sg = Group(actgrp['id']+".2",head2,actgrp['page'],ilist2,exact)
                    surplusGroups.append(sg)
                    # print(f"New group created: ID={sg.getId()}, head={sg.getHead()}, ilist: len={len(sg.getInflections())}")
                    surplusCnt = surplusCnt + 1
                
                actgrp['infls'] = ilist
                #print(f"single {pg} -> {len(ilist)} inflections")
                groups[actgrp['id']] = Group(actgrp['id'],actgrp['head'],actgrp['page'],actgrp['infls'],exact)
                simpleCnt = simpleCnt+1
    
    # Shared groups from inSharedGroups
    sharedCnt = 0
    for gid in list(inSharedGroups.keys()):
        #print(f"gid: {gid}")
        ilist = inSharedGroups[gid] # list of inflections
        exact = []      # exact spelling needed
        potentries = {} # e.g. {'kar': ['Poss.Ind', 'OTH'], 'karın': ['Ind']}
        for i in ilist:
            heads = inSharedInflections[i]['heads']
            if i in inExactList:
                exact.append(i)
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
        
        # more than <constants.MOBI_MAX_INFLECTIONS> inflections => create new group and limit ilist in <constants.MOBI_MAX_INFLECTIONS>
        if(len(ilist) > MOBI_MAX_INFLECTIONS):
            ilist2 = ilist[MOBI_MAX_INFLECTIONS:]
            ilist = ilist[:MOBI_MAX_INFLECTIONS]
            head2 = ilist2[0]
            for i in sorted(ilist2):
                if len(head2)==0 or len(head2) >= len(i):
                    head2 = i
            sg = Group(gid+".2",head2,pages,ilist2,exact)
            surplusGroups.append(sg)
            # print(f"New group created: ID={sg.getId()}, head={sg.getHead()}, ilist: len={len(sg.getInflections())}")
            surplusCnt = surplusCnt + 1

        # create Group object:
        groups[gid] = Group(gid,head,pages,ilist,exact)
        sharedCnt = sharedCnt + 1
       
    sgnote = ""
    if(surplusCnt > 0):
        for g in surplusGroups:
            groups[g.getId()] = g
        sgnote = f" + added another {surplusCnt} by splitting long inflection lists"
    print(f"Groups created: {simpleCnt} simple and {sharedCnt} shared groups" + sgnote)
    if len(voidheads) > 0:
        print(f"{len(voidheads)} simple groups got entirely shared, e.g. {voidheads[0]}")

    return groups

def addHeadToInflection(inInflection2Head, infl, head):
    if infl in inInflection2Head.keys():
        inInflection2Head[infl].append(head)
        # if infl=="ekmek":
        #     print(f"addHeadToInflection :: new {infl} appended to {head}")
    else:
        inInflection2Head[infl] = [head]
        # if infl=="ekmek":
        #     print(f"addHeadToInflection :: new {infl} points to {head}")

def addEntryToHead(inHead2Entry, head, src, orig):
    if head in inHead2Entry:
        #print(inHead2Entry)
        #print(f"head: {head} , src: {src}, orig: {orig}")
        if orig in inHead2Entry[head]:
            if src not in inHead2Entry[head][orig]:
                inHead2Entry[head][orig].append(src)
                # if orig=="ekmek":
                #     print(f"addEntryToHead :: new {src} created under {head}")
        else:
            inHead2Entry[head][orig] = [src]
            # if head=="ekmek":
            #     print(f"addEntryToHead :: {src} added under {head}.{orig}")
    else:
        inHead2Entry[head] = {orig:[src]}
        # if head=="ekmek":
        #     print(f"addEntryToHead :: new head {head} created, orig={orig}, src={src}")

def updateExact(inExacts, infl):
    infl_coded = getCodedWord(infl)
    if infl_coded in inExacts:
        if infl not in inExacts[infl_coded]:
            inExacts[infl_coded].append(infl)
    else:
        inExacts[infl_coded] = [infl]

def calcInflections(inEntries):
    SHARED_INFLECTIONS = {}
    SHARED_GROUPS = {}
    INFLECTION_TO_HEAD = {}
    HEAD_TO_ENTRY = {}
    EXACT_INFLECTIONS = {}
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
            updateExact(EXACT_INFLECTIONS, t)
            # add inflections and heads
            alli = inEntries[o].getInflections()
            for tp,x in alli.items():
                #print(f"tp={tp} , alli[tp]={alli[tp]}")
                for k in alli[tp].keys():
                    head = alli[tp][k]["head"]
                    addEntryToHead(HEAD_TO_ENTRY,head,k,t)
                    for i in alli[tp][k]["infl"]:
                        addHeadToInflection(INFLECTION_TO_HEAD, i['infl'], head)
                        updateExact(EXACT_INFLECTIONS, i['infl'])
                    
    # filter EXACT_INFLECTIONS for conflicting words only
    EXACT_INFLECTIONS = {k: v for k, v in EXACT_INFLECTIONS.items() if len(v) > 1}
    EXACT_LIST = []
    for k, v in EXACT_INFLECTIONS.items():
        for i in v:
            if i not in EXACT_LIST:
                EXACT_LIST.append(i)
    print(f"Number of exact inflected forms: {len(EXACT_LIST)}")

    # distinct links and identify shared inflections
    outGroups = rearrInflections(inEntries, INFLECTION_TO_HEAD, SHARED_INFLECTIONS, SHARED_GROUPS, HEAD_TO_ENTRY, EXACT_LIST)
    return outGroups
