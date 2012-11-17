from __future__ import print_function
import dataSelectionObject
from createGrpPairs import *
from HTS_GroupDataExtract import *
from HTS_distributionTest import *
from HTS_scatter import *
from HTS_regressionCoincidenceTest import *
from HTS_Ttest import *
from HTS_dataDict import *
#from HTS_ANOVA import *
#from HTS_ANOVA2 import *
import xlrd as xl
from dataDictViewer import *
from createGrpPairs import *
selected_files =''
plateType = ['']
dataSelector = dataSelectionObject.dataSelecObj()
dependent = ['Total Puncta 2']
#dataSelector.setIndependentVariable('Total Puncta 1')
dataSelector.setIndependentVariable('Neuronal Phenotype Neuron (n)')
#dataSelector.setIndependentVariable('Well');
#dataSelector.setIndependentVariable('Neuronal Phenotype Neuron (n)')
descriptions=('WT','KO','l','k')
pairs = {}
pairs['Genotype'] = ('WT','KO')
pairs['Marker'] = ('SynPSD', 'GADgamma')
#pairs['Marker'] = ('GADgamma', 'SynPSD')
#pairs['Marker'] = ('SynGluR2','GADGeph')
mode = 'noalternate'
[dataSelector,iteratePair] = createGrpPairs(dataSelector,pairs,descriptions,mode);
for j in range(len(plateType)):
    crossplatePrefix = plateType[j]
    for ndependents in range(len(dependent)):
        dataSelector.setDependentVariable(dependent[ndependents])
#
#         if dataDict:
#            if plateType[j] == '':
#                tempFiles = strfind(selected_files,plateType[j])
#                for indices in range(1,length(tempFiles)):
#                    if ~isempty(tempFiles[indices]):
#                        tempFiles[indices]=indices
#                tempFiles = cell2mat(tempFiles);
#                selected_cohorts = selected_files(tempFiles)
#            else:
#                selected_cohorts = selected_files
#
    selected_cohorts = ['C:\\Users\\Dalitso\\SkyDrive\MATLAB\\R21Repeath14Synap 4_well.xls']#,'C:\\Users\\Dalitso\\SkyDrive\\MATLAB\\R22Repeath14Synap 4_well.xls']
    fileMarker = ''
#   selectionStr = sprintf('Trial%s',plateType[j])
    dataDict = HTS_GroupDataExtract(dataSelector,selected_cohorts)
    dataDictViewer(dataDict)
    if mode=='alternate':
        csubplot = 5
        rsubplot = 1
    else:
        rsubplot = 3
        csubplot = round(len(selected_cohorts)/rsubplot)+1

    levels = ['Genotype','Marker']
    modeltype = [[1, 0], [0, 1], [1,1]]
    statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
    #statsStruct3=HTS_ANOVA(dataDict,selected_cohorts,'inplate',levels,modeltype,{False});
    #statsStruct = HTS_distributionTest(dataDict,'inplate',modeltype,[])
    #stastStruct = HTS_scatter(dataDict,'crossplate',modeltype,[],[],[])
    #statsStruct = HTS_regressionCoincidenceTest(dataDict,'crossplate',modeltype,[])
##pd = dataSelector.pairDefinitions
    #statsStruct3=HTS_ANOVA2(dataDict,selected_cohorts,'inplate',levels,modeltype,{False});
##print '###########################'
##print dataDict.dataSelector.groupDefinitions[0].description
##print dataDict.dataSelector.groupDefinitions[0].pairsDict
