import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.constants import *

    
rp_stem = {'last_syl_low':rp_last_syl_low
            ,'rp_ends_cons':rp_ends_cons
            ,'rp_ends_vow':rp_ends_vow
            ,'last_syl_ai':rp_last_syl_ai
            ,'last_syl_ou':rp_last_syl_ou
            ,'last_syl_ei':rp_last_syl_ei
            ,'last_syl_öü':rp_last_syl_oouu
            ,'rp_ends_uüii':rp_ends_uuii
            ,'rp_ends_aeoö':rp_ends_aeoo}

def getSrc(word, actSrc):
    if word['src']:
        return word['src'] + '.' + actSrc
    else:
        return actSrc

def getStem(word):
    return word[:len(word)-3]

def getProgressiveStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['PROGRESSIVE_STEM']:
        return EXCEPTIONS['PROGRESSIVE_STEM'][stem]
    
    if regex.match(rp_ends_aeoo, stem):
        return stem[:len(stem)-1]
    else:
        return stem
        
def getFutureStem(word):
    stem = getStem(word)
    
    if stem in EXCEPTIONS['PROGRESSIVE_STEM']:
        return EXCEPTIONS['PROGRESSIVE_STEM'][stem]
    else:
        return stem
        
def getNegStem(word):
    return word[:len(word)-2]

def getNegStem1(word):
    return word[:len(word)-1]
            
def getProgressive(stem, mx):
    if stem['infl'] in EXCEPTIONS['PROGRESSIVE']:
        return {'infl': EXCEPTIONS['PROGRESSIVE'][stem['infl']] , 'src': getSrc(stem, 'Prog')}

    ret = stem['infl']
    if mx['rp_ends_cons'] and mx['last_syl_ai']:
        return {'infl': ret + 'ıyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_cons'] and mx['last_syl_ei']:
        return {'infl': ret + 'iyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_cons'] and mx['last_syl_ou']:
        return {'infl': ret + 'uyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_cons'] and mx['last_syl_öü']:
        return {'infl': ret + 'üyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_uüii']:
        return {'infl': ret + 'yor', 'src': getSrc(stem, 'Prog')}
            
def getFuture(stem, mx):
    if stem['infl'] in EXCEPTIONS['FUTURE']:
        return {'infl': EXCEPTIONS['FUTURE'][stem['infl']] , 'src': getSrc(stem, 'Fut')}

    ret = stem['infl']
    if mx['rp_ends_vow']:
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

def getPersonMarker(word, paradigm):
    pm = {'prog-z-pr': ['um','sun','','uz','sunuz','lar']
         ,'prog-k-pt': ['m','n','','k','nuz','lar']
        }
    ret = []
    if paradigm in ['prog-z-pr', 'prog-k-pt']:
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
        
    return ret



def processVerb(w):

    infl = []

    prstem = getProgressiveStem(w)

    #Progressive
    ##Affirmative Progressive
    ###Affirmative Progressive Present
    prstemout = {}
    for k in rp_stem:
        if regex.match(rp_stem[k],prstem):
            prstemout[k]=True
        else:
            prstemout[k]=False

    prog = getProgressive({'infl': prstem, 'src': None},prstemout)
    progpt = getPast(prog, None)
    
    prog['src'] = getSrc(prog, 'Pr')
    prprogpm = getPersonMarker(prog, 'prog-z-pr')
    infl = infl + prprogpm
    
    ###Affirmative Progressive Past
    ptprogpm = getPersonMarker(progpt, 'prog-k-pt')
    infl = infl + ptprogpm
    
    ##Negative Progressive
    ###Negative Progressive Present
    negstem = getNegStem(w)
    negstemout = {}
    for k in rp_stem:
        if regex.match(rp_stem[k],negstem):
            negstemout[k]=True
        else:
            negstemout[k]=False
    prog = getProgressive({'infl': negstem, 'src': 'Neg'},negstemout)
    progpt = getPast(prog, None)
    
    prog['src'] = getSrc(prog, 'Pr')
    prprogpm = getPersonMarker(prog, 'prog-z-pr')
    infl = infl + prprogpm
    
    ###Negative Progressive Past
    ptprogpm = getPersonMarker(progpt, 'prog-k-pt')
    infl = infl + ptprogpm
    
    #Future
    ##Affirmative future +in-the-past
    fustem = getFutureStem(w)
    fustemout = {}
    for k in rp_stem:
        if regex.match(rp_stem[k],fustem):
            fustemout[k]=True
        else:
            fustemout[k]=False

    fut = getFuture({'infl': fustem, 'src': None},fustemout)
    futpt = getPast(fut, None)
    
    futpm = getPersonMarker(fut, 'z-fut')
    futptpm = getPersonMarker(futpt, 'k-pt')
    
    infl = infl + futpm
    infl = infl + futptpm
    
    ##Negative future +in-the-pastnegstem = getNegStem(w)
    negstem1 = getNegStem1(w)
    negstem1out = {}
    for k in rp_stem:
        if regex.match(rp_stem[k],negstem1):
            negstem1out[k]=True
        else:
            negstem1out[k]=False
    futneg = getFuture({'infl': negstem1, 'src': 'Neg'},negstem1out)
    #print(f"w :: negstem1={negstem1} , futneg={futneg}")
    futnegpt = getPast(futneg, None)
    
    futnegpm = getPersonMarker(futneg, 'z-fut')
    futnegptpm = getPersonMarker(futnegpt, 'k-pt')
    
    infl = infl + futnegpm
    infl = infl + futnegptpm
    
    return infl
    
#TEST
#for w in ['yemek', 'gitmek', 'aramak']:
#    print(f"{w} -> {processVerb(w)}")

