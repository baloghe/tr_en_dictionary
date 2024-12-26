from app.prcverb import processVerb
from app.prcnoun import processNoun
from app.prcadj import processAdj

pv = processVerb('olmak')
pn = processNoun('at')
pa = processAdj('sık')

showGrp = pv
for g in showGrp.keys():
    print(f"{g} :: {len(showGrp[g]['infl'])}")

#print(showGrp['Poss'])
