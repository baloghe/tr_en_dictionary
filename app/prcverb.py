import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.constants import *
import app.prcnoun as noun


rp_stem = {'last_syl_low':rp_last_syl_low
            ,'ends_cons':rp_ends_cons
            ,'ends_vow':rp_ends_vow
            ,'last_syl_ai':rp_last_syl_ai
            ,'last_syl_ou':rp_last_syl_ou
            ,'last_syl_ei':rp_last_syl_ei
            ,'last_syl_öü':rp_last_syl_oouu
            ,'ends_uüii':rp_ends_uuii
            ,'ends_aeoö':rp_ends_aeoo
            ,'last_cons_hard':rp_last_cons_hard}

def getContinuousStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['GENERAL_STEM']:
        return EXCEPTIONS['GENERAL_STEM'][stem]
    
    if regex.match(rp_ends_aeoo, stem):
        return stem[:len(stem)-1]
    else:
        return stem
        
def getFutureStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['GENERAL_STEM']:
        return EXCEPTIONS['GENERAL_STEM'][stem]
    else:
        return stem
        
def getIpStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['GENERAL_STEM']:
        return EXCEPTIONS['GENERAL_STEM'][stem]
    else:
        return stem
        
def getIngStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['GENERAL_STEM']:
        return EXCEPTIONS['GENERAL_STEM'][stem]
    else:
        return stem
        
def getCanStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['GENERAL_STEM']:
        return EXCEPTIONS['GENERAL_STEM'][stem]
    else:
        return stem

def getStem(word, inMarker=None):
    if inMarker=='Cont':
        return getContinuousStem(word)
    elif inMarker=='Fut':
        return getFutureStem(word)
    elif inMarker=='Neg-Cont':
        return word[:len(word)-2]
    elif inMarker=='Neg':
        return word[:len(word)-1]
    elif inMarker=='Ip':
        return getIpStem(word)
    elif inMarker=='Ing':
        return getIngStem(word)
    elif inMarker=='Can':
        return getCanStem(word)
    else:
        return word[:len(word)-3]

def getContinuous(stem, mx):
    if stem['infl'] in EXCEPTIONS['CONTINUOUS']:
        return {'infl': EXCEPTIONS['CONTINUOUS'][stem['infl']] , 'src': getSrc(stem, 'Cont')}

    ret = stem['infl']
    if mx['ends_cons'] and mx['last_syl_ai']:
        ret = ret + 'ıyor'
    elif mx['ends_cons'] and mx['last_syl_ei']:
        ret = ret + 'iyor'
    elif mx['ends_cons'] and mx['last_syl_ou']:
        ret = ret + 'uyor'
    elif mx['ends_cons'] and mx['last_syl_öü']:
        ret = ret + 'üyor'
    elif mx['ends_uüii']:
        ret = ret + 'yor'
    
    return {'infl': ret, 'src': getSrc(stem, 'Cont')}
            
def getFuture(stem, mx):
    if stem['infl'] in EXCEPTIONS['FUTURE']:
        return {'infl': EXCEPTIONS['FUTURE'][stem['infl']] , 'src': getSrc(stem, 'Fut')}

    ret = stem['infl']
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_ei'] or mx['last_syl_öü']:
        ret = ret + 'ecek'
    else:
        ret = ret + 'acak'
    
    return {'infl': ret, 'src': getSrc(stem, 'Fut')}

def getPast(word, mx):
    if word['infl'][len(word['infl'])-3:] == 'yor':
        return {'infl': word['infl'] + 'du', 'src': getSrc(word, 'Pt')}
    elif word['infl'][len(word['infl'])-2:] == 'ak':
        return {'infl': word['infl'] + 'tı', 'src': getSrc(word, 'Pt')}
    elif word['infl'][len(word['infl'])-2:] == 'ek':
        return {'infl': word['infl'] + 'ti', 'src': getSrc(word, 'Pt')}
    elif word['infl'][len(word['infl'])-3:] in ['mış','miş','muş','müş']:
        return {'infl': word['infl'] + 't', 'src': getSrc(word, 'Pt')}
    else:
        ret = word['infl']
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

def getIndirect(stem, mx):
    ret = stem['infl']
    if mx['last_syl_ai']:
        return {'infl': ret + 'mış', 'src': getSrc(stem, 'Ind')}
    elif mx['last_syl_ei']:
        return {'infl': ret + 'miş', 'src': getSrc(stem, 'Ind')}
    elif mx['last_syl_ou']:
        return {'infl': ret + 'muş', 'src': getSrc(stem, 'Ind')}
    elif mx['last_syl_öü']:
        return {'infl': ret + 'müş', 'src': getSrc(stem, 'Ind')}
    else:
        return stem

def getAorist(stem, mx):
    if stem['infl'] in EXCEPTIONS['AORIST']:
        return {'infl': EXCEPTIONS['AORIST'][stem['infl']] , 'src': getSrc(stem, 'Aor')}
    
    ret = stem['infl']
    if mx['ends_vow']:
        ret = ret + 'r'
    elif len(regex.findall(rp_all_vows,ret)) > 1:
        if mx['last_syl_ai']:
            ret = ret + 'ır'
        elif mx['last_syl_ei']:
            ret = ret + 'ir'
        elif mx['last_syl_ou']:
            ret = ret + 'ur'
        elif mx['last_syl_öü']:
            ret = ret + 'ür'
    else:
        if mx['last_syl_low']:
            ret = ret + 'ar'
        else:
            ret = ret + 'er'
            
    return {'infl': ret, 'src': getSrc(stem, 'Aor')}

def getAoristCant(stem, mx):
    ret = stem['infl']
            
    return {'infl': ret, 'src': getSrc(stem, 'Aor')}
    
def getKen(stem, mode='affirmative'):
    ret = stem['infl']
    
    if mode=='negative':
        ret = ret + 'z'
    
    ret = ret + 'ken'
        
    return {'infl': ret, 'src': getSrc(stem, 'Ing')}

def getProgressive(stem, mx):
    ret = stem['infl']
    
    if mx['last_syl_low']:
        ret = ret + 'makta'
    else:
        ret = ret + 'mekte'
    
    return {'infl': ret, 'src': getSrc(stem, 'Prog')}

