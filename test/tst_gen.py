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
ERRORS = {}

def prD(dict):
    for k in sorted(list(dict.keys())):
        print(f"{k} :: {dict[k]}")

readTSV(INFILE, ENTRIES, ERRORS)
groups = calcInflections(ENTRIES)
writeXML(OUTFILE, groups, WORDTYPE_MAP, INFLECTION_DESC)
writeJSON(OUTJSON, groups)
