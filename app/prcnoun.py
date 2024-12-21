import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.constants import *

rps = {'last_syl_low':rp_last_syl_low
    ,'last_syl_ai':rp_last_syl_ai
    ,'last_syl_ou':rp_last_syl_ou
    ,'last_syl_ei':rp_last_syl_ei
    ,'last_syl_öü':rp_last_syl_oouu
    ,'last_cons_hard':rp_last_cons_hard
    ,'ends_alter':rp_ends_alter_cons
    ,'ends_alter_poss':rp_ends_alter_cons_poss
    ,'ends_nk':rp_ends_alter_cons_nk
    ,'ends_vow':rp_ends_vow}
    
rps_pti = {'last_syl_ai':rp_last_syl_ai
    ,'last_syl_ou':rp_last_syl_ou
    ,'last_syl_ei':rp_last_syl_ei
    ,'last_syl_öü':rp_last_syl_oouu
    ,'last_cons_hard':rp_last_cons_hard}

def getAlternate(word, mx):
    ret = word
    if word not in EXCEPTIONS['ALTERNATE']:
        if mx['ends_nk']:
            ret = ret[:len(ret)-1] + 'g'
        elif mx['ends_alter']:
            last = ret[len(ret)-1]
            ret = ret[:len(ret)-1] + ALTERNATING_CONSONANTS[last]
    return ret
    
def getAlternatePoss(word, mx):
    ret = word
    if word not in EXCEPTIONS['ALTERNATE_POSS']:
        if mx['ends_nk']:
            ret = ret[:len(ret)-1] + 'g'
        elif mx['ends_alter_poss']:
            last = ret[len(ret)-1]
            ret = ret[:len(ret)-1] + ALTERNATING_CONSONANTS_POSS[last]
    return ret

def getPlural(word, mx):
    if word['infl'] in EXCEPTIONS['PLURAL']:
        return {'infl': EXCEPTIONS['PLURAL'][word['infl']] , 'src': getSrc(word, 'Pl')}
        
    ret = word['infl']
    if mx['last_syl_low']:
        ret = ret + 'lar'
    else:
        ret = ret + 'ler'
    
    return {'infl': ret , 'src': getSrc(word, 'Pl')}
        
def getAccusative(word, mx):
    if word['infl'] in EXCEPTIONS['ACCUSATIVE']:
        return {'infl': EXCEPTIONS['ACCUSATIVE'][word['infl']] , 'src': getSrc(word, 'Acc')}
        
    ret = word['infl']
    if mx['ends_vow']:
        # N-buffer from https://www.turkishtextbook.com/the-n-buffer/
        last2 = ret[len(ret)-2:]
        if last2 in ['sı','si','su','sü']:
            ret = ret + 'n'
        else:
            ret = ret + 'y'
    else:
        # alternate when needed
        ret = getAlternate(word['infl'], mx)
        
    if mx['last_syl_ai']:
        ret = ret + 'ı'
    elif mx['last_syl_ou']:
        ret = ret + 'u'
    elif mx['last_syl_ei']:
        ret = ret + 'i'
    elif mx['last_syl_öü']:
        ret = ret + 'ü'
    
    return {'infl': ret , 'src': getSrc(word, 'Acc')}

def getDative(word, mx):
    if word['infl'] in EXCEPTIONS['DATIVE']:
        return {'infl': EXCEPTIONS['DATIVE'][word['infl']] , 'src': getSrc(word, 'Acc')}
        
    ret = word['infl']
    if mx['ends_vow'] and word['src'] and word['src'][len(word['src'])-4:]=='Poss':
        ret = ret + 'n'
    elif mx['ends_vow']:
        ret = ret + 'y'
    else:
        # alternate when needed
        ret = getAlternate(word['infl'], mx)
        
    if mx['last_syl_low']:
        ret = ret + 'a'
    else:
        ret = ret + 'e'
    
    return {'infl': ret , 'src': getSrc(word, 'Dat')}

def getLocative(word, mx):
    if word['infl'] in EXCEPTIONS['LOCATIVE']:
        return {'infl': EXCEPTIONS['LOCATIVE'][word['infl']] , 'src': getSrc(word, 'Loc')}
        
    ret = word['infl']
    if mx['ends_vow'] and word['src'] and word['src'][len(word['src'])-4:]=='Poss':
        ret = ret + 'n'
        
    if mx['last_syl_low'] and mx['last_cons_hard']:
        ret = ret + 'ta'
    elif mx['last_cons_hard']:
        ret = ret + 'te'
    elif mx['last_syl_low']:
        ret = ret + 'da'
    else:
        ret = ret + 'de'
    
    return {'infl': ret , 'src': getSrc(word, 'Loc')}

