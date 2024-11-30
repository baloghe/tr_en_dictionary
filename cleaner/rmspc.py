import csv
import regex
regex.DEFAULT_VERSION = regex.VERSION1

#see if input contains potentionally non-dictionary formats

INFILE = 'input/dictv2.tsv'

ENTRIES = {}
ERRORS = {}

rp_space = regex.compile(r'.*\s+.*')

def readTSV(inFileName, outOK, outRemove):
    ok = []
    rem = []
    with open(inFileName, "r", encoding="utf8") as tsv:
        tsv_reader = csv.reader(tsv, delimiter="\t")
        i = 0
        for row in tsv_reader:
            o = row[:1][0]
            #print(o)
            if regex.match(rp_space,o):
                rem.append(row)
            else:
                ok.append(row)
        
        print(f"ReadTSV :: {inFileName} contained {len(ok)} acceptable and {len(rem)} bad records")
    
    # write acceptable rows
    with open(outOK, 'w', encoding='utf8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        for e in ok:
            writer.writerow(e)
    
    # write acceptable rows
    with open(outRemove, 'w', encoding='utf8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        for e in rem:
            writer.writerow(e)

readTSV(INFILE, 'input/ok.tsv', 'input/removed.tsv')

