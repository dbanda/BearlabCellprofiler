import dataSelectionObject
from createGrpPairs import *
from HTS_GroupDataExtract import *
from HTS_Ttest import *
from HTS_dataDict import *
from HTS_ANOVA import *
from HTS_GroupDataExtractMySql import *
import xlrd as xl
import numpy as np
import matplotlib.pyplot as plt
from properties import Properties
from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
import sqltools as sql
p = Properties.getInstance()
p.LoadFile('C:\\Users\\Dalitso\\workspace2\\abhakar\\Properties_README.txt')
db = DBConnect.getInstance()
plateType = ['']
dataSelector = dataSelectionObject.dataSelecObj()
dataSelector.table = p.image_table
#dependent = ['Total Puncta 2']
dependent = ['Image_Count_NucleiNeurons']
#dataSelector.setIndependentVariable('Well');
#dataSelector.setIndependentVariable('Neuronal Phenotype Neuron (n)')
dataSelector.setIndependentVariable('imageNumber')
descriptions=('WT','KO');
pairs = {};
pairs['Genotype'] = ('WT','KO');
pairs['Marker'] = ('SynGluR2','GADGeph')
mode = 'noalternate'
[dataSelector,iteratePair] = createGrpPairs(dataSelector,pairs,descriptions,mode);
for j in range(len(plateType)):
    crossplatePrefix = plateType[j];
    for ndependents in range(len(dependent)):
        dataSelector.setDependentVariable(dependent[ndependents])
#        if dataDict:
#            if plateType[j] == '':
#                tempFiles = strfind(selected_files,plateType[j]);
#                for indices in range(1,length(tempFiles)):
#                    if ~isempty(tempFiles[indices]):
#                        tempFiles[indices]=indices;
#                    end
#                end
#                tempFiles = cell2mat(tempFiles);
#                selected_cohorts = selected_files(tempFiles)
#            else:
#                selected_cohorts = selected_files;
    selected_cohorts = ['c:\\Users\\Dalitso\\Documents\\MATLAB\\R20Repeath14Synap 4_well.xls','c:\\Users\\Dalitso\\Documents\\MATLAB\\R21Repeath14Synap 4_well.xls']
    fileMarker = '';
    table = 'Main_10plates_Synap_v2_Per_Image'
    #selectionStr = sprintf('Trial%s',plateType[j]);
    dataDict = HTS_GroupDataExtractMySql(dataSelector,table);
    #dataDictViewer(dataDict)
    levels = ('Genotype','Trt')
    modeltype = [[1, 0], [0, 1], [1,1]]
    #statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
    #statsStruct3=HTS_ANOVA(dataDict,'inplate',levels,modeltype,{False});
##pd = dataSelector.pairDefinitions
##print '###########################'
##print dataDict.dataSelector.groupDefinitions[0].description
##print dataDict.dataSelector.groupDefinitions[0].pairsDict
