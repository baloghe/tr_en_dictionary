import json
import re

from app.tsvreader import readTSV

def getInflections(inJsonFileName):
    with open(inJsonFileName, 'r', encoding='UTF-8') as f:
        return json.load(f)

def getDistinctWords(inText):
    words = re.split(r'\W+', inText.lower())
    dword = {}

    for w in sorted(words):
        if len(w) > 0:
            if w in dword:
                dword[w] = dword[w]+1
            else:
                dword[w] = 1
    
    return dword
    
def writeResult(outFileName, inArray):
    file = open(outFileName, 'w', encoding='UTF-8')
    file.writelines(list(map(lambda e: e[0] + '\t' + str(e[1]) + '\n', inArray)))
    file.close()

def tryDict(inInfls, inText, outFoundFileName, outNotFoundFileName):
       
    DWORD = getDistinctWords(inText)
    print(f"tryDict :: {len(inInfls)} inflections against {len(DWORD)} distinct words:")
    
    FOUND = []
    NOTFOUND = []
    for k,cnt in DWORD.items():
        found = False
        if k in inInfls:
            FOUND.append([k,cnt])
        else:
            NOTFOUND.append([k,cnt])
            
    print(f"FOUND: {len(FOUND)} words, still MISSING: {len(NOTFOUND)}")

    #print(FOUND)
    writeResult(outFoundFileName, FOUND)
    writeResult(outNotFoundFileName, NOTFOUND)

def tryDictJSON(inJsonFileName, inText, outFoundFileName, outNotFoundFileName):
    INFL = getInflections(inJsonFileName)
    tryDict(INFL, inText, outFoundFileName, outNotFoundFileName)

def tryDictTSV(inDictFileName, inText, outFoundFileName, outNotFoundFileName):
    ENTRIES = {}
    ERRORS = {}

    readTSV(inDictFileName, ENTRIES, ERRORS)

    for o in ENTRIES:
        try:
            ENTRIES[o].calcInflections()
        except:
            print(f"ERROR: no inflection could be calculated for Entry={o}")
    INFL = []
    for (k,e) in list(ENTRIES.items()):
        i = e.getInflections()
        for t in list(i.keys()):
            for g in list(i[t].keys()):
                for j in i[t][g]['infl']:
                    INFL.append(j['infl'])
    tryDict(INFL, inText, outFoundFileName, outNotFoundFileName)