def getAblative(word, mx):
    if word['infl'] in EXCEPTIONS['ABLATIVE']:
        return {'infl': EXCEPTIONS['ABLATIVE'][word['infl']] , 'src': getSrc(word, 'Abl')}
        
    ret = word['infl']
    if mx['ends_vow'] and word['src'] and word['src'][len(word['src'])-4:]=='Poss':
        ret = ret + 'n'
        
    if mx['last_syl_low'] and mx['last_cons_hard']:
        ret = ret + 'tan'
    elif mx['last_cons_hard']:
        ret = ret + 'ten'
    elif mx['last_syl_low']:
        ret = ret + 'dan'
    else:
        ret = ret + 'den'
    
    return {'infl': ret , 'src': getSrc(word, 'Abl')}

def getLocativePersonals(word):
    lo = ['yım','sın','yız','sınız','ydım','ydın','ydı','ydık','ydınız','ydılar']
    hi = ['yim','sin','yiz','siniz','ydim','ydin','ydi','ydik','ydiniz','ydiler']

    x = None
    loc = word['infl']
    if loc[len(loc)-1] == 'a':
        x = lo
    else:
        x = hi
        
    ret = []
    for p in x:
        ret.append({'infl': loc+p , 'src': getSrc(word, 'LocPers')})
        
    return ret
        
def getPossessive(word, mx):
    stem = word['infl']
    if stem in EXCEPTIONS['POSSESSIVE']:
        ret = []
        for w in EXCEPTIONS['POSSESSIVE'][stem]:
            ret.append({'infl':  w, 'src': getSrc(word, 'Poss')})
        return ret
    
    else:
        # alternate when needed
        stem = getAlternate(word['infl'], mx)

    vow_lo = ['m','n','sı','mız','nız','sı']
    vow_hi = ['m','n','si','miz','niz','si']
    
    con_ai = ['ım','ın','ı','ımız','ınız','ı']
    con_ei = ['im','in','i','imiz','iniz','i']
    con_ou = ['um','un','u','umuz','unuz','u']
    con_oouu = ['üm','ün','ü','ümüz','ünüz','ü']
        
    ret = []
    if mx['ends_vow']:
        if mx['last_syl_low']:
            for p in vow_lo:
                ret.append(stem+p)
        else:
            for p in vow_hi:
                ret.append(stem+p)
    else:
        # alternate when needed
        base = getAlternatePoss(stem, mx)
            
        # then apply possessive markers
        if mx['last_syl_ai']:
            for p in con_ai:
                ret.append(base+p)
        elif mx['last_syl_ou']:
            for p in con_ou:
                ret.append(base+p)
        elif mx['last_syl_ei']:
            for p in con_ei:
                ret.append(base+p)
        else:
            for p in con_oouu:
                ret.append(base+p)
                
    ret2 = []
    src = getSrc(word, 'Poss')
    for r in ret:
        ret2.append({'infl': r , 'src': src})
    return ret2
    
def getGenitive(word, mx):
    if word['infl'] in EXCEPTIONS['GENITIVE']:
        return {'infl': EXCEPTIONS['GENITIVE'][word['infl']] , 'src': getSrc(word, 'Gen')}
    
    ret = ''
    if mx['ends_vow']:
        if mx['last_syl_low']:
            ret = word['infl']+'nın'
        else:
            ret = word['infl']+'nin'
    else:
        # alternate when needed
        base = getAlternate(word['infl'], mx)
            
        # then apply possessive markers
        if mx['last_syl_ai']:
            ret = base+'ın'
        elif mx['last_syl_ou']:
            ret = base+'un'
        elif mx['last_syl_ei']:
            ret = base+'in'
        else:
            ret = base+'ün'
            
    return {'infl': ret , 'src': getSrc(word, 'Gen')}
    
def getWith(word, mx):
    
    ret = word['infl']
    if mx['ends_vow']:
        ret = word['infl'] + 'y'
        
    if mx['last_syl_low']:
        ret = ret+'la'
    else:
        ret = ret+'le'
            
    return {'infl': ret , 'src': getSrc(word, 'With')}
            
def getKi(word):
    ret = word['infl']+'ki'
    return {'infl': ret , 'src': getSrc(word, 'Ki')}

