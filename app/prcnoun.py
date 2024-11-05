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
    ,'ends_nk':rp_ends_alter_cons_nk
    ,'rp_ends_vow':rp_ends_vow}

def getAlternate(word, mx):
    ret = word
    if word not in EXCEPTIONS['ALTERNATE']:
        if mx['ends_nk']:
            ret = ret[:len(ret)-1] + 'g'
        elif mx['ends_alter']:
            last = ret[len(ret)-1]
            ret = ret[:len(ret)-1] + ALTERNATING_CONSONANTS[last]
    return ret

def getSrc(word, actSrc):
    if word['src']:
        return word['src'] + '.' + actSrc
    else:
        return actSrc

def getPlural(word, mx):
    if word['infl'] in EXCEPTIONS['PLURAL']:
        return {'infl': EXCEPTIONS['PLURAL'][word['infl']] , 'src': getSrc(word, 'PlEx')}
        
    ret = word['infl']
    if mx['last_syl_low']:
        ret = ret + 'lar'
    else:
        ret = ret + 'lar'
    
    return {'infl': ret , 'src': getSrc(word, 'Pl')}
        
def getAccusative(word, mx):
    if word['infl'] in EXCEPTIONS['ACCUSATIVE']:
        return {'infl': EXCEPTIONS['ACCUSATIVE'][word['infl']] , 'src': getSrc(word, 'AccEx')}
        
    ret = word['infl']
    if mx['rp_ends_vow']:
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
        return {'infl': EXCEPTIONS['DATIVE'][word['infl']] , 'src': getSrc(word, 'AccEx')}
        
    ret = word['infl']
    if mx['rp_ends_vow']:
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
        return {'infl': EXCEPTIONS['LOCATIVE'][word['infl']] , 'src': getSrc(word, 'LocEx')}
        
    ret = word['infl']
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
        return {'infl': EXCEPTIONS['ABLATIVE'][word['infl']] , 'src': getSrc(word, 'AblEx')}
        
    ret = word['infl']
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
    if word['infl'] in EXCEPTIONS['POSSESSIVE']:
        ret = []
        for w in EXCEPTIONS['POSSESSIVE'][word['infl']]:
            ret.append({'infl':  w, 'src': getSrc(word, 'PossEx')})
        return ret
        
    vow_lo = ['m','n','sı','mız','nız']
    vow_hi = ['m','n','si','miz','niz']
    
    con_ai = ['ım','ın','ısı','ımız','ınız']
    con_ei = ['im','in','isi','imiz','iniz']
    con_ou = ['um','un','u','umuz','unuz']
    con_oouu = ['üm','ün','ü','ümüz','ünüz']
        
    ret = []
    if mx['rp_ends_vow']:
        if mx['last_syl_low']:
            for p in vow_lo:
                ret.append(word['infl']+p)
        else:
            for p in vow_hi:
                ret.append(word['infl']+p)
    else:
        # alternate when needed
        base = getAlternate(word['infl'], mx)
            
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
        return {'infl': EXCEPTIONS['GENITIVE'][word['infl']] , 'src': getSrc(word, 'GenEx')}
    
    ret = ''
    if mx['rp_ends_vow']:
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
    
    ret = ''
    if mx['rp_ends_vow']:
        ret = word['infl']
    else:
        if mx['last_syl_low']:
            ret = word['infl']+'la'
        else:
            ret = word['infl']+'le'
            
    return {'infl': ret , 'src': getSrc(word, 'With')}
            
def getKi(word):
    ret = word['infl']+'ki'
    return {'infl': ret , 'src': getSrc(word, 'Ki')}



def processNoun(w):

    infl = []
    
    wout = {}
    for k in rps:
        if regex.match(rps[k],w):
            wout[k]=True
        else:
            wout[k]=False
            
    plr = getPlural({'infl': w, 'src': None},wout)
    infl.append(plr)
    
    plrout = {}
    for k in rps:
        if regex.match(rps[k],plr['infl']):
            plrout[k]=True
        else:
            plrout[k]=False
    
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
    
    wpos = getPossessive({'infl': w, 'src': None},wout)
    plrpos = getPossessive(plr,plrout)
    infl= infl + wpos
    infl= infl + plrpos
    infl.append(getGenitive({'infl': w, 'src': None},wout))
    infl.append(getGenitive(plr,plrout))
    for a in wpos:
        aout = {}
        for k in rps:
            if regex.match(rps[k],a['infl']):
                aout[k]=True
            else:
                aout[k]=False
        infl.append(getAccusative(a,aout))
        infl.append(getGenitive(a,aout))
        infl.append(getWith(a,aout))
    for a in plrpos:
        aout = {}
        for k in rps:
            if regex.match(rps[k],a['infl']):
                aout[k]=True
            else:
                aout[k]=False
        infl.append(getAccusative(a,aout))
        infl.append(getGenitive(a,aout))
        infl.append(getWith(a,aout))
    
    #wtype = noun in all cases
    for i in infl:
        i['wtype'] = 'noun'
    
    return infl
    
#TEST
#for w in ['karı']:
#    print(f"{w} -> {processNoun(w)}")
