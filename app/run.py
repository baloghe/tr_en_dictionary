import sys

from app.tsvreader import readTSV
from app.xmlwriter import writeXML
from app.jsonwriter import writeJSON
from app.calci import calcInflections

from app.constants import *


print ('argument list', sys.argv)

if len(sys.argv) >= 4:

    INFILE = sys.argv[1]
    OUTJSON = sys.argv[2]
    OUTFILE = sys.argv[3]

    ENTRIES = {}
    ERRORS = {}

    readTSV(INFILE, ENTRIES, ERRORS)
    groups = calcInflections(ENTRIES)
    writeXML(OUTFILE, groups, WORDTYPE_MAP, INFLECTION_DESC)
    writeJSON(OUTJSON, groups)
else:
    print ('Less arguments passed than needed! exit program')
