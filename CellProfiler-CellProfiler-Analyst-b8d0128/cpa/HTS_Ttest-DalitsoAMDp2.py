def HTS_Ttest(dataDict,type,printToFile,alpha=0.05):
    import numpy as np
    #import scipy.stats as sc
    import math
    import matplotlib.pyplot as pyplot
    import scipy
    import statsmodels.stats.diagnostic as smStats
    dataSel = dataDict.dataSelector
    nGroups = dataSel.nGroups
    groupKeys = dataSel.getGroupDescriptions()
    print groupKeys
    fileKeys = dataDict.dict.keys()
    nFiles = len(fileKeys)
    plotColors = dataSel.getPlotColors()
    statsStruct = {}
    statsStruct['results'] = []
    statsStruct['testType'] = '2 sample t-test'
    if type == 'crossplate':
        nDataSets = 1
        combinedData = dataDict.dict['combinedData']
    if type == 'inplate':
        nDataSets = nFiles
    else:
        print'HTS_ttest: unknown type ''%s''',type
    print('------------------------------------\n')
    print('Dependent Variable: %s\n',dataSel.dependentVariable)
    fig = pyplot.figure()
    #fig = pyplot.subplot(2,5,5)
    plots= [0] * nDataSets * nGroups
    for iData in range(nDataSets):   
        print nDataSets, 'nDataSets'
        if type == 'crossplate':
            theDataSet = combinedData
            if nFiles == 1:
                dataSource = fileKeys[iData]
                titleStr = str(dataSource)
            else:
                dataSource = 'Multiple Files'
                titleStr = 'CrossPlate Analysis, Multiple Files'
        if type ==  'inplate':
                theDataSet = dataDict.dict[fileKeys[iData]]
                dataSource = fileKeys[iData]
                titleStr = str(dataSource)       
        cols= nDataSets/2.0
        cols = math.ceil(cols)
        print cols, iData
        plots[iData] = fig.add_subplot(2,cols,iData)
        #plots[iData] = pyplot.subplot(2,5,iData)
        #plts = pyplot.subplot(4,4,iData)
#        fh = figure('Visible','off')
#        hold(gca,'on')
        bh = [0]* nGroups
        legStrings = []*nGroups
        for iGrp in range(nGroups):
            grpKey = groupKeys[iGrp]
            depData = theDataSet[grpKey]['dependentData']
            #depData = depData(~isnan(depData))
            if not depData.any() :
                print'HTS_tTest: %s\nEmpty data for group %s\n',dataSource,grpKey
            mu = np.mean(depData)
            stderr = scipy.std(depData)/math.sqrt(len(depData))
            #print mu, mu+stderr
            bh[iGrp] = plots[iData].bar(iGrp,mu,0.75, color = plotColors[iGrp])#'facecolor')#,'blue')
            #
            pyplot.plot([iGrp+0.37,iGrp+0.37],[mu,mu+stderr],'k')
            pyplot.hold('on')
            legStrings += [str(str(grpKey) + '(n=' + str(len(depData))+')')]
        statValues = {}
        statValues['dataSource'] = dataSource
        for iGrp1 in range(nGroups):
            for iGrp2 in range( iGrp1+1,nGroups):
                grp1Key = groupKeys[iGrp1]
                depData1 = theDataSet[grp1Key]['dependentData']
                grp2Key = groupKeys[iGrp2]
                depData2 = theDataSet[grp2Key]['dependentData']
                np1 = smStats.lillifors(depData1) 
                np2 = smStats.lillifors(depData2)
                if np1 and np2: 
                     tmp = {}
                     (tmp['p'],tmp['h']) = scipy.stats.ttest_ind(depData1,depData2) #,alpha)
                else: 
                    tmp = {}
                    (tmp['p'],tmp['h']) = ranksum(depData1,depData2,'alpha',alpha)
                    
                statsKey = str(grp1Key) + ' vs ' + str(grp2Key)
                statValues[statsKey] = tmp
                print statValues
                #depData1_all[iGrp1,iGrp2]=depData1 
                #---------- Analysis Complete    ------------------------------------
#            scribe.legend(gca,'vertical','NorthEastOutside',-1,bh',false,...
#                legStrings,propargs[:])
                # Format the figure
                titleStr = titleStr.split('\\' )[-1]
                plots[iData].set_title(titleStr);
                plots[iData].set_ylabel(dataSel.dependentVariable)
                #set(gca,'XTickLabelMode','manual')
                #set(gca,'TickDir','out')
                plots[iData].set_xticklabels('')
                plots[iData].set_xticks([])
                plots[iData].legend(bh[iGrp],legStrings)
    pyplot.show()
                
    return statsStruct
    
