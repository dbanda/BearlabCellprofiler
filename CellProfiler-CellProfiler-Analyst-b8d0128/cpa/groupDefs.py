class groupDef():
    def __init__(self):
        self.nPairs = 0
        self.pairsDict = {}
        self.plotColor = [0, 0 , 1]
        self.description = 'groupDef'
        self.validIndici = []
        self.matchCount = 0
    def setDescription(self, description):
        self.description = description
    def setPlotColor(self, color):
        self.plotColor = color
    def addPair(self, description, valueMatchingString):
        self.nPairs = self.nPairs + 1
        keyStr = description.replace(' ', '')
        self.pairsDict[keyStr] = valueMatchingString
    def updateValidIndiciFromDataColumn(self, headerStr, dataValues):
        headerStr_ = headerStr.replace (' ', '')
        #print 'Passed %s...\n', (headerStr_)
        if self.pairsDict.has_key(headerStr_):
            matchValue = self.pairsDict[headerStr_]
            #print self.pairsDict, 'hs headst' , headerStr_
            #print matchValue ,'mvsd',self.description
            self.matchCount = self.matchCount + 1
            indici = self.recursiveComparison(matchValue, dataValues)
            if self.validIndici == []:
                self.validIndici = indici
            else:
                self.validIndici = indici & self.validIndici       
    def checkMatchCount(self):
        if self.matchCount != self.nPairs:
            warning('groupDef: %s Not all pairs were successfully matched.  DATA MAY BE INCORRECT', self.description)
        if ~sum(self.validIndici):
                warning('groupDef: %s Empty set, no data will be selected for this group', self.description)
    def clearAllIndici(self):
        self.validIndici = []
        self.matchCount = 0
    def nData(self):
        n = sum(self.validIndici)
        return n
    def recursiveComparison(self, challengeStr, data):
        import numpy as np
        match_indici = np.array([False] * len(data),dtype = bool)
        for ii in range(len(data)):
            match_indici[ii] = data[ii] == challengeStr
        return match_indici
    ##print 'Data extraction error:\n%s\n',(getReport(ME)