def getIndirect(word, mx):
    ret = word['infl']
    if mx['ends_vow']:
        ret = ret + 'y'
        
    if mx['last_syl_ai']:
        return {'infl': ret + 'mış', 'src': getSrc(word, 'Ind')}
    elif mx['last_syl_ei']:
        return {'infl': ret + 'miş', 'src': getSrc(word, 'Ind')}
    elif mx['last_syl_ou']:
        return {'infl': ret + 'muş', 'src': getSrc(word, 'Ind')}
    elif mx['last_syl_öü']:
        return {'infl': ret + 'müş', 'src': getSrc(word, 'Ind')}
    else:
        return word

def getPast(word, mx):
    ret = word['infl']
    if mx['ends_vow']:
        ret = ret + 'y'
        
    if mx['last_cons_hard']:
        ret = ret + 't'
    else:
        ret = ret + 'd'
    
    if mx['last_syl_ai']:
        return {'infl': ret + 'ı', 'src': getSrc(word, 'Pt')}
    elif mx['last_syl_ei']:
        return {'infl': ret + 'i', 'src': getSrc(word, 'Pt')}
    elif mx['last_syl_ou']:
        return {'infl': ret + 'u', 'src': getSrc(word, 'Pt')}
    elif mx['last_syl_öü']:
        return {'infl': ret + 'ü', 'src': getSrc(word, 'Pt')}
    else:
        return word

def getPredicative(word, mx):
    ret = word['infl']
    
    if mx['last_cons_hard']:
        ret = ret + 't'
    else:
        ret = ret + 'd'
    
    if mx['last_syl_ai']:
        ret = ret + 'ır'
    elif mx['last_syl_ei']:
        ret = ret + 'ir'
    elif mx['last_syl_ou']:
        ret = ret + 'ur'
    elif mx['last_syl_öü']:
        ret = ret + 'ür'
    
    return {'infl': ret, 'src': getSrc(word, 'Pred')}

def getPersonMarker(word, mx, paradigm):
    pm = []
    if paradigm == 'k-pt':
        if mx['last_syl_ai']:
            pm = ['m','n','','k','nız','lar']
        elif mx['last_syl_ei']:
            pm = ['m','n','','k','niz','ler']
        elif mx['last_syl_ou']:
            pm = ['m','n','','k','nuz','lar']
        elif mx['last_syl_öü']:
            pm = ['m','n','','k','nüz','ler']
    if paradigm == 'z-ind':
        if mx['last_syl_ai']:
            pm = ['ım','ın','','ız','sınız','lar']
        elif mx['last_syl_ei']:
            pm = ['im','in','','iz','siniz','ler']
        elif mx['last_syl_ou']:
            pm = ['um','un','','uz','unuz','lar']
        elif mx['last_syl_öü']:
            pm = ['üm','ün','','üz','ünüz','ler']
            
    ret = []
    for p in pm:
        stem = word['infl']
        if mx['ends_vow'] and paradigm == 'z-ind' and p != '':
            stem = stem + 'y'
        
        ret.append({'infl': stem + p , 'src': word['src']})
    
    return ret

