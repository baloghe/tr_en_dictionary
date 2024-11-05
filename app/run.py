from app.tsvreader import readTSV
from app.xmlwriter import writeXML
from app.calci import calcInflections

from app.constants import *

INFILE = 'input/dictv2.tsv'
OUTFILE = 'interim_output/TR_EN_v2.html'

ENTRIES = {}
INFLECTION_TO_ENTRY = {}
ERRORS = {}

readTSV(INFILE, ENTRIES, ERRORS)
calcInflections(ENTRIES, INFLECTION_TO_ENTRY)
writeXML(OUTFILE, WORDTYPE_MAP, ENTRIES, INFLECTION_TO_ENTRY)
