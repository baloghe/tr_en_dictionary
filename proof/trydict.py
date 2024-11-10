import json
import re

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

def tryDict(inJsonFileName, inText, outFoundFileName, outNotFoundFileName):
    INFL = getInflections(inJsonFileName)
   
    DWORD = getDistinctWords(inText)
    print(f"tryDict :: {len(INFL)} inflections against {len(DWORD)} distinct words:")
    
    FOUND = []
    NOTFOUND = []
    for k,cnt in DWORD.items():
        found = False
        if k in INFL:
            FOUND.append([k,cnt])
        else:
            NOTFOUND.append([k,cnt])
        if(k=='aldım'):
            print(f"aldım :: {found}")
            
    print(f"FOUND: {len(FOUND)} words, still MISSING: {len(NOTFOUND)}")

    #print(FOUND)
    writeResult(outFoundFileName, FOUND)
    writeResult(outNotFoundFileName, NOTFOUND)
