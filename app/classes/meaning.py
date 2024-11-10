class Meaning:
    def __init__(self, meaning, wordtype, examples):
        self.meaning = meaning
        self.wordtype = wordtype
        self.examples = examples
        
    def getMeaning(self):
        return self.meaning
        
    def getWordType(self):
        return self.wordtype
        
    def getExamples(self):
        return self.examples
        
    def toJSONObj(self):
        return {'m': self.meaning, 'tp': self.wordtype, 'ex': self.examples}
