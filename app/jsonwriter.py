import json

def writeJSON(outFileName, inInflection2Entries):
    j = []
    for e in inInflection2Entries.keys():
        #j.append(e.toJSONObj())
        j.append(e)
    with open(outFileName, "w", encoding='UTF-8') as outfile:
        json.dump(j, outfile, ensure_ascii=False)