def getPredicative(stem, mx):
    ret = stem['infl']
    
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
    
    return {'infl': ret, 'src': getSrc(stem, 'Pred')}

def getImperative(stem, mx):
    ret = stem['infl']
    
    return {'infl': ret, 'src': getSrc(stem, 'Imp')}

def getOptative(stem, mx):
    ret = stem['infl']
    
    if ret in EXCEPTIONS['GENERAL_STEM']:
        ret = EXCEPTIONS['GENERAL_STEM'][ret]
    
    if mx == None:
        mx = getMx(ret, {'ends_vow': rp_ends_vow, 'last_syl_low': rp_last_syl_low})
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'a'
    else:
        ret = ret + 'e'
        
    return {'infl': ret, 'src': getSrc(stem, 'Opt')}
    
def getNecessitative(stem, mx):
    ret = stem['infl']
    
    if mx['last_syl_low']:
        ret = ret + 'malı'
    else:
        ret = ret + 'meli'
        
    return {'infl': ret, 'src': getSrc(stem, 'Nec')}

def getObligation(stem, neg=False):
    negret = stem
    ret = stem
    
    if stem[len(stem)-3:] == 'mak':
        ret = stem[:len(stem)-3] + 'mağa'
        negret = stem[:len(stem)-3] + 'mamağa'
    else:
        ret = stem[:len(stem)-3] + 'meğe'
        negret = stem[:len(stem)-3] + 'memeğe'
        
    if(neg):
        return {'infl': negret, 'src': 'Neg.Obl'}
    else:
        return {'infl': ret, 'src': 'Obl'}

def getConditional(stem, mx, addy=False):
    ret = stem['infl']

    if addy and mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'sa'
    else:
        ret = ret + 'se'
        
    return {'infl': ret, 'src': getSrc(stem, 'Cond')}

def getCannotDictForm(stem, mx):
    ret = stem['infl']
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'amamak'
    else:
        ret = ret + 'ememek'
    
    return {'infl': ret, 'src': getSrc(stem, 'Can.Neg')}

def getPotentialDictForm(stem, mx):
    ret = stem['infl']
    
    if ret in EXCEPTIONS['GENERAL_STEM']:
        ret = EXCEPTIONS['GENERAL_STEM'][ret]
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'abilmek'
    else:
        ret = ret + 'ebilmek'
    
    return {'infl': ret, 'src': getSrc(stem, 'Pot')}

def getIp(stem, mx):
    ret = stem['infl']
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_ai']:
        ret = ret + 'ıp'
    elif mx['last_syl_ei']:
        ret = ret + 'ip'
    elif mx['last_syl_ou']:
        ret = ret + 'up'
    elif mx['last_syl_öü']:
        ret = ret + 'üp'
    
    return {'infl': ret, 'src': getSrc(stem, 'Ip')}

def getIng(stem, mx):
    ret = stem['infl']
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'an'
    else:
        ret = ret + 'en'
    
    return {'infl': ret, 'src': getSrc(stem, 'Ing')}

def getByIng(stem, mx):
    ret = stem['infl']
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'arak'
    else:
        ret = ret + 'erek'
    
    return {'infl': ret, 'src': getSrc(stem, 'Ing')}

def getUnless(stem, mx):
    ret = stem['infl']
    
    if mx['last_syl_low']:
        ret = ret + 'dıkça'
    else:
        ret = ret + 'dikçe'
    
    return {'infl': ret, 'src': getSrc(stem, 'Unless')}

def getAs(stem, mx):
    ret = stem['infl']

    if mx['last_cons_hard']:
        ret = ret + 't'
    else:
        ret = ret + 'd'
    
    if mx['last_syl_ai']:
        ret = ret + 'ıkça'
    elif mx['last_syl_ei']:
        ret = ret + 'ikçe'
    elif mx['last_syl_ou']:
        ret = ret + 'ukça'
    elif mx['last_syl_öü']:
        ret = ret + 'ükçe'
    
    return {'infl': ret, 'src': getSrc(stem, 'As')}

def getWhen(stem, mx):
    ret = stem['infl']
    
    if ret in EXCEPTIONS['GENERAL_STEM']:
        ret = EXCEPTIONS['GENERAL_STEM'][ret]
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_ai']:
        ret = ret + 'ınca'
    elif mx['last_syl_ei']:
        ret = ret + 'ince'
    elif mx['last_syl_ou']:
        ret = ret + 'unca'
    elif mx['last_syl_öü']:
        ret = ret + 'ünce'
    
    return {'infl': ret, 'src': getSrc(stem, 'When')}

def getRelClauses(stem, mx):

    infl = []

    acc = noun.getAccusative(stem, mx)
    dat = noun.getDative(stem, mx)
    abl = noun.getAblative(stem, mx)
    loc = noun.getLocative(stem, mx)
    wth = noun.getWith(stem, mx)

    plr = noun.getPlural(stem, mx)
    plrout = getMx(plr['infl'], noun.rps)

    accplr = noun.getAccusative(plr, plrout)
    datplr = noun.getDative(plr, plrout)
    ablplr = noun.getAblative(plr, plrout)
    locplr = noun.getLocative(plr, plrout)
    wthplr = noun.getWith(plr, plrout)
    
    infl = infl + [acc, dat, abl, loc, wth] + [plr, accplr, datplr, ablplr, locplr, wthplr]

    return infl
    
