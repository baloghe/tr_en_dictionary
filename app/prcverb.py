import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.constants import *

def getSrc(word, actSrc):
    if word['src']:
        return word['src'] + '.' + actSrc
    else:
        return actSrc

def getStem(word):
    return word[:len(word)-3]
    
rp_stem = {'last_syl_low':rp_last_syl_low
            ,'rp_ends_cons':rp_ends_cons
            ,'last_syl_ai':rp_last_syl_ai
            ,'last_syl_ou':rp_last_syl_ou
            ,'last_syl_ei':rp_last_syl_ei
            ,'last_syl_öü':rp_last_syl_oouu
            ,'rp_ends_uüii':rp_ends_uuii
            ,'rp_ends_aeoö':rp_ends_aeoo}
            
def getProgressive(stem, mx):
    if stem['infl'] in EXCEPTIONS['PROGRESSIVE']:
        return {'infl': EXCEPTIONS['PROGRESSIVE'][stem['infl']] , 'src': getSrc(stem, 'Prog')}

    ret = stem['infl']
    if mx['rp_ends_cons'] and mx['last_syl_ai']:
        return {'infl': stem + 'ıyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_cons'] and mx['last_syl_ei']:
        return {'infl': stem + 'iyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_cons'] and mx['last_syl_ou']:
        return {'infl': stem + 'uyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_cons'] and mx['last_syl_öü']:
        return {'infl': stem + 'üyor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_uüii']:
        return {'infl': stem + 'yor', 'src': getSrc(stem, 'Prog')}
    elif mx['rp_ends_aeoö']:
        stem2 = ret[:len(ret)-1]
        #print(f"stem2: {stem2}")
        
        rp_stem2 = { 'last_syl_ai':rp_last_syl_ai
                    ,'last_syl_ou':rp_last_syl_ou
                    ,'last_syl_ei':rp_last_syl_ei
                    ,'last_syl_öü':rp_last_syl_oouu}
        stem2out = {}
        for k in rp_stem2:
            if regex.match(rp_stem2[k],stem2):
                stem2out[k]=True
            else:
                stem2out[k]=False
        if stem2out['last_syl_ai']:
            return {'infl': stem2 + 'ıyor', 'src': getSrc(stem, 'Prog')}
        elif stem2out['last_syl_ei']:
            return {'infl': stem2 + 'iyor', 'src': getSrc(stem, 'Prog')}
        elif stem2out['last_syl_ou']:
            return {'infl': stem2 + 'uyor', 'src': getSrc(stem, 'Prog')}
        elif stem2out['last_syl_öü']:
            return {'infl': stem2 + 'üyor', 'src': getSrc(stem, 'Prog')}

def getPersonMarker(word, paradigm):
    pm = {'prog-z': ['um','sun','','uz','sunuz','lar']}
    ret = []
    for p in pm[paradigm]:
        ret.append({'infl': word['infl']+p , 'src': word['src']})
        
    return ret



def processVerb(w):

    infl = []

    stem = getStem(w)
    print(f"stem: {stem}")
    
    stemout = {}
    for k in rp_stem:
        if regex.match(rp_stem[k],stem):
            stemout[k]=True
        else:
            stemout[k]=False

    prog = getProgressive({'infl': stem, 'src': None},stemout)
    progpm = getPersonMarker(prog, 'prog-z')
    infl = infl + progpm
    
    return infl
    
#TEST
#for w in ['yemek', 'gitmek', 'aramak']:
#    print(f"{w} -> {processVerb(w)}")

