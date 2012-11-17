def HTS_distributionTest(dataDict,type,printToFile,alpha):
    import numpy as np
    #import scipy.stats as sc
    import math
    import matplotlib.pyplot as pyplot
    import scipy
    import statsmodels.stats.diagnostic as smStats
    import statsmodels.api as sm 
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
    
    for iData in range(nDataSets):   
            plots= [0] * nDataSets * nGroups
            
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
            #ecdf = sm.distributions.ECDF(sample)  
            ecdf = sm.distributions.ECDF(depData)
            x = np.linspace(min(depData), max(depData))
            y =ecdf(x)
            #,color=plotColors[iGrp])
            pyplot.plot(x,y)
            pyplot.step(x,y)
            legStrings += [str(str(grpKey) + '(n=' + str(len(depData))+')')]
            statValues = {}
            statValues['dataSource'] = dataSource
            tmp ={}
            for iGrp1 in range(nGroups):
                for iGrp2 in range( iGrp1+1,nGroups):
                    grp1Key = groupKeys[iGrp1]
                    depData1 = theDataSet[grp1Key]['dependentData']
                    grp2Key = groupKeys[iGrp2]
                    depData2 = theDataSet[grp2Key]['dependentData']
                    [tmp['h'],tmp['p']] = scipy.stats.ks_2samp(depData1,depData2)#,alpha) # this need to be redone
                    statsKey = str(grp1Key) +'vs'+str(grp2Key)
                    statValues[statsKey] = tmp
                    print statValues
            titleStr = titleStr.split('\\' )[-1]
            plots[iData].set_title(titleStr)
            plots[iData].set_ylabel('P(X\leqx)')
            plots[iData].set_xlabel(dataSel.dependentVariable)
            
            #xlabel(dataSel.dependentVariable,'fontsize',14)
#            set(gca,'TickDir','out')
#            hold(gca,'off')
#            
#            if exist('set_all_properties','file') == 2
#                set_all_properties(fh,'hggroup','LineWidth',2)
#
#            if printToFile{1}
#              
#                if exist('Graphs','dir') ~= 7
#                    mkdir('Graphs')     
#                end
#    
#                selectionStr = evalin('base','selectionStr')
#                directory = sprintf('Graphs/%s',selectionStr)
#                
#                if exist(directory,'dir') ~= 7
#                    mkdir(directory)  
#                end
#                
#                parseFile=regexp(dataSource,'/','split')
#                [splitstring,matchstring] = regexp(parseFile{end},'[1-9999]\d',...
#                    'split','match')
#                fileMarker = evalin('base', 'fileMarker')
#                
#                if isempty(matchstring) 
#                    crossplatePrefix = evalin('base','crossplatePrefix')
#                    filename = sprintf('%s%sDistCrossplate-%s',fileMarker,dataSel.dependentVariable,...
#                        crossplatePrefix )
#                else
#                    filename = sprintf('%s%sDist%s%s',fileMarker,dataSel.dependentVariable,...
#                        splitstring{1},matchstring{1})
#                end         
#                
#                epsFileName = sprintf('%s/%s.eps',directory,filename)
#                 print('-depsc',epsFileName)
#                fprintf('distributionTest: EPS file created: %s\n',epsFileName)
#                set(fh,'Visible','on')
#                
#                if printToFile{2}
#                    wbkName = sprintf('./Statistics/%s-Dist-Stats.csv',filename)
#                    fprintf('You are saving Dist stats for file %s\n',dataSource)
#                end
#                
#            else
#                set(fh,'Visible','on')
#                
#            switch lower(type)
#                case 'crossplate'
#                    statsStruct.results{end+1} = statValues
#                case 'inplate'
#                    statsStruct.results{end+1} = statValues
#            end
    pyplot.show()
    return statsStruct
    
    
            