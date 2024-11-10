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
    etree.SubElement(where, "{www.mobipocket.com/pagebreak}pagebreak", nsmap={'mbp':NSMAP['mbp']})

def writeOriginal(orth, origtext):
    porig = etree.SubElement(orth,"p")
    borig = etree.SubElement(porig,"b")
    borig.text = origtext

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

def writeEntry(where, inEntry, wtMap, inInflection2Entry):
    #print(f"inEntry: {inEntry}")
    wt = inEntry.getMeaningsByTypes()
    origtext = inEntry.getOrig()
    
    writePB(where)

    entry = etree.SubElement(where, "{www.mobipocket.com/idx}entry", nsmap={'idx':NSMAP['idx']})
    for (k,v) in {"name":"word" , "scriptable":"yes" , "spell":"yes"}.items():
        entry.set(k,v)
        
    orth = etree.SubElement(entry, "{www.mobipocket.com/idx}orth", nsmap={'idx':NSMAP['idx']})
    orth.set('value', origtext)
    
    #original
    writeOriginal(orth, origtext)
    
    #meanings with eventual examples
    writeMeanings(orth, wt, wtMap)
    
    #inflexions
    sInfl = []
    for (k,v) in inEntry.getInflections().items():
        if len(inInflection2Entry[k]) == 1:
            sInfl.append(k)
    if len(sInfl) > 0:
        infl = etree.SubElement(orth, "{www.mobipocket.com/idx}infl", nsmap={'idx':NSMAP['idx']})
        clr_infl = list(set(sInfl))
        for c in clr_infl:
            ai = etree.SubElement(infl,"{www.mobipocket.com/idx}iform", nsmap={'idx':NSMAP['idx']})
            ai.set('value',c)
            ai.set('exact','yes')

def writeComplexEntry(where, origtext, wtMap, inEntries, inInflection2Entry):
    writePB(where)

    entry = etree.SubElement(where, "{www.mobipocket.com/idx}entry", nsmap={'idx':NSMAP['idx']})
    for (k,v) in {"name":"word" , "scriptable":"yes" , "spell":"yes"}.items():
        entry.set(k,v)
        
    orth = etree.SubElement(entry, "{www.mobipocket.com/idx}orth", nsmap={'idx':NSMAP['idx']})
    orth.set('value', origtext)
    
    #original
    writeOriginal(orth, origtext)
    
    #why complex
    porig = etree.SubElement(orth,"p")
    iorig = etree.SubElement(porig,"i")
    iorig.text = 'Different words sharing the same inflected form. Potential originals:'
    
    #meanings with eventual examples
    #1. entries having the same dictionary form as origtext (all word types)
    wt = {}
    if origtext in inEntries:
        wt0 = inEntries[origtext].getMeaningsByTypes()
        for t in wt0:
            wt[t] = []
            for i in wt0[t]:
                wt[t].append({'inflected': None, 'orig': origtext, 'meaning': i})
    
    #2. entries having an inflected form matching the literal of origtext, filtered for equalling word type
    for e in inInflection2Entry[origtext]:
        if e != origtext:
            wt0 = inEntries[e].getMeaningsByTypes()
            matchInfl = inEntries[e].getInflections()[origtext]
            for f in matchInfl:
                ft = f['wtype']
                if ft in wt0:
                    if ft not in wt:
                        wt[ft] = []
                    for i in wt0[ft]:
                        wt[ft].append({'inflected': f['src'], 'orig': e, 'meaning': i})
            
    writeComplexMeanings(orth, wt, wtMap)
    
    #no inflection since the entry itself represents an inflected form

def writeXML(outFileName, wtMap, inEntries, inInflection2Entry):
    
    (html,fs) = writeXmlHeader()
    
    # first write out words with no overlapping with another word's inflection
    for e in sorted(inEntries):
        o = inEntries[e].getOrig()
        if len(inInflection2Entry[o]) == 1:
            writeEntry(fs,inEntries[e], wtMap, inInflection2Entry)
        else:
            writeComplexEntry(fs, o, wtMap, inEntries, inInflection2Entry)
    
    # write tree to actual XML file
    etree.ElementTree(html).write(outFileName, xml_declaration=True, encoding='UTF-8')
