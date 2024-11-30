from lxml import etree

from app.classes.meaning import Meaning
from app.classes.entry import Entry

NSMAP = {'idx':'www.mobipocket.com/idx' , 'mbp':'www.mobipocket.com/pagebreak' , 'xlink':'http://www.w3.org/1999/xlink'}

def writeXmlHeader():
    html = etree.Element("html", nsmap=NSMAP)
    body = etree.SubElement(html, "body")
    fs = etree.SubElement(body, "{www.mobipocket.com/pagebreak}frameset", nsmap={'mbp':NSMAP['mbp']})
    slave = etree.SubElement(fs, "{www.mobipocket.com/pagebreak}slave-frame", nsmap={'mbp':NSMAP['mbp']})
    for (k,v) in {"display":"bottom" , "device":"all" , "breadth":"auto" , "leftmargin":"0" , "rightmargin":"0" , "bottommargin":"0" , "topmargin":"0"}.items():
        slave.set(k,v)
    
    div = etree.SubElement(slave, "div")
    for (k,v) in {"align":"center" , "bgcolor":"yellow"}.items():
        div.set(k,v)
        
    a = etree.SubElement(div, "a")
    a.set("onclick","index_search()")
    a.text = "Dictionary Search"
    return (html,fs);
    
def writePB(where):
    pb = etree.SubElement(where, "{www.mobipocket.com/pagebreak}pagebreak", nsmap={'mbp':NSMAP['mbp']})
    pb.text = ''

def writeOriginal(orth, origtext, grps=None, grpMap=None, head=None):
    porig = etree.SubElement(orth,"p")
    borig = etree.SubElement(porig,"b")
    borig.text = origtext
    if grps:
        ig = []
        for g in grps:
            if g != 'OTH':
                r = '.'.join(map(lambda x: grpMap[x], g.split('.')))
                ig.append(r)
        if(ig):
            iorig = etree.SubElement(porig,"i")
            iorig.text = ' + ' + ' or '.join(ig) + ' = ' + head
            

def writeMeanings(orth, wt, wtMap):
    for tp in sorted(wt):
        ptype = etree.SubElement(orth,"p")
        itype = etree.SubElement(ptype,"i")
        tperror = False
        if (tp):
            itype.text = wtMap[tp]
        else:
            tperror = True
            
        etree.SubElement(ptype,"br")
        #print(f"{origtext} -> tp: {tp}")
        for m in wt[tp]:
            span = etree.SubElement(ptype,"span")
            str = '  ' + m.getMeaning()
            ex = m.getExamples()
            if ex:
                str = str + ':'
                span.text = str
                for e in ex:
                    if len(e) > 0:
                        etree.SubElement(ptype,"br")
                        iex = etree.SubElement(ptype,"i")
                        iex.text = '    ' + e
            else:
                span.text = str
            etree.SubElement(ptype,"br")
            #print missing word type error on first meaning only
            if tperror:
                print(f"{m.getMeaning()} -> missing word type")
                tperror = False

def writeComplexMeanings(orth, wt, wtMap):
    for tp in sorted(wt):
        ptype = etree.SubElement(orth,"p")
        itype = etree.SubElement(ptype,"i")
        itype.text = wtMap[tp]
        etree.SubElement(ptype,"br")
        #print(f"{origtext} -> tp: {tp}")
        for m in wt[tp]:
            span = etree.SubElement(ptype,"span")
            if m['inflected']:
                str = '  ' + m['orig'] + '+' + m['inflected'] + ' :: ' + m['meaning'].getMeaning()
            else:
                str = '  ' + m['orig'] + ' (uninflected) :: ' + m['meaning'].getMeaning()
            ex = m['meaning'].getExamples()
            if ex:
                str = str + ':'
                span.text = str
                for e in ex:
                    if len(e) > 0:
                        etree.SubElement(ptype,"br")
                        iex = etree.SubElement(ptype,"i")
                        iex.text = '    ' + e
                        #print(f"e={e}, len(e)={len(e)}")
            else:
                span.text = str
            etree.SubElement(ptype,"br")

def writeInflections(where, sInfl):
    if len(sInfl) > 0:
        infl = etree.SubElement(where, "{www.mobipocket.com/idx}infl", nsmap={'idx':NSMAP['idx']})
        clr_infl = list(set(sInfl))
        if len(clr_infl) > 255:
            print(f"WARNING: entry {origtext}, head={head} has {len(clr_infl)} inflections! Truncated to 255")
            clr_infl = clr_infl[0:255]
        for c in clr_infl:
            ai = etree.SubElement(infl,"{www.mobipocket.com/idx}iform", nsmap={'idx':NSMAP['idx']})
            ai.set('value',c)
            ai.set('exact','yes')
            ai.text = ''