def getPersonMarker(word, paradigm):
    pm = {'cont-z-pr': ['um','sun','','uz','sunuz','lar']
         ,'cont-k-pt': ['m','n','','k','nuz','lar']
        }
    
    mx = getMx(word['infl'],rp_stem)
        
    ret = []
    if paradigm in ['cont-z-pr', 'cont-k-pt']:
        for p in pm[paradigm]:
            ret.append({'infl': word['infl']+p , 'src': word['src']})
        #bonus: -lArdI
        if paradigm=='cont-k-pt':
            bonus = word['infl']
            if mx['last_syl_ai'] or mx['last_syl_ou']:
                bonus = word['infl'][:len(word['infl'])-2] + 'lardı'
            else:
                bonus = word['infl'][:len(word['infl'])-2] + 'lerdi'
            #print(f"{word['infl']} -> bonus: {bonus}")
            ret.append({'infl': bonus , 'src': word['src']})
    elif paradigm == 'z-fut':
        ending = {'ak': ['ğım','ksın','k','ğız','ksınız','klar']
                 ,'ek': ['ğim','ksin','k','ğiz','ksiniz','kler']}
        actend = word['infl'][len(word['infl'])-2:]
        word['infl'] = word['infl'][:len(word['infl'])-1]
        
        for p in ending[actend]:
            ret.append({'infl': word['infl'] + p , 'src': word['src']})
    elif paradigm == 'k-pr':
        ending = {'lo': ['m','n','','k','nız','lar']
                 ,'hi': ['m','n','','k','niz','ler']}
        actend = ''
        if regex.match(rp_last_syl_ai, word['infl']) or regex.match(rp_last_syl_ou, word['infl']):
            actend = 'lo'
        else:
            actend = 'hi'
        
        for p in ending[actend]:
            ret.append({'infl': word['infl'] + p , 'src': word['src']})
    elif paradigm == 'z-ind':
        ending = {'mış': ['ım','sın','','ız','sınız','lar']
                 ,'miş': ['im','sin','','iz','siniz','ler']
                 ,'muş': ['um','sun','','uz','sunuz','lar']
                 ,'müş': ['üm','sün','','üz','sünüz','ler']}
        actend = word['infl'][len(word['infl'])-3:]
        for p in ending[actend]:
            ret.append({'infl': word['infl'] + p , 'src': word['src']})
    elif paradigm == 'k-ind-pt':
        ending = {'mışt': ['ım','ın','ı','ık','ınız','ılar']
                 ,'mişt': ['im','in','i','ik','iniz','iler']
                 ,'muşt': ['um','un','u','uk','unuz','ular']
                 ,'müşt': ['üm','ün','ü','ük','ünüz','üler']}
        actend = word['infl'][len(word['infl'])-4:]
        for p in ending[actend]:
            ret.append({'infl': word['infl'] + p , 'src': word['src']})
    elif paradigm == 'k-pt':
        pm = []
        if mx['last_syl_ai']:
            pm = ['m','n','','k','nız','lar']
        elif mx['last_syl_ei']:
            pm = ['m','n','','k','niz','ler']
        elif mx['last_syl_ou']:
            pm = ['m','n','','k','nuz','lar']
        elif mx['last_syl_öü']:
            pm = ['m','n','','k','nüz','ler']
        stem = word['infl']
        for p in pm:
            ret.append({'infl': stem + p , 'src': word['src']})
        #bonus: -lArdI
        bonus = stem
        if mx['last_syl_ai'] or mx['last_syl_ou']:
            bonus = word['infl'][:len(word['infl'])-2] + 'lardı'
        else:
            bonus = word['infl'][:len(word['infl'])-2] + 'lerdi'
        #print(f"{stem} -> bonus: {bonus}")
        ret.append({'infl': bonus , 'src': word['src']})
    elif paradigm == 'z-aor':
        pm = []
        if mx['last_syl_ai']:
            pm = ['ım','sın','','ız','sınız','lar']
        elif mx['last_syl_ei']:
            pm = ['im','sin','','iz','siniz','ler']
        elif mx['last_syl_ou']:
            pm = ['um','sun','','uz','sunuz','lar']
        elif mx['last_syl_öü']:
            pm = ['üm','sün','','üz','sünüz','ler']
        stem = word['infl']
        for p in pm:
            ret.append({'infl': stem + p , 'src': word['src']})
        #print([word, pm, mx['last_syl_ai']])
    elif paradigm == 'z-aor-neg':
        pm = []
        if mx['last_syl_ai']:
            pm = ['m','zsın','z','yız','zsınız','zlar']
        elif mx['last_syl_ei']:
            pm = ['m','zsin','z','yiz','zsiniz','zler']
        elif mx['last_syl_ou']:
            pm = ['m','zsun','z','yuz','zsunuz','zlar']
        elif mx['last_syl_öü']:
            pm = ['m','zsün','z','yüz','zsünüz','zler']
        stem = word['infl']
        for p in pm:
            ret.append({'infl': stem + p , 'src': word['src']})
    elif paradigm == 'z-imp':
        pm = []
        if mx['last_syl_ai']:
            pm = ['','sın','ın','ınız','sınlar']
        elif mx['last_syl_ei']:
            pm = ['','sin','in','iniz','sinler']
        elif mx['last_syl_ou']:
            pm = ['','sun','un','unuz','sunlar']
        elif mx['last_syl_öü']:
            pm = ['','sün','ün','ünüz','sünler']
            
        stem = word['infl']
        
        lastletter = stem[len(stem)-1:]
        altstem = stem
        if lastletter in ALTERNATING_CONSONANTS:
            chg = ALTERNATING_CONSONANTS[lastletter]
            altstem = stem[:len(stem)-1] + chg
        elif mx['ends_vow']:
            altstem = stem + 'y'
                    
        for p in pm:
            if p and p[0] in ['ı','i','u','ü']:
                ret.append({'infl': altstem + p , 'src': word['src']})
            else:
                ret.append({'infl': stem + p , 'src': word['src']})
    elif paradigm == 'm-opt':
        pm = []
        if mx['last_syl_low']:
            pm = ['yım','sın','','lım','sınız','lar']
        elif mx['last_syl_ei']:
            pm = ['yim','sin','','lim','siniz','ler']
            
        stem = word['infl']
        for p in pm:
            ret.append({'infl': stem + p , 'src': word['src']})
    elif paradigm == 'z-nec':
        pm = []
        if mx['last_syl_low']:
            pm = ['yım','sın','','yız','sınız','lar']
        else:
            pm = ['yim','sin','','yiz','siniz','iler']
        stem = word['infl']
        for p in pm:
            ret.append({'infl': stem + p , 'src': word['src']})
        
    return ret

