import csv
import regex
regex.DEFAULT_VERSION = regex.VERSION1

from app.tsvreader import readTSV
from app.classes.entry import Entry

#see if input contains potentionally non-dictionary formats

INFILE = 'input/dictv2.tsv'

ENTRIES = {}
ERRORS = {}

readTSV(INFILE, ENTRIES, ERRORS)

rp_verb_ending = regex.compile(r'.*?(mak|mek)$')
rp_noun_plural = regex.compile(r'.*?(lar|ler)$')

def xor(str1, str2):
    return bool(str1) ^ bool(str2)

problems = []
problemtypes = {'verb': 0 , 'plural': 0}
#verbproblems = list(filter(lambda x: xor('verb' in x.getMeaningsByTypes() , regex.match(rp_verb_ending,x.getOrig())), ENTRIES.values()))
for k, e in sorted(ENTRIES.items()):
    if xor( 'verb' in e.getMeaningsByTypes() , regex.match(rp_verb_ending,e.getOrig()) ):
        problems.append([e.getOrig() , 'verb' , bool(regex.match(rp_verb_ending,e.getOrig()))])
        problemtypes['verb'] = problemtypes['verb'] + 1
    if  'noun' in e.getMeaningsByTypes() and regex.match(rp_noun_plural,e.getOrig()):
        problems.append([e.getOrig() , 'plural' , bool(regex.match(rp_noun_plural,e.getOrig()))])
        problemtypes['plural'] = problemtypes['plural'] + 1

print(f"problems: {problemtypes}")
with open('cleaner/problems.tsv', 'w', encoding='utf8', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
    for e in problems:
        writer.writerow(e)
    
