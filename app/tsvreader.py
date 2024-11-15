import csv

from app.classes.entry import Entry

def addError(line, problem, dstErrors):
    e = None
    if line in dstErrors:
        e = dstErrors[line]
        e = e + '; ' + problem
    else:
        e = problem
    dstErrors[line] = e
    
def readTSV(inFileName, dstEntries, dstErrors):
    with open(inFileName, "r", encoding="utf8") as tsv:
        tsv_reader = csv.reader(tsv, delimiter="\t")
        i = 0
        for row in tsv_reader:
            i = i+1
            (o, m) = row[:2]
            if m is None:
                addError(i, 'missing meaning', dstErrors)
            t = None
            x = None
            if len(row) > 2:
                t = row[2]
            else:
                addError(i, 'missing word type', dstErrors)
            if len(row) > 3 and len(row[3]) > 0:
                x = row[3:]
            
            if o in dstEntries:
                e = dstEntries[o]
                e.addMeaning(m, t, x)
            else:
                e = Entry(o, m, t, x)
            dstEntries[o] = e
        
        print(f"ReadTSV :: {len(dstEntries)} entries added from {inFileName}, errors: {len(dstErrors)}")