def getNounPossessives(stem, mx):

    infl = []
    
    stempos = noun.getPossessive(stem,mx)

    plr = noun.getPlural(stem, mx)
    plrout = getMx(plr['infl'], noun.rps)
    plrpos = noun.getPossessive(plr,plrout)

    infl= infl + stempos + plrpos
    for a in stempos + plrpos:
        aout = getMx(a['infl'], noun.rps)
        infl.append(noun.getAccusative(a,aout))
        infl.append(noun.getDative(a,aout))
        infl.append(noun.getGenitive(a,aout))
        infl.append(noun.getKi(noun.getGenitive(a,aout)))
        infl.append(noun.getWith(a,aout))
        infl.append(noun.getPredicative(a,aout))
        infl.append(noun.getAblative(a,aout))
        infl.append(noun.getKi(noun.getAblative(a,aout)))
        infl.append(noun.getLocative(a,aout))
        infl.append(noun.getKi(noun.getLocative(a,aout)))
        nind = noun.getIndirect(a,aout)
        nindout = getMx(nind['infl'], noun.rps)
        infl.append(noun.getPredicative(nind,nindout))
        nindpm = noun.getPersonMarker(nind,nindout,'z-nind')
        nindpt = noun.getPast(nind,nindout)
        nindptout = getMx(nindpt['infl'], noun.rps)
        infl.append(noun.getPredicative(nindpt,nindptout))
        nindptpm = noun.getPersonMarker(nindpt,nindout,'k-pt')
        
        infl = infl + nindpm + nindptpm

    return infl

def processCont(w):

    infl = []

    prstem = getStem(w, 'Cont')

    #Continuous (y)Iyor
    ##Affirmative Continuous
    ###Affirmative Continuous Present
    prstemout = getMx(prstem, rp_stem)
    cont = getContinuous({'infl': prstem, 'src': None},prstemout)
    contpt = getPast(cont, None)
    
    cont['src'] = getSrc(cont, 'Pr')
    prcontpm = getPersonMarker(cont, 'cont-z-pr')
    infl = infl + prcontpm
    
    ###Affirmative Continuous Past
    ptcontpm = getPersonMarker(contpt, 'cont-k-pt')
    infl = infl + ptcontpm
    
    ##Negative Continuous
    ###Negative Continuous Present
    negstem = getStem(w, 'Neg-Cont')
    negstemout = getMx(negstem, rp_stem)
    contneg = getContinuous({'infl': negstem, 'src': 'Neg'},negstemout)
    contnegpt = getPast(contneg, None)
    
    contneg['src'] = getSrc(contneg, 'Pr')
    contnegpm = getPersonMarker(contneg, 'cont-z-pr')
    infl = infl + contnegpm
    
    ###Negative Continuous Past
    contnegptpm = getPersonMarker(contnegpt, 'cont-k-pt')
    infl = infl + contnegptpm    

    #Indirect continuous
    icontstem = cont['infl']
    icontout = getMx(icontstem, rp_stem)
    icont = getIndirect(cont, icontout)
    icontpm = getPersonMarker(icont, 'cont-z-pr')

    infl = infl + icontpm

    #Conditional
    contstem = cont['infl']
    contstemout = getMx(contstem, rp_stem)
    contcond = getConditional(cont, contstemout)
    contcondpm = getPersonMarker(contcond, 'k-pt')

    infl = infl + contcondpm
    
    return infl

def processFut(w):

    infl = []
    
    #Future
    ##Affirmative future +in-the-past +indirect
    fustem = getStem(w, 'Fut')
    fustemout = getMx(fustem, rp_stem)
    fut = getFuture({'infl': fustem, 'src': None},fustemout)
    futpt = getPast(fut, None)
    
    futpm = getPersonMarker(fut, 'z-fut')
    futptpm = getPersonMarker(futpt, 'k-pt')
    
    infl = infl + futpm
    infl = infl + futptpm
    
    futindstem = getFuture({'infl': fustem, 'src': None},fustemout)['infl']
    futindstemout = getMx(futindstem, rp_stem)
    futind = getIndirect(getFuture({'infl': fustem, 'src': None},fustemout),futindstemout)
    
    futindpm = getPersonMarker(futind, 'z-ind')
    infl = infl + futindpm

    ##Relative future: (y)AcAk + noun cases
    fustem = getStem(w, 'Fut')
    fustemout = getMx(fustem, rp_stem)
    relfut = getFuture({'infl': fustem, 'src': None},fustemout)
    relfutout = getMx(relfut['infl'], noun.rps)
    infl = infl + getRelClauses(relfut, relfutout)
    
    ###Noun Possessives
    infl = infl + getNounPossessives(relfut,relfutout)
    
    return infl

