import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.constants import *

    
rp_stem = {'last_syl_low':rp_last_syl_low
            ,'rp_ends_cons':rp_ends_cons
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
        
def getNegStem(word):
    return word[:len(word)-2]
            
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

def getPast(word, mx):
    if word['infl'][len(word['infl'])-3:] == 'yor':
        return {'infl': word['infl'] + 'du', 'src': getSrc(word, 'Pt')}

def getPersonMarker(word, paradigm):
    pm = {'prog-z-pr': ['um','sun','','uz','sunuz','lar']
		 ,'prog-k-pt': ['m','n','','k','nuz','lar']
		}
    ret = []
    for p in pm[paradigm]:
        ret.append({'infl': word['infl']+p , 'src': word['src']})
        
    return ret



def processVerb(w):

    infl = []

    prstem = getProgressiveStem(w)
    negstem = getNegStem(w)
    
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
    
    ptprogpm = getPersonMarker(progpt, 'prog-z-pr')
    infl = infl + ptprogpm
    
    negstemout = {}
    for k in rp_stem:
        if regex.match(rp_stem[k],negstem):
            negstemout[k]=True
        else:
            negstemout[k]=False
    prog = getProgressive({'infl': negstem, 'src': 'Neg'},negstemout)
    progpt = getPast(prog, None)
    
    prog['src'] = getSrc(prog, 'Pr')
    prprogpm = getPersonMarker(prog, 'prog-k-pt')
    infl = infl + prprogpm
    
    ptprogpm = getPersonMarker(progpt, 'prog-k-pt')
    infl = infl + ptprogpm
    
    return infl
    
#TEST
#for w in ['yemek', 'gitmek', 'aramak']:
#    print(f"{w} -> {processVerb(w)}")

