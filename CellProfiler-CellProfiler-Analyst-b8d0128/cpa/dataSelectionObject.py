class dataSelecObj:
    def __init__(self):
        self.pairDefinitions = {}
        self.dependentVariable = ()
        self.independentVariable = ()
        self.groupDefinitions = []
        self.nGroups = 0
    def setDependentVariable(self,value):
        self.dependentVariable = value[:]
    def setIndependentVariable(self,value):
        self.independentVariable = value[:]
    def addGroupDef(self,grpDef):
        tmplist={}
        if grpDef:
            if grpDef.description == self.getGroupDescriptions:
                print('dataSelectionselfect.addGroupDef: nonunique group name')
            self.groupDefinitions += [grpDef]
            self.nGroups = self.nGroups + 1
            for ii in range(len(grpDef.pairsDict)):
                pairKeys = grpDef.pairsDict.keys()
                theKey = pairKeys[ii].replace(' ','')
                theKey = str(theKey)
                tmplist[ii] =(theKey,grpDef.pairsDict[theKey])
            #print tmplist, 'tmplist'
            #print grpDef.description, 'grpDef descriptions'
            self.pairDefinitions[grpDef.description] = tmplist
        else:
            print('dataSelectionselfect.addGroupDef: not a groupDef')
    def findValidIndiciFromDataColumn(self,headerStr,dataValues):
        for iGrp in self.groupDefinitions:
            iGrp.updateValidIndiciFromDataColumn(headerStr,dataValues)
    def clearAllIndici(self):
        for iGrp in range(1,self.nGroups):
                self.groupDefinitions(iGrp).clearAllInd
    def extractDataFromGroups(self,dependentDataValues,independentDataValues):
        import numpy as np
        dataDict = {}
        tmp = {}
        dependentDataValues = np.array(dependentDataValues)
        independentDataValues = np.array(independentDataValues)
        for iGrp in self.groupDefinitions:
            tmp = {}
            theGroup = iGrp
            theGroup.checkMatchCount
            tmp['dependentData'] = dependentDataValues[theGroup.validIndici]
            tmp['independentData'] = independentDataValues[theGroup.validIndici]
            #tmp['pairs'] = theGroup.pairsDict[theGroup.description]
            dataDict[theGroup.description] = tmp
            #print iGrp,theGroup.description,tmp

        return dataDict
    def extractDataFromGroupsMysql(self,dependentDataValues,independentDataValues):
        from properties import Properties
        from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
        import sqltools as sql
        p = Properties.getInstance()
        p.LoadFile('C:\\Users\\Dalitso\\Desktop\\workspace2\\abhakar\\Properties_README.txt')
        db = DBConnect.getInstance()
        def buildquery(self, theGroup, var):
            pairs =  theGroup.pairsDict
            if var == 'dep':
                for i in pairs.keys():
                    print i
                    q = 'SELECT ' + '`' +self.dependentVariable +'`' + 'FROM ' + self.table + ' WHERE '
                    q2= [i +' LIKE `' + pairs[i] + '` AND ' for i in pairs.keys()]
                    result = q + ''.join(q2)[:-4]
                    print result
            if var == 'ind':
                for i in pairs.keys():
                    print i
                    q = 'SELECT ' + '`' +self.independentVariable +'`'+ 'FROM ' + self.table + 'WHERE'
                    q2= [i +'`' +' LIKE `' + pairs[i] + '` AND ' for i in pairs.keys()]
                    result = q + ''.join(q2)[:-4]
                    print result
            return result

        import numpy as np
        dataDict = {}
        dependentDataValues = np.array(dependentDataValues)
        independentDataValues = np.array(independentDataValues)
        tmp = {}
        for iGrp in self.groupDefinitions:
            theGroup = iGrp
            theGroup.checkMatchCount
            tmp['dependentData'] = db.execute(buildquery(self,theGroup, 'dep'))
            tmp['independentData'] = db.execute(buildquery(self,theGroup, 'ind'))
            #tmp['pairs'] = theGroup.pairsDict[theGroup.description]
            dataDict[theGroup.description] = tmp
            #print iGrp,theGroup.description,tmp
        return dataDict
#         for iGrp in range(self.nGroups):
#            tmp = {}
#            theGroup = self.groupDefinitions[iGrp]
#            theGroup.checkMatchCount
#            tmp['dependentData'] = dependentDataValues[theGroup.validIndici]
#            tmp['independentData'] = independentDataValues[theGroup.validIndici]
#            #tmp['pairs'] = theGroup.pairsDict[theGroup.description]
#            dataDict[theGroup.description] = tmp
#            #print iGrp,theGroup.description,tmp
#            print self.groupDefinitions[iGrp], theGroup.description
#
#        return dataDict
    def getGroupDescriptions(self):
        groupDescriptions = []
        for ii in range(self.nGroups):
            groupDescriptions += [self.groupDefinitions[ii].description]
        return groupDescriptions
    def getPlotColors(self):
        plotColors= []
        for ii in range(self.nGroups):
            plotColors+=[ self.groupDefinitions[ii].plotColor]
        return plotColors
    def formatLegendStrings(self):
        legStrs = cell(1,self.nGroups)
        for ii in range(1,self.nGroups):
            legStrs[ii] = 'wtf'
        return legStrs
                    #self.groupDefinitions{ii}.description,...
                    #self.groupDefinitions{ii}.nData)
    def reportContents(self,filename):
        if nargin < 2:
            FID = 1
            closeFile = false
        else:
            FID = fopen(filename)
            closeFile = true
        print(FID,'dataSelectionselfect: \ndependentVariable = ''%s''\nindependentVariable = ''%s''\n')(self.dependentVariable,self.independentVariable)
        print('Groups:\n')
        for ii in range(1,self.nGroups):
            print(FID,'%i: ')(ii)
            self.groupDefinitions(ii).reportContents(FID)
            if closeFile:
                fclose(FID)