def processNeg(w):

    infl = []
    
    ##Relative clauses on the negative infinitive -mAk
    neginf = getStem(w, 'Neg')
    if neginf[len(neginf)-1:] == 'a':
        neginf = neginf + 'mak'
    else:
        neginf = neginf + 'mek'
    neginfout = getMx(neginf, noun.rps)
    neginfrel = getRelClauses({'infl': neginf, 'src': 'Neg'}, neginfout)

    infl = infl + [{'infl': neginf, 'src': 'Neg'}] + neginfrel

    ##Relative clauses + possessives on the negative infinitive -mA
    neginf2stem = getStem(neginf, 'Neg')
    neginf2out = getMx(neginf2stem, noun.rps)
    neginf2rel = getRelClauses({'infl': neginf2stem, 'src': 'Neg'}, neginf2out)
    neginf2pos = getNounPossessives({'infl': neginf2stem, 'src': 'Neg'}, neginf2out)

    infl = infl + neginf2rel + neginf2pos

    ##Negative future +in-the-pastnegstem = getNegStem(w) +indirect
    negstem1 = getStem(w, 'Neg')
    negstem1out = getMx(negstem1, rp_stem)
    futneg = getFuture({'infl': negstem1, 'src': 'Neg'},negstem1out)
    #print(f"w :: negstem1={negstem1} , futneg={futneg}")
    futnegpt = getPast(futneg, None)
    
    futnegpm = getPersonMarker(futneg, 'z-fut')
    futnegptpm = getPersonMarker(futnegpt, 'k-pt')
    
    infl = infl + futnegpm
    infl = infl + futnegptpm
    
    futnegindstem = getFuture({'infl': negstem1, 'src': 'Neg'},negstem1out)['infl']
    futnegindstemout = getMx(futnegindstem, rp_stem)
    futnegind = getIndirect(getFuture({'infl': negstem1, 'src': 'Neg'},negstem1out),futnegindstemout)
    
    futnegindpm = getPersonMarker(futnegind, 'z-ind')
    infl = infl + futnegindpm
    
    ##-mAdIkcA: Unless
    unlstem = negstem1
    unlstemout = negstem1out
    unl = getUnless({'infl': unlstem, 'src': 'Neg'},unlstemout)
    
    infl = infl + [unl]

    ## When not -IncA
    incanegstem = negstem1
    incanegout = negstem1out
    incaneg = getWhen({'infl': incanegstem, 'src': 'Neg'}, incanegout)

    infl = infl + [incaneg]

    ##Indirect Negative +past
    indneg = getIndirect({'infl': negstem1, 'src': 'Neg'},negstem1out)
    indnegpm = getPersonMarker(indneg, 'z-ind')
    indnegpt = getPast(indneg, None)
    indnegptpm = getPersonMarker(indnegpt, 'k-ind-pt')
    
    infl = infl + indnegpm
    infl = infl + indnegptpm
    
    ##Negative Simple Past
    negpt = getPast({'infl': negstem1, 'src': 'Neg'},negstem1out)
    negptpm = getPersonMarker(negpt, 'k-pt')
    infl = infl + negptpm
    
    #Negative Past + Conditional
    negptcond = getConditional(negpt, negstem1out, addy=True)
    negptcondpm = getPersonMarker(negptcond, 'k-pt')
    
    infl = infl + negptcondpm
    
    #Aorist +ken
    aorneg = {'infl': negstem1, 'src': 'Neg.Aor'}
    aornegpm = getPersonMarker(aorneg, 'z-aor-neg')
    kenneg = getKen(aorneg, mode='negative')
    infl = infl + aornegpm + [kenneg]

    ##Aorist +Conditional
    aornegcondstem = negstem1 + 'z'
    aornegcondout = getMx(aornegcondstem, rp_stem)
    aornegcond = getConditional({'infl': aornegcondstem, 'src': 'Neg.Aor'}, aornegcondout)
    aornegcondpm = getPersonMarker(aornegcond, 'k-pr')
    infl = infl + aornegcondpm
    
    #Progressive mAktA
    maktanegstem = negstem1
    maktaneg = getProgressive({'infl': maktanegstem, 'src': 'Neg'}, getMx(getStem(w), rp_stem))
    
    infl = infl + [maktaneg]
    
    #Predicative DIr +past mIstIr
    pcontnegstem = getContinuous({'infl': getStem(w, 'Neg-Cont'), 'src': 'Neg'},getMx(getStem(w, 'Neg-Cont'), rp_stem))
    pcontnegout = getMx(pcontnegstem['infl'], rp_stem)
    pmaktanegstem = maktaneg
    pmaktanegout = getMx(pmaktanegstem['infl'], rp_stem)
    pmistirnegstem = indneg
    pmistirnegout = getMx(pmistirnegstem['infl'], rp_stem)
    
    pcontneg = getPredicative(pcontnegstem, pcontnegout)
    pmaktaneg = getPredicative(pmaktanegstem, pmaktanegout)
    pmistirneg = getPredicative(pmistirnegstem, pmistirnegout)
    
    infl = infl + [pcontneg, pmaktaneg, pmistirneg]

    #Indirect continuous
    icontnegstem = getContinuous({'infl': getStem(w, 'Neg-Cont'), 'src': 'Neg'},getMx(getStem(w, 'Neg-Cont'), rp_stem))
    icontnegout = getMx(icontnegstem['infl'], rp_stem)
    icontneg = getIndirect(icontnegstem, icontnegout)
    icontnegpm = getPersonMarker(icontneg, 'cont-z-pr')

    infl = infl + icontnegpm
    
    #Imperative
    impnegstem = negstem1
    impneg = getImperative({'infl': impnegstem, 'src': 'Neg'}, None)
    impnegpm = getPersonMarker(impneg, 'z-imp')
    
    infl = infl + impnegpm
    
    #Optative
    optnegstem = negstem1
    optneg = getOptative({'infl': optnegstem, 'src': 'Neg'}, None)
    optnegpm = getPersonMarker(optneg, 'm-opt')
    
    infl = infl + optnegpm
    
    #Necessitative
    necnegstem = negstem1
    necnegstemout = negstem1out
    necneg = getNecessitative({'infl': necnegstem, 'src': None}, necnegstemout)
    necnegpm = getPersonMarker(necneg, 'z-nec')
    
    infl = infl + necnegpm
    
    ##Necessitative past
    necnegptstem = necneg['infl'] + 'y'
    necnegptstemout = getMx(necnegptstem, rp_stem)
    necnegpt = getPast({'infl': necnegptstem, 'src': necneg['src']}, necnegptstemout)
    necnegptpm = getPersonMarker(necnegpt, 'k-pt')
    
    infl = infl + necnegptpm

    ##Necessitative Predicative
    necnegpredstem = necneg['infl']
    necnegpredstemout = getMx(necnegpredstem, rp_stem)
    necnegpred = getPredicative({'infl': necnegpredstem, 'src': necneg['src']}, necnegpredstemout)
    
    infl = infl + [necnegpred]
    
    #Would (otherwise) == Aorist + Past    
    wouldnegstem = aorneg['infl'] + 'z'
    wouldnegstemout = getMx(wouldnegstem, rp_stem)
    wouldneg = getPast({'infl': wouldnegstem, 'src': aorneg['src']},wouldnegstemout)
    wouldnegpm = getPersonMarker(wouldneg, 'k-pt')
    
    infl = infl + wouldnegpm
    
    #Obligation (with mecbur)
    infl.append(getObligation(w, True))
    
    #Relative clauses
    ##Relative past: DIk + noun cases
    relnegpt = negpt
    relnegpt['infl'] = relnegpt['infl'] + 'k'
    relnegptout = getMx(relnegpt['infl'], noun.rps)
    
    infl = infl + getRelClauses(relnegpt, relnegptout)

    ###Noun Possessives +cases
    infl = infl + getNounPossessives(relnegpt,relnegptout)

    ##Relative future: (y)AcAk+ noun cases
    relnegfut = futneg
    relnegfut['infl'] = relnegfut['infl'] + 'k'
    relnegfutout = getMx(relnegfut['infl'], noun.rps)
    
    infl = infl + getRelClauses(relnegfut, relnegfutout)

    ###Noun Possessives +cases
    infl = infl + getNounPossessives(relnegfut, relnegfutout)

    #Irrealis Conditional == -sA directly after the (negative) stem
    cndnegstem = negstem1
    cndnegstemout = getMx(cndnegstem, rp_stem)
    cndneg = getConditional({'infl': cndnegstem, 'src': None}, cndnegstemout)
    cndnegpm = getPersonMarker(cndneg, 'k-pr')
    
    infl = infl + cndnegpm
    
    ##Irrealis Conditional past
    cndnegptstem = cndneg['infl'] + 'y'
    cndnegptstemout = getMx(cndnegptstem, rp_stem)
    cndnegpt = getPast({'infl': cndnegptstem, 'src': cndneg['src']}, cndnegptstemout)
    cndnegptpm = getPersonMarker(cndnegpt, 'k-pt')
    
    infl = infl + cndnegptpm
    
    #-Ing == -(y)An + Past-Ing == -dAn + by -ing == -(y)ArAk
    ingneg = getIng({'infl': negstem1, 'src': 'Neg'}, negstem1out)
    ingptnegstem = negstem1 + 'd'
    ingptnegstemout = getMx(ingptnegstem, rp_stem)
    ingptneg = getIng({'infl': ingptnegstem, 'src': 'Neg.Pt'}, ingptnegstemout)
    byingneg = getByIng({'infl': negstem1, 'src': 'Neg'}, negstem1out)
    
    infl = infl + [ingneg, byingneg, ingptneg]

    ##Noun Possessives for -(y)An
    ingnegout = getMx(ingneg['infl'], noun.rps)
    ingnegacc = noun.getAccusative(ingneg, ingnegout)
    ingnegdat = noun.getDative(ingneg, ingnegout)
    ingnegabl = noun.getAblative(ingneg, ingnegout)
    ingnegloc = noun.getLocative(ingneg, ingnegout)

    infl = infl + [ingnegacc, ingnegdat, ingnegabl, ingnegloc]
    infl = infl + getNounPossessives(ingneg,ingnegout)
    
    return infl

