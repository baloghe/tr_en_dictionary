import json

from proof.trydict import tryDict

fname = 'input/yakalamak_inflexions.txt'

def getText(inFileName):
    with open(inFileName, "r", encoding="utf8") as f:
        ret = f.read()
    return ret

tryDict('interim_output/TR_EN_prod.json', getText(fname), 'interim_output/prf_tst_found', 'interim_output/prf_tst_notfound')