def processNoun(w):

    infl = []
    
    wout = getMx(w, rps)           
    plr = getPlural({'infl': w, 'src': None},wout)
    infl.append(plr)
    
    plrout = getMx(plr['infl'], rps)
    
    ## predicative on nominal
    infl.append(getPredicative({'infl': w, 'src': None},wout))
    infl.append(getPredicative(plr,plrout))
    
    infl.append(getAccusative({'infl': w, 'src': None},wout))
    infl.append(getAccusative(plr,plrout))
    infl.append(getDative({'infl': w, 'src': None},wout))
    infl.append(getDative(plr,plrout))
    infl.append(getAblative({'infl': w, 'src': None},wout))
    infl.append(getAblative(plr,plrout))
    
    infl.append(getWith({'infl': w, 'src': None},wout))
    infl.append(getWith(plr,plrout))
    infl.append(getKi(getAblative({'infl': w, 'src': None},wout)))
    infl.append(getKi(getAblative(plr,plrout)))
    
    wloc = getLocative({'infl': w, 'src': None},wout)
    plrloc = getLocative(plr,plrout)
    infl.append(wloc)
    infl.append(plrloc)
    infl = infl + getLocativePersonals(wloc)
    infl = infl + getLocativePersonals(plrloc)
    
    infl.append(getKi(wloc))
    infl.append(getKi(plrloc))
    
    #Past and personal marker applied to nominal
    wpm = getPersonMarker({'infl': w, 'src': 'Aor'},wout,'z-ind')
    plrpm = getPersonMarker({'infl': plr['infl'], 'src': getSrc(plr,'Aor')},plrout,'z-ind')
    
    infl = infl + wpm + plrpm
    
    wpt = getPast({'infl': w, 'src': None},wout)
    plrpt = getPast(plr,plrout)
    wptout = getMx(wpt['infl'], rps)
    plrptout = getMx(plrpt['infl'], rps)
    #print(f"{w} -> wpt: {wpt['infl']}, plrpt: {plrpt['infl']}")
    wptpm = getPersonMarker(wpt,wptout,'k-pt')
    plrptpm = getPersonMarker(plrpt,plrptout,'k-pt')
    
    infl= infl + wptpm + plrptpm
    
    #Indirect and personal marker applied to nominal
    wind = getIndirect({'infl': w, 'src': None},wout)
    plrind = getIndirect(plr,plrout)
    windout = getMx(wind['infl'], rps)
    plrindout = getMx(plrind['infl'], rps)
    windpm = getPersonMarker(wind,windout,'z-ind')
    plrindpm = getPersonMarker(plrind,plrindout,'z-ind')
    ## +predicative
    infl.append(getPredicative(wind,windout))
    infl.append(getPredicative(plrind,plrindout))
    infl= infl + windpm + plrindpm
    
    windpt = getPast(wind,windout)
    windptout = getMx(windpt['infl'], rps)
    plrindpt = getPast(plrind,plrindout)
    plrindptout = getMx(plrindpt['infl'], rps)
    windptpm = getPersonMarker(windpt,windptout,'k-pt')
    plrindptpm = getPersonMarker(plrindpt,plrindptout,'k-pt')
    
    infl= infl + windptpm + plrindptpm
    
    #Possessive and variations
    wpos = getPossessive({'infl': w, 'src': None},wout)
    plrpos = getPossessive(plr,plrout)
    infl= infl + wpos
    infl= infl + plrpos
    infl.append(getGenitive({'infl': w, 'src': None},wout))
    infl.append(getGenitive(plr,plrout))
    for a in wpos:
        aout = getMx(a['infl'], rps)
        infl.append(getAccusative(a,aout))
        infl.append(getDative(a,aout))
        infl.append(getGenitive(a,aout))
        infl.append(getKi(getGenitive(a,aout)))
        infl.append(getWith(a,aout))
        infl.append(getPredicative(a,aout))
        infl.append(getAblative(a,aout))
        infl.append(getKi(getAblative(a,aout)))
        infl.append(getLocative(a,aout))
        infl.append(getKi(getLocative(a,aout)))
        ind = getIndirect(a,aout)
        indout = getMx(ind['infl'], rps)
        indpred = getPredicative(ind,indout)
        infl.append(indpred)
        indpm = getPersonMarker(ind,indout,'z-ind')
        indpt = getPast(ind,indout)
        indptout = getMx(indpt['infl'], rps)
        infl.append(getPredicative(indpt,indptout))
        indptpm = getPersonMarker(indpt,indout,'k-pt')
        infl = infl + indpm + indptpm
        apt = getPast(a,aout)
        aptout = getMx(apt['infl'], rps)
        aptpm = getPersonMarker(apt,aptout,'k-pt')
        infl = infl + aptpm
    for a in plrpos:
        aout = getMx(a['infl'], rps)
        infl.append(getAccusative(a,aout))
        infl.append(getDative(a,aout))
        infl.append(getGenitive(a,aout))
        infl.append(getKi(getGenitive(a,aout)))
        infl.append(getWith(a,aout))
        infl.append(getPredicative(a,aout))
        infl.append(getAblative(a,aout))
        infl.append(getKi(getAblative(a,aout)))
        infl.append(getLocative(a,aout))
        infl.append(getKi(getLocative(a,aout)))
        ind = getIndirect(a,aout)
        indout = getMx(ind['infl'], rps)
        infl.append(getPredicative(ind,indout))
        indpm = getPersonMarker(ind,indout,'z-ind')
        indpt = getPast(ind,indout)
        indptout = getMx(indpt['infl'], rps)
        infl.append(getPredicative(indpt,indptout))
        indptpm = getPersonMarker(indpt,indout,'k-pt')
        infl = infl + indpm + indptpm
        apt = getPast(a,aout)
        aptout = getMx(apt['infl'], rps)
        aptpm = getPersonMarker(apt,aptout,'k-pt')
        infl = infl + aptpm
    
    #Predicative DIr +past mIstIr
    
    #wtype = noun in all cases
    for i in infl:
        i['wtype'] = 'noun'
    
    ret = getInflectionGroups(infl,'noun',w)
    
    return ret
    
#TEST
#for w in ['karı']:
#    print(f"{w} -> {processNoun(w)}")