def processInd(w):

    infl = []
    
    ##Indirect Affirmative +past
    indstem = getStem(w)
    indstemout = getMx(indstem, rp_stem)
    ind = getIndirect({'infl': indstem, 'src': None},indstemout)
    indpm = getPersonMarker(ind, 'z-ind')
    indpt = getPast(ind, None)
    indptpm = getPersonMarker(indpt, 'k-ind-pt')
    
    infl = infl + indpm
    infl = infl + indptpm
    
    return infl

def processPt(w):

    infl = []
    
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    pt = getPast({'infl': ptstem, 'src': None},ptstemout)
    ptpm = getPersonMarker(pt, 'k-pt')
    
    infl = infl + ptpm
    
    #Conditional
    ptcondout = getMx(pt['infl'], rp_stem)
    ptcond = getConditional(pt, ptcondout, addy=True)
    ptcondpm = getPersonMarker(ptcond, 'k-pr')
    
    infl = infl + ptcondpm

    #Relative clauses
    ##Relative past: DIk + noun cases
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    pt = getPast({'infl': ptstem, 'src': None},ptstemout)
    relpt = pt
    relpt['infl'] = relpt['infl'] + 'k'
    relptout = getMx(relpt['infl'], noun.rps)
    
    #infl = infl + [relptacc, relptdat, relptabl, relptloc]
    relptn = getRelClauses(relpt, relptout)
    infl = infl + relptn

    ###Noun Possessives +cases
    relptpos = getNounPossessives(relpt, relptout)
    infl = infl + relptpos
    
    return infl

def processAor(w):

    infl = []
    
    #Aorist +ken
    aorstem = getStem(w)
    aorstemout = getMx(aorstem, rp_stem)
    aor = getAorist({'infl': aorstem, 'src': None}, aorstemout)
    aorpm = getPersonMarker(aor, 'z-aor')
    ken = getKen(aor)
    
    infl = infl + aorpm + [ken]
    
    #Would (otherwise) == Aorist + Past
    wouldstemout = getMx(aor['infl'], rp_stem)
    would = getPast(aor,wouldstemout)
    wouldpm = getPersonMarker(would, 'k-pt')
    
    infl = infl + wouldpm

    #Aorist + Conditional == Realis condition
    aorstem = aor['infl']
    aorcond = getConditional(aor, wouldstemout)
    aorcondpm = getPersonMarker(aorcond, 'k-pr')
    
    infl = infl + aorcondpm
    
    return infl

def processCannot(w):

    infl = []
            
    #Cannot = Stem+(y)a/e+Neg+Tense+PersonMarker
    cantstem = getStem(w, 'Can')
    cantstemout = getMx(cantstem, rp_stem)
    cantdf = getCannotDictForm({'infl': cantstem, 'src': None}, cantstemout)
    cantcontstem = getStem(cantdf['infl'], 'Cont')
    cantcontstemout = getMx(cantcontstem, rp_stem)
    cantcont = getContinuous({'infl': cantcontstem, 'src': cantdf['src']},cantcontstemout)
    cantcontpt = getPast(cantcont, None)
    cantcont['src'] = getSrc(cantcont, 'Pr')
    
    cantcontpm = getPersonMarker(cantcont, 'cont-z-pr')
    cantcontptpm = getPersonMarker(cantcontpt, 'cont-k-pt')
    
    infl = infl + cantcontpm + cantcontptpm
    
    cantfutstem = getFutureStem(cantdf['infl'])
    cantfutstemout = getMx(cantfutstem, rp_stem)
    cantfut = getFuture({'infl': cantfutstem, 'src': cantdf['src']},cantfutstemout)
    cantfutpt = getPast(cantfut, None)
    
    cantfutpm = getPersonMarker(cantfut, 'z-fut')
    cantfutptpm = getPersonMarker(cantfutpt, 'k-pt')
    
    infl = infl + cantfutpm + cantfutptpm
    
    cantindstem = getStem(cantdf['infl'])
    cantindstemout = getMx(cantindstem, rp_stem)
    cantind = getIndirect({'infl': cantindstem, 'src': cantdf['src']},cantindstemout)
    cantindpm = getPersonMarker(cantind, 'z-ind')
    cantindpt = getPast(cantind, None)
    cantindptpm = getPersonMarker(cantindpt, 'k-ind-pt')
    
    infl = infl + cantindpm + cantindptpm
    
    cantptstem = cantindstem
    cantptstemout = getMx(cantptstem, rp_stem)
    cantpt = getPast({'infl': cantptstem, 'src': cantdf['src']},cantptstemout)
    cantptpm = getPersonMarker(cantpt, 'k-pt')
    
    infl = infl + cantptpm
    
    cantaorstem = cantptstem
    cantaorstemout = getMx(cantaorstem, rp_stem)
    cantaor = getAoristCant({'infl': cantaorstem, 'src': cantdf['src']}, cantaorstemout)
    cantaorpm = getPersonMarker(cantaor, 'z-aor-neg')
    
    infl = infl + cantaorpm
    
    #-Ing == -(y)An + by -ing == -(y)ArAk
    cantingstem = getStem(cantdf['infl'])
    cantingstemout = getMx(cantingstem, rp_stem)
    canting = getIng({'infl': cantingstem, 'src': cantdf['src']}, cantingstemout)
    bycanting = getByIng({'infl': cantingstem, 'src': cantdf['src']}, cantingstemout)
    
    infl = infl + [canting, bycanting]
    
    ##Relative clauses and Noun Possessives for -(y)An
    cantingout = getMx(canting['infl'], noun.rps)
    cantingacc = noun.getAccusative(canting, cantingout)
    cantingdat = noun.getDative(canting, cantingout)
    cantingabl = noun.getAblative(canting, cantingout)
    cantingloc = noun.getLocative(canting, cantingout)

    infl = infl + [cantingacc, cantingdat, cantingabl, cantingloc]
    infl = infl + getNounPossessives(canting,cantingout)
    
    return infl

