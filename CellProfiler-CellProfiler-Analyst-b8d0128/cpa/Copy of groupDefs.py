class groupDef():
    def __init__(self):
        self.nPairs = 0;
        self.pairsDict = {}
        self.plotColor = [0, 0 , 1];
        self.description = 'groupDef';
        self.validIndici = [];
        self.matchCount = 0;
              
    def setDescription(self, description):
        self.description = description
    def setPlotColor(self, color):
        self.plotColor = color;
      
    def addPair(self, description, valueMatchingString):
        self.nPairs = self.nPairs + 1;
        keyStr = description.replace(' ', '')
        self.pairsDict[keyStr] = valueMatchingString
        
    def updateValidIndiciFromDataColumn(self, headerStr, dataValues):
        headerStr_ = headerStr.replace (' ', '')
        #print 'Passed %s...\n', (headerStr_);
        if self.pairsDict.has_key(headerStr_):
            matchValue = self.pairsDict[headerStr_]
            self.matchCount = self.matchCount + 1;
            indici = self.recursiveComparison(matchValue, dataValues);
            if self.validIndici == []:
                self.validIndici = indici
            else:
                self.validIndici = indici & self.validIndici       
    def checkMatchCount(self):
        if self.matchCount != self.nPairs:
            warning('groupDef: %s Not all pairs were successfully matched.  DATA MAY BE INCORRECT', self.description);
        if ~sum(self.validIndici):
                warning('groupDef: %s Empty set, no data will be selected for this group', self.description);

    def clearAllIndici(self):
        self.validIndici = [];
        self.matchCount = 0;
        
    def nData(self):
        n = sum(self.validIndici);
        return n
        
    def recursiveComparison(self, challengeStr, data):
        import numpy as np
        import re as re
        #print challengeStr
        #print data
        #[parts, ind] = re.match(challengeStr, '&', 'once', 'split');
        parts= challengeStr
        ind = False
        if ind:
            match_indici = self.recursiveComparison(parts[0], data) 
            self.recursiveComparison(parts[1], data)
            #return
        #[parts, ind] = regexp(challengeStr, '\|', 'once', 'split');
        if ind:
            match_indici = self.recursiveComparison(parts[1], data)
            self.recursiveComparison(parts[2], data);
            #return
        notFlag = False
        index = re.match(challengeStr,'~')
        if index == 1:
            challengeStr = challengeStr[index + 1:end];
            notFlag = true;
#        elif ~isempty(index):
#            error('recursiveComparison: NOT operator must be in position 1');
#        index = regexp(challengeStr, '[><]=');
#        if ~isempty(index):
#            operator = challengeStr[index:index + 1];
#            challengeStr = challengeStr[index + 2:end];
#        index = regexp[challengeStr, '[><]'];
#        if ~isempty(index):
##            operator = challengeStr[index];
##            challengeStr = challengeStr[index + 1:end];
#        
#        if exist('operator', 'var'):
#            if index != 1:
#                error('recursiveComparison: operator must be in position 1');
        
        else:
            operator = '=';
            
        match_indici = np.array([False] * len(data),dtype = bool)
        for ii in range(len(data)):
            theData = data[ii]
            dataClass = type(theData)
#            if operator == '=' and dataClass, 'double'):
#                warning('recursiveComparison: relational operator used on class %s data', dataClass);
#            end
#            if isintance(dataClass, int):
#                if strcmpi(challengeStr, 'empty'):
#                    match_indici[ii] = isnan(theData);
#                else:
#                    match_indici[ii] = theData == str2double(challengeStr);
#                    
            if dataClass:
                    match_indici[ii] = theData == challengeStr
            else:
                print 'groupDef.findMatches: unknown class %s for data selections',dataClass
                  
#                        case '<'
#                            match_indici[ii] = theData < str2double(challengeStr);
#                        case '>'
#                            match_indici[ii] = theData > str2double(challengeStr);
#                        case '>='
#                            match_indici[ii] = theData >= str2double(challengeStr);
#                        case '<='
#                            match_indici[ii] = theData <= str2double(challengeStr);
#                        else
#                            error('recursiveComparison: unknown operator');
#            if notFlag:
#                match_indici = ~match_indici;
        return match_indici
    ##print 'Data extraction error:\n%s\n',(getReport(ME)