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

def getSrc(word, actSrc):
    if word['src']:
        return word['src'] + '.' + actSrc
    else:
        return actSrc    

def getContinuousStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['CONTINUOUS_STEM']:
        return EXCEPTIONS['CONTINUOUS_STEM'][stem]
    
    if regex.match(rp_ends_aeoo, stem):
        return stem[:len(stem)-1]
    else:
        return stem
        
def getFutureStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['CONTINUOUS_STEM']:
        return EXCEPTIONS['CONTINUOUS_STEM'][stem]
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
    
    if ret in EXCEPTIONS['CONTINUOUS_STEM']:
        ret = EXCEPTIONS['CONTINUOUS_STEM'][ret]
    
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
    
    if mx['ends_vow']:
        ret = ret + 'y'
    
    if mx['last_syl_low']:
        ret = ret + 'abilmek'
    else:
        ret = ret + 'ebilmek'
    
    return {'infl': ret, 'src': getSrc(stem, 'Pot')}
    
def getPersonMarker(word, paradigm):
    pm = {'cont-z-pr': ['um','sun','','uz','sunuz','lar']
         ,'cont-k-pt': ['m','n','','k','nuz','lar']
        }
    
    mx = getMx(word['infl'],rp_stem)
        
    ret = []
    if paradigm in ['cont-z-pr', 'cont-k-pt']:
        for p in pm[paradigm]:
            ret.append({'infl': word['infl']+p , 'src': word['src']})
    elif paradigm == 'z-fut':
        ending = {'ak': ['ğım','ksın','k','ğız','ksınız','klar']
                 ,'ek': ['ğim','ksin','k','ğiz','ksiniz','kler']}
        actend = word['infl'][len(word['infl'])-2:]
        word['infl'] = word['infl'][:len(word['infl'])-1]
        
        for p in ending[actend]:
            ret.append({'infl': word['infl'] + p , 'src': word['src']})
    elif paradigm == 'k-pt':
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
    elif paradigm == 'z-aor':
        pm = []
        if mx['last_syl_ai']:
            pm = ['ım','sın','','ız','sınız','ılar']
        elif mx['last_syl_ei']:
            pm = ['im','sin','','iz','siniz','iler']
        elif mx['last_syl_ou']:
            pm = ['um','sun','','uz','sunuz','ular']
        elif mx['last_syl_öü']:
            pm = ['üm','sün','','üz','sünüz','üler']
        stem = word['infl']
        for p in pm:
            ret.append({'infl': stem + p , 'src': word['src']})
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
    relfut['infl'] = relfut['infl']
    relfutout = getMx(relfut['infl'], noun.rps)
    relfutacc = noun.getAccusative(relfut, relfutout)
    relfutdat = noun.getDative(relfut, relfutout)
    relfutabl = noun.getAblative(relfut, relfutout)
    relfutloc = noun.getLocative(relfut, relfutout)
    
    infl = infl + [relfutacc, relfutdat, relfutabl, relfutloc]

    ###Noun Possessives
    relfutpos = noun.getPossessive(relfut,relfutout)
    infl= infl + relfutpos
    for a in relfutpos:
        aout = getMx(a['infl'], noun.rps)
        infl.append(noun.getAccusative(a,aout))
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

def processNeg(w):

    infl = []
    
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
    
    #Aorist +ken
    aorneg = {'infl': negstem1, 'src': 'Neg.Aor'}
    aornegpm = getPersonMarker(aorneg, 'z-aor-neg')
    kenneg = getKen(aorneg, mode='negative')
    infl = infl + aornegpm + [kenneg]
    
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
    
    #Imperative
    impnegstem = negstem1
    impneg = getImperative({'infl': impnegstem, 'src': None}, None)
    impnegpm = getPersonMarker(impneg, 'z-imp')
    
    infl = infl + impnegpm
    
    #Optative
    optnegstem = negstem1
    optneg = getOptative({'infl': optnegstem, 'src': None}, None)
    optnegpm = getPersonMarker(optneg, 'm-opt')
    
    infl = infl + optnegpm
    
    #Necessitative
    necnegstem = negstem1
    necnegstemout = negstem1out
    necneg = getNecessitative({'infl': necnegstem, 'src': None}, necnegstemout)
    necnegpm = getPersonMarker(necneg, 'z-nec')
    
    infl = infl + necnegpm
    
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
    relnegptacc = noun.getAccusative(relnegpt, relnegptout)
    relnegptdat = noun.getDative(relnegpt, relnegptout)
    relnegptabl = noun.getAblative(relnegpt, relnegptout)
    relnegptloc = noun.getLocative(relnegpt, relnegptout)
    
    infl = infl + [relnegptacc, relnegptdat, relnegptabl, relnegptloc]
    
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

    #Relative clauses
    ##Relative past: DIk + noun cases
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    pt = getPast({'infl': ptstem, 'src': None},ptstemout)
    relpt = pt
    relpt['infl'] = relpt['infl'] + 'k'
    relptout = getMx(relpt['infl'], noun.rps)
    relptacc = noun.getAccusative(relpt, relptout)
    relptdat = noun.getDative(relpt, relptout)
    relptabl = noun.getAblative(relpt, relptout)
    relptloc = noun.getLocative(relpt, relptout)
    
    infl = infl + [relptacc, relptdat, relptabl, relptloc]

    ###Noun Possessives +cases
    relptpos = noun.getPossessive(relpt,relptout)
    infl= infl + relptpos
    for a in relptpos:
        aout = getMx(a['infl'], noun.rps)
        infl.append(noun.getAccusative(a,aout))
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
    
    return infl

def processCannot(w):

    infl = []
            
    #Cannot = Stem+(y)a/e+Neg+Tense+PersonMarker
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    cantstem = ptstem
    cantstemout = ptstemout
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
    
    infl = infl + potcontpm + potcontptpm
    
    potfutstem = getStem(potdf['infl'], 'Fut')
    potfutstemout = getMx(potfutstem, rp_stem)
    potfut = getFuture({'infl': potfutstem, 'src': potdf['src']},potfutstemout)
    potfutpt = getPast(potfut, None)
    
    potfutpm = getPersonMarker(potfut, 'z-fut')
    potfutptpm = getPersonMarker(potfutpt, 'k-pt')
    
    infl = infl + potfutpm + potfutptpm
    
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
    
    #Progressive mAktA
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    maktastem = ptstem
    maktastemout = ptstemout
    makta = getProgressive({'infl': maktastem, 'src': None}, maktastemout)
    
    infl = infl + [makta]
    
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
    
    #Obligation (with mecbur)
    infl.append(getObligation(w))

    #wtype = noun in all cases
    for i in infl:
        i['wtype'] = 'verb'
    
    return infl
    
#TEST
#for w in ['yemek', 'gitmek', 'aramak']:
#    print(f"{w} -> {processVerb(w)}")
