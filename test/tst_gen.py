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
INFLECTION_TO_HEAD = {}
HEAD_TO_ENTRY = {}
ERRORS = {}

readTSV(INFILE, ENTRIES, ERRORS)
calcInflections(ENTRIES, INFLECTION_TO_HEAD, HEAD_TO_ENTRY)
writeJSON(OUTJSON, INFLECTION_TO_HEAD)
print(HEAD_TO_ENTRY)
writeXML(OUTFILE, WORDTYPE_MAP, ENTRIES, INFLECTION_TO_HEAD, HEAD_TO_ENTRY, INFLECTION_DESC)