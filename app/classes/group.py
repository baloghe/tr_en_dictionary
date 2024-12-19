class Group:
    def __init__(self, id, inHead, inPageLst, inInfls, inExact):
        self.id = id
        self.head = inHead
        self.pages = inPageLst    # list( {orig: "orig word", inflGrps: ["OTH" or "Pt.Abl...."], mbytp: Entry.getMeaningsByTypes() } )
        self.inflections = inInfls
        self.exactInfls = inExact
    
    def getId(self):
        return self.id
    
    def isValid(self):
        return (self.head != None and self.head !='')
    
    def getPages(self):
        return self.pages
    
    def getHead(self):
        return self.head
    
    def getInflections(self):
        return self.inflections
    
    def getExactInflections(self):
        return self.exactInfls
