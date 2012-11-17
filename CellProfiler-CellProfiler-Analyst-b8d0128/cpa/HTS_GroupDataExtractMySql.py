def HTS_GroupDataExtractMySql(dataSelector,table):
    from HTS_dataDict import HTS_dataDict
    import xlrd as xl
    import numpy as np
    import matplotlib.pyplot as plt
    from properties import Properties
    from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
    import sqltools as sql

    p = Properties.getInstance()
    db = DBConnect.getInstance()
    dependentDataValues = False
    independentDataValues = False
#    def buildquery(self, table):
#        q = 'SELECT ' + self.independentVar + ', '+ self.dependentVar +' FROM ' + table
#        q2= [' WHERE '+ y[1] +' LIKE ' +y[0] for y in group.pairs]
#        return q + ''.join(q2)

    returnDict = HTS_dataDict(dataSelector)
    #for iFile in range(nFiles):
    dataSelector.clearAllIndici
    print('HTS_GroupDataExtract: using sheet %s for %s\n',table)
    query ='SELECT `' + dataSelector.independentVariable + '`  FROM ' + '`' +table+'`'
    print query
    dataSelector.findValidIndiciFromDataColumn(dataSelector.independentVariable,db.execute(query))
    query = 'SELECT `' + dataSelector.dependentVariable + '`  FROM ' + '`' +table+'`'
    print query
    dataSelector.findValidIndiciFromDataColumn(dataSelector.dependentVariable,db.execute(query))
    print dependentDataValues, independentDataValues, "variables"
    if not dependentDataValues:
        print 'HTS_GroupDataExtract: dependent variable not found in %s',
    if not independentDataValues:
        print 'HTS_GroupDataExtract: independent variable not found in %s'
    # print dataSelector.extractDataFromGroups(dependentDataValues,independentDataValues)
    dataSelector.table =  table
    returnDict.dict[table] =  dataSelector.extractDataFromGroupsMysql(dependentDataValues,independentDataValues)



#    if nFiles > 1:
#       # Get data from the selector
#        nGroups = dataSelector.nGroups
#        groupKeys = dataSelector.getGroupDescriptions()
#      # Create the combined group
#        combinedData = {}
#        tmpStruct = {}
#        tmpStruct['dependentData'] = np.array([])
#        tmpStruct['independentData'] = np.array([])
#        for iGrp in range(nGroups):
#            combinedData[groupKeys[iGrp]] = tmpStruct
#        for iFile in range(nFiles):
#            #print('the key = %s\n')
#            fileData = returnDict.dict[dataFiles[iFile]]
#            for iGrp in range(nGroups):
#                grpKey = groupKeys[iGrp]
#                #combDepData = combinedData[grpKey]['dependentData']
#                fileDepData = fileData[grpKey]['dependentData']
#                tmpStruct['dependentData'] = np.concatenate((tmpStruct['dependentData'],fileDepData[:]))
#                #combIndData = [combinedData[grpKey]['independentData']]
#                fileIndData = fileData[grpKey]['independentData']
#                tmpStruct['independentData'] = np.concatenate((tmpStruct['independentData'],fileIndData[:]))
#                combinedData[grpKey] = tmpStruct
#
#        returnDict.dict['combinedData'] = combinedData

    return returnDict

