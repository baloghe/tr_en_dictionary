import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.constants import *

    
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

def getStem(word):
    return word[:len(word)-3]

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
        
def getNegStem(word):
    return word[:len(word)-2]

def getNegStem1(word):
    return word[:len(word)-1]

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

def getPersonMarker(word, paradigm):
    pm = {'cont-z-pr': ['um','sun','','uz','sunuz','lar']
         ,'prog-k-pt': ['m','n','','k','nuz','lar']
        }
    
    mx = getMx(word['infl'],rp_stem)
        
    ret = []
    if paradigm in ['cont-z-pr', 'prog-k-pt']:
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
        
    return ret

def processVerb(w):

    infl = []

    prstem = getContinuousStem(w)

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
    negstem = getNegStem(w)
    negstemout = getMx(negstem, rp_stem)
    contneg = getContinuous({'infl': negstem, 'src': 'Neg'},negstemout)
    contnegpt = getPast(contneg, None)
    
    contneg['src'] = getSrc(contneg, 'Pr')
    contnegpm = getPersonMarker(contneg, 'cont-z-pr')
    infl = infl + contnegpm
    
    ###Negative Continuous Past
    contnegptpm = getPersonMarker(contnegpt, 'cont-k-pt')
    infl = infl + contnegptpm
    
    #Future
    ##Affirmative future +in-the-past
    fustem = getFutureStem(w)
    fustemout = getMx(fustem, rp_stem)
    fut = getFuture({'infl': fustem, 'src': None},fustemout)
    futpt = getPast(fut, None)
    
    futpm = getPersonMarker(fut, 'z-fut')
    futptpm = getPersonMarker(futpt, 'k-pt')
    
    infl = infl + futpm
    infl = infl + futptpm
    
    ##Negative future +in-the-pastnegstem = getNegStem(w)
    negstem1 = getNegStem1(w)
    negstem1out = getMx(negstem1, rp_stem)
    futneg = getFuture({'infl': negstem1, 'src': 'Neg'},negstem1out)
    #print(f"w :: negstem1={negstem1} , futneg={futneg}")
    futnegpt = getPast(futneg, None)
    
    futnegpm = getPersonMarker(futneg, 'z-fut')
    futnegptpm = getPersonMarker(futnegpt, 'k-pt')
    
    infl = infl + futnegpm
    infl = infl + futnegptpm
    
    #Indirect
    ##Indirect Affirmative +past
    indstem = getStem(w)
    indstemout = getMx(indstem, rp_stem)
    ind = getIndirect({'infl': indstem, 'src': None},indstemout)
    indpm = getPersonMarker(ind, 'z-ind')
    indpt = getPast(ind, None)
    indptpm = getPersonMarker(indpt, 'k-ind-pt')
    
    infl = infl + indpm
    infl = infl + indptpm
    
    ##Indirect Negative +past
    indneg = getIndirect({'infl': negstem1, 'src': 'Neg'},negstem1out)
    indnegpm = getPersonMarker(indneg, 'z-ind')
    indnegpt = getPast(indneg, None)
    indnegptpm = getPersonMarker(indnegpt, 'k-ind-pt')
    
    infl = infl + indnegpm
    infl = infl + indnegptpm
    
    #Past
    ptstem = getStem(w)
    ptstemout = getMx(ptstem, rp_stem)
    pt = getPast({'infl': ptstem, 'src': None},ptstemout)
    negpt = getPast({'infl': negstem1, 'src': 'Neg'},negstem1out)
    ptpm = getPersonMarker(pt, 'k-pt')
    negptpm = getPersonMarker(negpt, 'k-pt')
    
    infl = infl + ptpm + negptpm
    
    #Aorist +ken
    aorstem = ptstem
    aorstemout = ptstemout
    aor = getAorist({'infl': aorstem, 'src': None}, aorstemout)
    aorneg = {'infl': negstem1, 'src': 'Neg.Aor'}
    aorpm = getPersonMarker(aor, 'z-aor')
    aornegpm = getPersonMarker(aorneg, 'z-aor-neg')
    ken = getKen(aor)
    kenneg = getKen(aorneg, mode='negative')
    
    infl = infl + aorpm + aornegpm + [ken, kenneg]
    
    #Progressive mAktA
    maktastem = ptstem
    maktastemout = ptstemout
    makta = getProgressive({'infl': maktastem, 'src': None}, maktastemout)
    maktanegstem = negstem1
    maktaneg = getProgressive({'infl': maktanegstem, 'src': 'Neg'}, maktastemout)
    
    infl = infl + [makta, maktaneg]
    
    #Predicative DIr +past mIstIr
    pcontstem = cont
    pcontout = getMx(pcontstem['infl'], rp_stem)
    pcontnegstem = contneg
    pcontnegout = getMx(pcontnegstem['infl'], rp_stem)
    pmaktastem = makta
    pmaktaout = getMx(pmaktastem['infl'], rp_stem)
    pmaktanegstem = maktaneg
    pmaktanegout = getMx(pmaktanegstem['infl'], rp_stem)
    pmistirstem = ind
    pmistirout = getMx(pmistirstem['infl'], rp_stem)
    pmistirnegstem = indneg
    pmistirnegout = getMx(pmistirnegstem['infl'], rp_stem)
    
    pcont = getPredicative(pcontstem, pcontout)
    pcontneg = getPredicative(pcontnegstem, pcontnegout)
    pmakta = getPredicative(pmaktastem, pmaktaout)
    pmaktaneg = getPredicative(pmaktanegstem, pmaktanegout)
    pmistir = getPredicative(pmistirstem, pmistirout)
    pmistirneg = getPredicative(pmistirnegstem, pmistirnegout)
    
    infl = infl + [pcont, pcontneg, pmakta, pmaktaneg, pmistir, pmistirneg]
    
    #Imperative
    impstem = ptstem
    imp = getImperative({'infl': impstem, 'src': None}, None)
    impnegstem = negstem1
    impneg = getImperative({'infl': impnegstem, 'src': None}, None)
    imppm = getPersonMarker(imp, 'z-imp')
    impnegpm = getPersonMarker(impneg, 'z-imp')
    
    infl = infl + imppm + impnegpm
    
    #Optative
    optstem = ptstem
    opt = getOptative({'infl': optstem, 'src': None}, None)
    optnegstem = negstem1
    optneg = getOptative({'infl': optnegstem, 'src': None}, None)
    optpm = getPersonMarker(opt, 'm-opt')
    optnegpm = getPersonMarker(optneg, 'm-opt')
    
    infl = infl + optpm + optnegpm
    
    #wtype = noun in all cases
    for i in infl:
        i['wtype'] = 'verb'
    
    return infl
    
#TEST
#for w in ['yemek', 'gitmek', 'aramak']:
#    print(f"{w} -> {processVerb(w)}")