def processPot(w):

    infl = []
    
    #Potential Affirmative (y)Abil
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    potdfstem = ptstem
    potdfstemout = ptstemout
    potdf = getPotentialDictForm({'infl': potdfstem, 'src': None},potdfstemout)
    potcontstem = getStem(potdf['infl'], 'Cont')
    potcontstemout = getMx(potcontstem, rp_stem)
    potcont = getContinuous({'infl': potcontstem, 'src': potdf['src']},potcontstemout)
    potcontpt = getPast(potcont, None)
    potcont['src'] = getSrc(potcont, 'Pr')

    potcontpm = getPersonMarker(potcont, 'cont-z-pr')
    potcontptpm = getPersonMarker(potcontpt, 'cont-k-pt')

    ##Ing :: -An and -ArAk
    potingstem = getStem(potdf['infl'], 'Ing')
    potingstemout = getMx(potingstem, rp_stem)
    poting = getIng({'infl': potingstem, 'src': 'Pot'}, potingstemout)
    potingout = getMx(poting['infl'], noun.rps)   
    potingplr = noun.getPlural(poting, potingout)
    potbying = getByIng({'infl': potingstem, 'src': 'Pot'}, potingstemout)
    
    infl = infl + [potdf,poting,potingplr,potbying] + potcontpm + potcontptpm
    
    potfutstem = getStem(potdf['infl'], 'Fut')
    potfutstemout = getMx(potfutstem, rp_stem)
    potfut = getFuture({'infl': potfutstem, 'src': potdf['src']},potfutstemout)
    potfutpt = getPast(potfut, None)
    
    potfutpm = getPersonMarker(potfut, 'z-fut')
    potfutptpm = getPersonMarker(potfutpt, 'k-pt')
    
    infl = infl + potfutpm + potfutptpm

    ##Relative clauses and Noun Possessives
    potfutrcstem = getStem(potdf['infl'], 'Fut')
    potfutrcstemout = getMx(potfutrcstem, rp_stem)
    potfutrc = getFuture({'infl': potfutrcstem, 'src': potdf['src']},potfutrcstemout)
    potfutrcout = getMx(potfutrc['infl'], noun.rps)
    
    infl = infl + getRelClauses(potfutrc, potfutrcout)
    infl = infl + getNounPossessives(potfutrc, potfutrcout)
    
    #Potential +Indirect
    potindstem = getStem(potdf['infl'])
    potindstemout = getMx(potindstem, rp_stem)
    potind = getIndirect({'infl': potindstem, 'src': potdf['src']},potindstemout)
    potindpm = getPersonMarker(potind, 'z-ind')
    potindpt = getPast(potind, None)
    potindptpm = getPersonMarker(potindpt, 'k-ind-pt')
    
    infl = infl + potindpm + potindptpm
    
    potptstem = potindstem
    potptstemout = getMx(potptstem, rp_stem)
    potpt = getPast({'infl': potptstem, 'src': potdf['src']},potptstemout)
    potptpm = getPersonMarker(potpt, 'k-pt')
    
    infl = infl + potptpm
    
    potaorstem = potptstem
    potaorstemout = getMx(potaorstem, rp_stem)
    potaor = getAorist({'infl': potaorstem, 'src': potdf['src']}, potaorstemout)
    potaorpm = getPersonMarker(potaor, 'z-aor')
    
    infl = infl + potaorpm

    #Irrealis Conditional == -sA directly after Stem+Potential
    potcndstem = potaorstem
    potcndstemout = potaorstemout
    potcnd = getConditional({'infl': potcndstem, 'src': potdf['src']}, potcndstemout)
    potcndpm = getPersonMarker(potcnd, 'k-pr')
    
    infl = infl + potcndpm

    #Potential +Optative
    potopt = getOptative({'infl': potaorstem, 'src': potdf['src']}, potaorstemout)
    potoptpm = getPersonMarker(potopt, 'm-opt')
    
    infl = infl + potoptpm
    
    return infl

