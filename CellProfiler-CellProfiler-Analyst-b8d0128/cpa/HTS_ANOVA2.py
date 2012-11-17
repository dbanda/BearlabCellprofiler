def HTS_ANOVA2(dataDict,fileKeys,Ttype,levels,modeltype,printToFile,alpha=0.05):
    import scipy as sc
    import scipy.stats as scStats
    from anova import anova_twoway
    import xlrd
    import xlwt
    import csv
    from pyvttbl import *
    
    #from __future__ import print_function
    dataSel = dataDict.dataSelector
    nGroups = dataSel.nGroups
    groupKeys = dataSel.getGroupDescriptions()
    #fileKeys = dataDict.dict.keys()
    nFiles = len(fileKeys)
    
    
   
    #from statsmodels.stats.anova import anova_lm
    dataSel = dataDict.dataSelector
    nGroups = dataSel.nGroups
    groupKeys = dataSel.getGroupDescriptions()
    fileKeys = dataDict.dict.keys()
    nFiles = len(fileKeys)
    print (1,'------------------------------------\n')
    print ('Dependent Variable: %s\n',dataSel.dependentVariable)
    if Ttype == 'crossplate':
        nDataSets = 1
        combinedData = dataDict.dict['combinedData']
    if Ttype== 'inplate':
        nDataSets = nFiles
    else:
        print 'HTS_ANOVAtrial: unknown type ''%s''',type
    statsStruct = []
    for iData in range(nDataSets):   
        if type ==  'crossplate':
            theDataSet = combinedData
            if nFiles == 1:
                dataSource = fileKeys[iData]
            else:
                dataSource = 'Multiple Files'
        if Ttype == 'inplate':
            theDataSet = dataDict.dict[fileKeys[iData]]
            dataSource = fileKeys[iData]
        Fmatrix = [] 
        print levels
        anovaGroups= [None] * (len(levels)-2)
        
        for iGrp in range(nGroups):
            grpKey = groupKeys[iGrp] 
            depData =theDataSet[grpKey]['dependentData']
            #depData = depData(~isnan(depData)) %remove NaN
            grpProperties = dataSel.pairDefinitions[grpKey]
            Fmatrix += [depData]
            dependentDataSize = len(depData)
            for nlevel in range(len(levels)):
                for ngrpPairs in range(len(grpProperties)):
                    if levels[nlevel]==grpProperties[ngrpPairs]:
                        anovaGrps = grpProperties[ngrpPairs]
                        tempanovaGroups = cell(dependentDataSize,1)
                        for ndepData in range(dependentDataSize):
                            tempanovaGroups[ndepData]= anovaGrps[2]
                        anovaGroups[nlevel]= vertcat(anovaGroups[nlevel],tempanovaGroups)  
                        break
            #print  anovaGroups
            print type(anovaGroups)
            if len(levels) == 1:
                [ANOVAtable ,statsStruct.results] = anova_twoway(Fmatrix,anovaGroups,'varnames',levels,'display','on')
                multcompareNames = ['Groups 1& 2''lower bound of difference''estimate of difference''upper bound of difference']
            else:
                print Fmatrix, anovaGroups
                ANOVAtable = anova_twoway(Fmatrix)
                multcompareNames = ['group1''group2''lower bound of difference''estimate of difference''upper bound of difference']
                [MC] = multcompare(statsStruct.results,'display','off') 
    
            if len(multcompareNames) < len(ANOVAtable[:,1],1):
                print ANOVAtable
                for ii in range(len(ANOVAtable[:,1],1) - len(multcompareNames)):
                    multcompareNames += ['']
                    MC += []
            elif len(levels) == 1:
                MC = MC[2:]
            ANOVAtable = horzcat(ANOVAtable, multcompareNames,MC) 
            ANOVAtable[1,1] = dataSource 
        
        return statsStruct