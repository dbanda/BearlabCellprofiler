def HTS_GroupDataExtract(dataSelector,dataFiles):
    from HTS_dataDict import HTS_dataDict
    import xlrd as xl
    import numpy as np
    dependentDataValues = False
    independentDataValues = False
    
    returnDict = HTS_dataDict(dataSelector)
    nFiles = len(dataFiles)
    for iFile in range(nFiles):
        dataSelector.clearAllIndici
        dataFile = dataFiles[iFile]
        book = xl.open_workbook(dataFile)
        sheetName = ''
        for sheet in book.sheet_names():
            if sheet == 'AutoCreate':
                sheetName = 'AutoCreate'
                sheet = book.sheet_by_name(sheetName)
            if sheet=='Math':
                sheetName = 'Math'
                sheet = book.sheet_by_name(sheetName)
            if sheet== 'Corrected':
                sheetName = 'Corrected'
                sheet = book.sheet_by_name(sheetName)
        if sheetName == '':
            print ('HTS_GroupDataExtract: %s does not have a recognized sheet name',dataFile)
        print('HTS_GroupDataExtract: using sheet %s for %s\n',sheetName,dataFile)
        headerRows =  zip(sheet.row_values(0), sheet.row_values(1))
        for pair in range(len(headerRows)):
            headerRows[pair] = headerRows[pair][0] + headerRows[pair][1]
        for col in range(len(headerRows)):
                #print headerRows[col], dataSelector.independentVariable
                if headerRows[col].replace(' ','') == dataSelector.independentVariable.replace(' ', ''):
                    independentDataValues = sheet.col_values(col,2)
                    
                if headerRows[col] == dataSelector.dependentVariable:
                    dependentDataValues = sheet.col_values(col,2)                    
                  
                    
                dataSelector.findValidIndiciFromDataColumn(headerRows[col],sheet.col_values(col,2))
        if not dependentDataValues:
            print('HTS_GroupDataExtract: dependent variable not found in %s',dataFile)
        
        if not independentDataValues:
            print('HTS_GroupDataExtract: independent variable not found in %s',dataFile)
       # print dataSelector.extractDataFromGroups(dependentDataValues,independentDataValues)
        returnDict.dict[dataFile] =  dataSelector.extractDataFromGroups(dependentDataValues,independentDataValues)
        
            
        
    if nFiles > 1:
       # Get data from the selector
        nGroups = dataSelector.nGroups
        groupKeys = dataSelector.getGroupDescriptions()
      # Create the combined group
        combinedData = {}
        tmpStruct = {}
        tmpStruct['dependentData'] = np.array([])
        tmpStruct['independentData'] = np.array([])
        for iGrp in range(nGroups):
            combinedData[groupKeys[iGrp]] = tmpStruct
        for iFile in range(nFiles):
            #print('the key = %s\n')
            fileData = returnDict.dict[dataFiles[iFile]]
            for iGrp in range(nGroups):
                grpKey = groupKeys[iGrp]
                #combDepData = combinedData[grpKey]['dependentData']
                fileDepData = fileData[grpKey]['dependentData']
                tmpStruct['dependentData'] = np.concatenate((tmpStruct['dependentData'],fileDepData[:]))
                #combIndData = [combinedData[grpKey]['independentData']]
                fileIndData = fileData[grpKey]['independentData']
                tmpStruct['independentData'] = np.concatenate((tmpStruct['independentData'],fileIndData[:]))
                combinedData[grpKey] = tmpStruct
                
        returnDict.dict['combinedData'] = combinedData
        
    return returnDict
    
