def HTS_scatter(dataDict,Type,rsubplot,csubplot,printToFile,alpha):
    import numpy as np
    import math
    import matplotlib.pyplot as pyplot
    import scipy
    import statsmodels.stats.diagnostic as smStats
    dataSel = dataDict.dataSelector
    nGroups = dataSel.nGroups
    groupKeys = dataSel.getGroupDescriptions()
    fileKeys = dataDict.dict.keys()
    nFiles = len(fileKeys)
    plotColors = dataSel.getPlotColors()
    statsStruct = {}
    statsStruct['results'] = {}
    statsStruct['testType'] = 'scatter plot'
    plotMode = Type
    if Type == 'crossplate':
        nDataSets = 1
        combinedData = dataDict.dict['combinedData']
    if Type == 'inplate':
        nDataSets = nFiles    
    else:
         print('HTS_regressionCoincidence: unknown Type ''%s''',Type)
         
    print(1,'------------------------------------\n')
    print('Dependent Variable: %s\n',dataSel.dependentVariable)
    fig = pyplot.figure()
    plots= [0] * nDataSets * nGroups
    for iData in range(nDataSets):        
        print nDataSets, 'nDataSets'
        if Type == 'crossplate':
            theDataSet = combinedData
            if nFiles == 1:
                dataSource = fileKeys[iData]
                titleStr = str(dataSource)
            else:
                dataSource = 'Multiple Files'
                titleStr = 'CrossPlate Analysis, Multiple Files'
        if Type ==  'inplate':
                theDataSet = dataDict.dict[fileKeys[iData]]
                dataSource = fileKeys[iData]
                titleStr = str(dataSource)
        rows =1   
        if nDataSets > 3:
            rows = 2
        cols= nDataSets/2.0
        cols = math.ceil(cols)
        plots[iData] = fig.add_subplot(rows,cols,iData)
        minX = float('inf') 
        maxX = -float('inf')
        fitParams = [0] * nGroups
        legStrings = []
        scatterplot = [0]*nGroups
        for iGrp in range(nGroups):
            grpKey = groupKeys[iGrp]
            grpProperties = dataSel.pairDefinitions[grpKey] 
            y = [theDataSet[grpKey]['dependentData']]
            x = [theDataSet[grpKey]['independentData']]
            n = len(x)
            tmpStruct ={}
            tmpStruct['x'] = x
            tmpStruct['y'] = y
            fitParams[iGrp] = tmpStruct
            if plotMode == 'alternate': 
                if iGrp >=3:
                    if iGrp%2 != 0:
                        isubplot = isubplot + 1
            print('##########################this is the data####################3')
            print(x)
            print(y)
            print 'IGRP'
            print iGrp
            print plotColors[iGrp]
            if iGrp == 0:
                xel = range(len(x)) #,length(x),1)
                global x_list
                x_list = x
            if Type ==  'crossplate':
                #pyplot.plot(range(len(y)),y) #,plotColors[iGrp])#,'MarkerEdgeColor', plotColors[iGrp],'MarkerSize',3.5)
                print (type(y[0]))
                #plots[iData].plot(range(len(y[0])),y[0])
                plots[iData].scatter (range(len(y[0])),y[0])
                #pyplot.show()
                
            xel = range(len(xel), len(x) + len(x) -1)
            if iGrp%2 == 0:
                #currentAxis = get(gcf,'CurrentAxes')
                if grpProperties[0][1] =='Marker':
                    subplotTitle = grpProperties[0][1]
                else:
                    subplotTitle = grpProperties[0]
            plots[iData].set_title(subplotTitle[1])
                #formatFigures(subplotTitle[2],currentAxis,nDataSets,iData,dataSel,6,2)
            pyplot.hold('on')
            legStrings += [str(str(grpKey) + '(n=' + str(len(y))+')')]

        x_ = [0, minX, maxX]
        x_ = [0, minX ,300]
        if plotMode =='alternate': 
            isubplot = isubplot - ((nGroups/2)-1)
            legStrings = {'WT','KO'}
        if iData == 1: 
            #figure(fh)
#            if iGrp > 1:
#                if isstr(x_list):
#                    x_list = cellstr(x_list)
#                if isstr(x):
#                    xstr = cellstr(x)
#                else
#                    xstr = x
#                end    
#                x_list = [x_list xstr]
#                x_list = char(x_list)
#                
#            end
            
#            h= get(fh, 'CurrentAxes')
#            set(h, 'Xlimmode','Auto')
#            pyplot.x
#            disp(legStrings)
            #legend(legStrings,'Orientation','Vertical','Location','Best')
            pyplot.hold('on')
        #currentAxis = get(gcf,'CurrentAxes')    
        #formatFigures(titleStr,currentAxis,nDataSets,iData,dataSel,6,2)
        if plotMode =='alternate':
            h = get(currentAxis,'Title')
            strH = get(h,'String')
            newTitle = strcat()#strH,':',subplotTitle{2})
            title(newTitle)   
        if Type == 'crossplate':
               #statsStruct[results[end+1]] = statValues
            pass
        if Type == 'inplate':
                #statsStruct.results[end+1] = statValues
            pass
    print x_list[0] , 'xlist'
    plots[iData].set_xticks(range(len(y[0])))
    plots[iData].set_xticklabels(x_list[0])
    pyplot.hold('on')
    pyplot.show()
    return statsStruct