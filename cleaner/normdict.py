import csv
import regex
regex.DEFAULT_VERSION = regex.VERSION1

import sys

from app.constants import alphaSort, WORDTYPE_MAP

INFILE  = sys.argv[1]
if len(sys.argv) > 3:
    OUTOK = sys.argv[2]
    OUTREM = sys.argv[3]
    print(f"will write normalized records in a new file called {OUTOK}")
else:
    OUTOK = INFILE
    OUTREM = sys.argv[2]
    print(f"will overwrite {INFILE} with normalized records")

rp_space = regex.compile(r'.*\s+.*')

def writeTSV(outFileName, inLines):
    with open(outFileName, 'w', encoding="UTF-8") as f:
        for line in alphaSort(inLines):
            line2 = ""
            for a in line:
                if line2:
                    line2 = line2 + "\t" + a
                else:
                    line2 = a
            f.write("%s\n" % line2)
    print(f"{outFileName} successfully written")

def readTSV(inFileName, outOK, outRemove):
    ok = []
    rem = []
    keyset = {}
    with open(inFileName, "r", encoding="utf8") as tsv:
        tsv_reader = csv.reader(tsv, delimiter="\t")
        i = 0
        for row in tsv_reader:            
            i = i+1
            if len(row) < 3 or len(row[2]) == 0:
                # discard rows without a translation and a type
                rem.append(row)
            else:
                (o, m, t) = row[:3]
                x = row[3:]
                try:
                    if regex.match(rp_space,o):
                        # discard rows where orig contains space
                        rem.append(row)
                    elif t not in WORDTYPE_MAP:
                        # discard rows with an invalid type
                        rem.append(row)
                    else:
                        key = o + "#" + m + "#" + t
                        value = [o,m,t] + x
                        if key in keyset:
                            actv = keyset[key]
                            if len(actv) < len(value):
                                keyset[key] = value
                                # discard shorter rows (previously read) on key collision
                                rem.append(actv)
                            else:
                                # discard shorter rows (actually read) on key collision
                                rem.append(value)
                        else:
                            keyset[key] = value
                except:
                    print(f"ERROR: {o}#{m}#{t}")
            
        for (k,v) in keyset.items():
            ok.append(v)

        print(f"ReadTSV :: {inFileName} contained {len(ok)} acceptable and {len(rem)} bad records")
    
    # write acceptable rows
    writeTSV(outOK, alphaSort(ok))
    
    # write acceptable rows
    writeTSV(outRemove, alphaSort(rem))

readTSV(INFILE, OUTOK, OUTREM)
