from lxml import etree

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
    return (html,fs)
    
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

def writeInflections(where, sInfl, head):
    if len(sInfl) > 0:
        infl = etree.SubElement(where, "{www.mobipocket.com/idx}infl", nsmap={'idx':NSMAP['idx']})
        clr_infl = list(set(sInfl))
        if len(clr_infl) > 255:
            print(f"WARNING: head={head} has {len(clr_infl)} inflections! Truncated to 255")
            clr_infl = clr_infl[0:255]
        for c in clr_infl:
            ai = etree.SubElement(infl,"{www.mobipocket.com/idx}iform", nsmap={'idx':NSMAP['idx']})
            ai.set('value',c)
            ai.set('exact','yes')
            ai.text = ''

'''
    where: etree node
    page: list( {orig: "orig word", inflGrps: ["OTH" or "Pt.Abl...."], mbytp: Entry.getMeaningsByTypes() } )
    head: "inf grp head"
    infls: list(string) of inflection literals
'''
def writeEntry(where, page, head, grpMap, infls, wtMap):
    
    writePB(where)

    entry = etree.SubElement(where, "{www.mobipocket.com/idx}entry", nsmap={'idx':NSMAP['idx']})
    for (k,v) in {"name":"word" , "scriptable":"yes" , "spell":"yes"}.items():
        entry.set(k,v)
        
    orth = etree.SubElement(entry, "{www.mobipocket.com/idx}orth", nsmap={'idx':NSMAP['idx']})
    try:
        orth.set('value', head)
    except:
        print(f"XMLWriter :: orth.set failed, head={head}")
        print(infls)
    
    #original
    if len(page) == 1:
        d = page[0]
        writeOriginal(orth, d['orig'], d['inflGrps'], grpMap, head)
        writeMeanings(orth, d['mbytp'], wtMap)
    else:
        ph = etree.SubElement(orth,"p")
        bh = etree.SubElement(ph,"b")
        bh.text = head
        ol = etree.SubElement(orth,"ol")
        for d in page:
            li = etree.SubElement(ol,"li")
            writeOriginal(li, d['orig'], d['inflGrps'], grpMap, head)
            writeMeanings(li, d['mbytp'], wtMap)
    
    #write out inflections
    writeInflections(orth, infls, head)

def writeXML(outFileName, inGroups, wtMap, grpMap):
    (html,fs) = writeXmlHeader()
    cnt = 0
    invalidgrp = []
    for id in sorted(inGroups.keys()):
        g = inGroups[id]
        if(g.isValid()):
            writeEntry(fs, g.getPages(), g.getHead(), grpMap, g.getInflections(), wtMap)
            cnt = cnt+1
        else:
            invalidgrp.append(id)
    print(f"Headwords to write out: {cnt}")
    if len(invalidgrp) > 0:
        print(f"{len(invalidgrp)} groups deemed as invalid")
    # write tree to actual XML file
    etree.ElementTree(html).write(outFileName, xml_declaration=True, encoding='UTF-8')
    print(f"XML successfully created: {outFileName}")
