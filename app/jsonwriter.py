import json

def writeJSON(outFileName, inGroups):
    j = []
    for (id,e) in inGroups.items():
        #j.append(e.toJSONObj())
        if e.isValid():
            j = j + e.getInflections()
            # print(len(j))
            j.append(e.getHead())
    j = list(set(j))
    print(f"{len(j)} inflections detected")
    with open(outFileName, "w", encoding='UTF-8') as outfile:
        json.dump(j, outfile, ensure_ascii=False)
    print(f"JSON successfully created: {outFileName}")
