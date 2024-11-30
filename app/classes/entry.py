from .meaning import Meaning
from app.prcnoun import processNoun
from app.prcverb import processVerb

class Entry:
    def __init__(self, orig, meaning, wordtype, examples):
        self.orig = orig
        self.meanings = [Meaning(meaning, wordtype, examples)]
        self.inflections = {}
        
    def addMeaning(self, meaning, wordtype, examples):
        nm = Meaning(meaning, wordtype, examples)
        self.meanings.append(nm)
        
    def getOrig(self):
        return self.orig
        
    def getMeanings(self):
        return self.meanings
        
    def getInflections(self):
        return self.inflections
        
    def getMeaningsByTypes(self):
        wt = {}
        for item in self.meanings:
            t = item.getWordType()
            if t in wt:
                wt[t].append(item)
            else:
                wt[t] = [item]

        return wt
        
    def calcInflections(self):
        wt = set(map(lambda x: x.getWordType(), self.meanings))
        #print(f"calcInflections :: wt={wt}")
        if 'noun' in wt:
            self.inflections['noun'] = processNoun(self.orig)
        
        if 'verb' in wt:
            self.inflections['verb'] = processVerb(self.orig)
        
    def toJSONObj(self):
        ms = []
        for m in self.meanings:
            ms.append(m.toJSONObj())
        ii = []
        for t in self.inflections.values():
            for k in self.inflections[t].keys():
                for i in self.inflections[t][k]["infl"]:
                    ii.append(i)
        return {'o': self.orig, 'm': ms, 'i': ii}
