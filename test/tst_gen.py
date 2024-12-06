from app.tsvreader import readTSV
from app.xmlwriter import writeXML
from app.jsonwriter import writeJSON
from app.calci import calcInflections
from app.constants import *

#creates interim result (HTML) from limited input (TSV)

INFILE = 'input/dict_test_v2.tsv'
OUTFILE = 'interim_output/dict_test_v2.html'
OUTJSON = 'interim_output/dict_test_v2.json'

ENTRIES = {}
SHARED_INFLECTIONS = {}
INFLECTION_TO_HEAD = {}
HEAD_TO_ENTRY = {}
ERRORS = {}

def prD(dict):
    for k in sorted(list(dict.keys())):
        print(f"{k} :: {dict[k]}")

readTSV(INFILE, ENTRIES, ERRORS)
calcInflections(ENTRIES, INFLECTION_TO_HEAD, HEAD_TO_ENTRY, SHARED_INFLECTIONS)
writeJSON(OUTJSON, INFLECTION_TO_HEAD)
print("HEAD_TO_ENTRY:")
prD(HEAD_TO_ENTRY)
print("SHARED_INFLECTIONS:")
prD(SHARED_INFLECTIONS)
'''
---> problems: SHARED_INFLECTIONS may contain inflections that are also heads (=inflections group leader) like 'kız' or 'kara'
                      => the head of that group has to be replaced when written out
---> also todo: several shared inflections share the same group of heads, e.g.
kızdı    :: ['kız', 'kızdı']
kızdık   :: ['kız', 'kızdı']
kızdılar :: ['kız', 'kızdı']
kızdım   :: ['kız', 'kızdı']
kızdın   :: ['kız', 'kızdı']
kızdınız :: ['kız', 'kızdı']
     these should be grouped together into some 'kız+kızdı' group yielding a complex entry, 
     and added as inflections to it
'''
writeXML(OUTFILE, WORDTYPE_MAP, ENTRIES, INFLECTION_TO_HEAD, HEAD_TO_ENTRY, INFLECTION_DESC)