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

def processAdj(w):

    infl = []
    
    wout = getMx(w, rps)

    ## predicative
    infl.append(getPredicative({'infl': w, 'src': None},wout))
    
    #Past and personal marker
    wpm = getPersonMarker({'infl': w, 'src': 'Aor'},wout,'z-ind')
    
    infl = infl + wpm
    
    wpt = getPast({'infl': w, 'src': None},wout)
    wptout = getMx(wpt['infl'], rps)
    wptpm = getPersonMarker(wpt,wptout,'k-pt')
    
    infl= infl + wptpm
    
    #Indirect and personal marker applied to nominal
    wind = getIndirect({'infl': w, 'src': None},wout)
    windout = getMx(wind['infl'], rps)
    windpm = getPersonMarker(wind,windout,'z-ind')
    ## +predicative
    infl.append(getPredicative(wind,windout))
    infl= infl + windpm
    
    windpt = getPast(wind,windout)
    windptout = getMx(windpt['infl'], rps)
    windptpm = getPersonMarker(windpt,windptout,'k-pt')
    
    infl= infl + windptpm
    
    #wtype = adj in all cases
    for i in infl:
        i['wtype'] = 'adj'
    
    ret = getInflectionGroups(infl,'adj',w)
    
    return ret
