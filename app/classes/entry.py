from .meaning import Meaning
from app.prcnoun import processNoun

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
            actinf = processNoun(self.orig)
            for i in actinf:
                if i['infl'] in self.inflections:
                    self.inflections[i['infl']].append(i)
                else:
                    self.inflections[i['infl']] = [i]
        
        if 'verb' in wt:
            actinf = processVerb(self.orig)
            for i in actinf:
                if i['infl'] in self.inflections:
                    self.inflections[i['infl']].append(i)
                else:
                    self.inflections[i['infl']] = [i]
            #print(f"self.inflections={self.inflections}")