def writeEntry(where, inEntry, head, wtMap, inflGroups, grpMap):
    #print(f"inEntry: {inEntry}")
    wt = inEntry.getMeaningsByTypes()
    origtext = inEntry.getOrig()
    
    writePB(where)

    entry = etree.SubElement(where, "{www.mobipocket.com/idx}entry", nsmap={'idx':NSMAP['idx']})
    for (k,v) in {"name":"word" , "scriptable":"yes" , "spell":"yes"}.items():
        entry.set(k,v)
        
    orth = etree.SubElement(entry, "{www.mobipocket.com/idx}orth", nsmap={'idx':NSMAP['idx']})
    orth.set('value', head)
    if head==None or head == '':
        print(f"head is None for origtext={origtext}, inflGroups={inflGroups}")
    
    #original
    writeOriginal(orth, origtext, inflGroups, grpMap, head)
    
    #meanings with eventual examples
    writeMeanings(orth, wt, wtMap)
    
    #collect inflections
    sInfl = []
    for (k,v) in inEntry.getInflections().items():
        tpis = inEntry.getInflections()[k]
        tpkeys = list(set(tpis.keys()) & set(inflGroups))
        for x in tpkeys:
            sInfl = sInfl + list(map(lambda y: y['infl'], tpis[x]['infl']))
            #sInfl = sInfl + tpis[x]['infl']
            #print(f"writeEntry :: added {k}.{x} :: {len(tpis[x]['infl'])}")
    
    #write out inflections
    writeInflections(orth, sInfl)

#fs, inEntries, h, oo, wtMap, grpMap
def writeComplexEntry(where, inEntries, head, origs, wtMap, grpMap):
    writePB(where)

    entry = etree.SubElement(where, "{www.mobipocket.com/idx}entry", nsmap={'idx':NSMAP['idx']})
    for (k,v) in {"name":"word" , "scriptable":"yes" , "spell":"yes"}.items():
        entry.set(k,v)
        
    orth = etree.SubElement(entry, "{www.mobipocket.com/idx}orth", nsmap={'idx':NSMAP['idx']})
    orth.set('value', head)
    
    #why complex
    porig = etree.SubElement(orth,"p")
    iorig = etree.SubElement(porig,"i")
    iorig.text = 'Different words sharing the same inflected form. Potential originals:'
    
    #meaning +examples for each candidate
    ol = etree.SubElement(orth,"ol")
    sInfl = []
    for o in list(origs.keys()):
        li = etree.SubElement(ol,"li")
        igrps = origs[o]
        #original
        writeOriginal(li, o, igrps, grpMap, head)
        #meanings with eventual examples
        wt = inEntries[o].getMeaningsByTypes()
        writeMeanings(li, wt, wtMap)
        #collect inflections
        for (k,v) in inEntries[o].getInflections().items():
            tpis = inEntries[o].getInflections()[k]
            tpkeys = list(set(tpis.keys()) & set(igrps))
            for x in tpkeys:
                sInfl = sInfl + list(map(lambda y: y['infl'], tpis[x]['infl']))
        
    #write out inflections
    writeInflections(orth, sInfl)

def writeXML(outFileName, wtMap, inEntries, inInflection2Head, inHead2Entry, grpMap):
    
    (html,fs) = writeXmlHeader()
    simple = 0
    complex = 0
    # first write out words with no overlapping with another word's inflection
    for h in sorted(inHead2Entry.keys()):
        oo = inHead2Entry[h]
        #print(f"h={h}, oo={oo}")
        if len(oo.items()) == 1:
            o = list(oo.keys())[0] #Entry.orig
            igrps = oo[o]    #list of inflection group IDs
            writeEntry(fs, inEntries[o], h, wtMap, igrps, grpMap)
            simple = simple + 1
        else:
            writeComplexEntry(fs, inEntries, h, oo, wtMap, grpMap)
            complex = complex + 1
    
    print(f"Processed {simple} simple and {complex} complex entries.")
    # write tree to actual XML file
    etree.ElementTree(html).write(outFileName, xml_declaration=True, encoding='UTF-8')
    print(f"XML successfully created: {outFileName}")
