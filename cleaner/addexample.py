import csv
import sys

INDICTFILE = sys.argv[1]
INEXFILE = sys.argv[2]
OUTFILE = sys.argv[3]
WARNFILE = sys.argv[4]

'''
the intention is to add examples to the relevant words in the dictionary
INEXFILE :: examples to be added to one or more entries
{example} \t {orig1} [\t {orig2} ... [\t {orign}]]
where example is preferably in [TR]: [EN] fashion
      orig1, ..., orign: the entries we want to add this example to
E.g.
falan filan: etcetera   falan   filan
In this case the example "falan filan: etcetera" should be added to both 'falan' and 'filan'
E.g.
afiyet olsun! enjoy your meal!   afiyet
In this case the example "afiyet olsun! enjoy your meal!" should be added to the entry 'afiyet'

If a desired entry does not exist in the dictionary, a warning is raised indicating the missing entry.
If an example is already present at the given entry, it wouldn't be added again
'''

def readTSV(inFileName):
    lines = []
    with open(inFileName, "r", encoding="utf8") as tsv:
        tsv_reader = csv.reader(tsv, delimiter="\t")
        i = 0
        for row in tsv_reader:
            i = i+1
            lines.append(row)
        print(f"{inFileName} :: lines read: {i}")
    return lines

def addExample(e, dict):
    ret = {'success': False, 'missing': [], 'cnt': 0, 'already': 0}

    ex = e[0]
    ws = list(set(e[1:]))
    # bookkeeping of origs/filters & done
    bk = {}
    done = 0
    already = 0
    for w in ws:
        o = None
        f = None
        if '::' in w:
            (o,f) = w.split('::')
        else:
            o = w
        bk[w] = {'o':o,'f':f,'done':False}
        
    for entry in dict:
        # print(entry)
        if done >= len(ws):
            break
        for w in ws:
            if not bk[w]['done']:
                o = bk[w]['o']
                f = bk[w]['f']
                if o==entry[0]:
                    if (not f) or (f in entry[1:3]):
                        #no filter OR matches both filter and orig
                        if ex not in entry:
                            entry.append(ex)
                        else:
                            already = already + 1
                        done = done+1
                        bk[w]['done'] = True
    
    #return something helpful
    if done >= len(ws):
        ret = {'success': True, 'missing': [], 'cnt': done, 'already': already}
    else:
        notf = []
        for w in ws:
            if not bk[w]['done']:
                notf.append(w)
        ret = {'success': False, 'missing': notf, 'cnt': done, 'already': already}
    return ret

def writeTSV(outFileName, inLines):
    with open(outFileName, 'w', encoding="UTF-8") as f:
        for line in inLines:
            line2 = ""
            for a in line:
                if line2:
                    line2 = line2 + "\t" + a
                else:
                    line2 = a
            f.write("%s\n" % line2)
    print(f"{outFileName} successfully written")

DICT = readTSV(INDICTFILE)
EXAMPLES = readTSV(INEXFILE)
WARNINGS = []
cnt = 0
err = 0
alr = 0

for e in EXAMPLES:
    r = addExample(e,DICT)
    cnt = cnt + r['cnt']
    alr = alr + r['already']
    if not r['success']:
        err = err + 1
    WARNINGS.append(r['missing'])

#so...
print("Examples added:")
print(f"{cnt} matches found of which {alr} examples were already present => net addition: {cnt - alr}")
print(f"missing words: {err}")

writeTSV(OUTFILE,DICT)
writeTSV(WARNFILE,WARNINGS)