def processVerb(w):

    infl = []

    #Continuous
    infl = infl + processCont(w)
    
    #Future
    infl = infl + processFut(w)
    
    #Negative
    infl = infl + processNeg(w)
    
    #Indirect
    infl = infl + processInd(w)
    
    #Past
    infl = infl + processPt(w)
    
    #Aorist +ken
    infl = infl + processAor(w)
    
    #Cannot = Stem+(y)a/e+Neg+Tense+PersonMarker
    infl = infl + processCannot(w)
    
    #Potential Affirmative (y)Abil
    infl = infl + processPot(w)
    
    #Other cases/tenses
    
    #Progressive mAktA + Past mAktAydI
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    maktastem = ptstem
    maktastemout = ptstemout
    makta = getProgressive({'infl': maktastem, 'src': None}, maktastemout)
    maktaptstem = makta['infl']+'y'
    maktaptstemout = getMx(maktaptstem, rp_stem)
    maktapt = getPast({'infl': maktaptstem, 'src': makta['src']}, maktaptstemout)
    
    infl = infl + [makta, maktapt]

    ##Rather == mAktA + n + sa == Progressive Conditional
    cndmaktastem = makta['infl'] + 'n'
    cndmakta = getConditional({'infl': cndmaktastem, 'src': makta['src']}, maktastemout)
    
    infl = infl + [cndmakta]
    
    #Predicative DIr +past mIstIr
    pcontstem = getContinuous({'infl': getStem(w, 'Cont'), 'src': None},getMx(getStem(w, 'Cont'), rp_stem))
    pcontout = getMx(pcontstem['infl'], rp_stem)
    pmaktastem = makta
    pmaktaout = getMx(pmaktastem['infl'], rp_stem)
    indstem = getStem(w)
    indstemout = getMx(indstem, rp_stem)
    ind = getIndirect({'infl': indstem, 'src': None},indstemout)
    pmistirstem = ind
    pmistirout = getMx(pmistirstem['infl'], rp_stem)
    
    pcont = getPredicative(pcontstem, pcontout)
    pmakta = getPredicative(pmaktastem, pmaktaout)
    pmistir = getPredicative(pmistirstem, pmistirout)
    
    infl = infl + [pcont, pmakta, pmistir]
    
    #Imperative
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    impstem = ptstem
    imp = getImperative({'infl': impstem, 'src': None}, None)
    imppm = getPersonMarker(imp, 'z-imp')
    
    infl = infl + imppm
    
    #Optative
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    optstem = ptstem
    opt = getOptative({'infl': optstem, 'src': None}, None)
    optpm = getPersonMarker(opt, 'm-opt')
    
    infl = infl + optpm
    
    #Necessitative
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    necstem = ptstem
    necstemout = ptstemout
    nec = getNecessitative({'infl': necstem, 'src': None}, necstemout)
    necpm = getPersonMarker(nec, 'z-nec')
    
    infl = infl + necpm
    
    ##Necessitative past
    necptstem = nec['infl'] + 'y'
    necptstemout = getMx(necptstem, rp_stem)
    necpt = getPast({'infl': necptstem, 'src': nec['src']}, necptstemout)
    necptpm = getPersonMarker(necpt, 'k-pt')
    
    infl = infl + necptpm

    ##Necessitative Predicative
    necpredstem = nec['infl']
    necpredstemout = getMx(necpredstem, rp_stem)
    necpred = getPredicative({'infl': necpredstem, 'src': nec['src']}, necpredstemout)
    
    infl = infl + [necpred]
    
    #Obligation (with mecbur)
    infl.append(getObligation(w))

    #Irrealis Conditional == -sA directly after the stem
    cndstem = getStem(w)
    cndstemout = getMx(cndstem, rp_stem)
    cnd = getConditional({'infl': cndstem, 'src': None}, cndstemout)
    cndpm = getPersonMarker(cnd, 'k-pr')
    
    infl = infl + cndpm
    
    ##Irrealis Conditional past
    cndptstem = cnd['infl'] + 'y'
    cndptstemout = getMx(cndptstem, rp_stem)
    cndpt = getPast({'infl': cndptstem, 'src': cnd['src']}, cndptstemout)
    cndptpm = getPersonMarker(cndpt, 'k-pt')
    
    infl = infl + cndptpm
    
    #-Ip
    ipstem = getStem(w, 'Ip')
    ipstemout = getMx(ipstem, rp_stem)
    ip = getIp({'infl': ipstem, 'src': None}, ipstemout)
    
    infl = infl + [ip]
    
    #-Ing == -(y)An + by -ing == -(y)ArAk
    ingstem = getStem(w, 'Ing')
    ingstemout = getMx(ingstem, rp_stem)
    ing = getIng({'infl': ingstem, 'src': None}, ingstemout)
    ingout = getMx(ing['infl'], noun.rps)   
    ingplr = noun.getPlural(ing, ingout)
    bying = getByIng({'infl': ingstem, 'src': None}, ingstemout)
    
    infl = infl + [ing, ingplr, bying]

    ##Noun Possessives for -(y)An
    ingout = getMx(ing['infl'], noun.rps)
    ingacc = noun.getAccusative(ing, ingout)
    ingdat = noun.getDative(ing, ingout)
    ingabl = noun.getAblative(ing, ingout)
    ingloc = noun.getLocative(ing, ingout)

    infl = infl + [ingacc, ingdat, ingabl, ingloc]
    infl = infl + getNounPossessives(ing,ingout)

    ## As -dIkcA
    dikcastem = getStem(w)
    dikcaout = getMx(dikcastem, rp_stem)
    dikca = getAs({'infl': dikcastem, 'src': None}, dikcaout)

    infl = infl + [dikca]

    ## When -IncA
    incastem = getStem(w)
    incaout = getMx(incastem, rp_stem)
    inca = getWhen({'infl': incastem, 'src': None}, incaout)

    infl = infl + [inca]

    ##Relative clauses on the infinitive -mAk
    inf = w
    infout = getMx(w, noun.rps)
    infrel = getRelClauses({'infl': inf, 'src': None}, infout)

    infl = infl + infrel

    ##Relative clauses + possessives on the infinitive -mA
    inf2stem = getStem(w, 'Neg')
    inf2out = getMx(inf2stem, noun.rps)
    inf2rel = getRelClauses({'infl': inf2stem, 'src': None}, inf2out)
    inf2pos = getNounPossessives({'infl': inf2stem, 'src': None}, inf2out)
    
    infl = infl + inf2rel + inf2pos

    #wtype = noun in all cases
    for i in infl:
        i['wtype'] = 'verb'
    
    ret = getInflectionGroups(infl,'verb',w)
    
    return ret
    
#TEST
#for w in ['yemek', 'gitmek', 'aramak']:
#    print(f"{w} -> {processVerb(w)}")
