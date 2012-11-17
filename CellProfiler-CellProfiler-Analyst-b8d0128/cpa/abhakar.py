import dataSelectionObject
from createGrpPairs import *
from HTS_GroupDataExtract import *
from HTS_Ttest import *
from HTS_dataDict import *
from HTS_ANOVA import *
from HTS_distributionTest import *
from HTS_GroupDataExtractMySql import *
import numpy as np
import matplotlib.pyplot as plt
from properties import Properties
from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
import sqltools as sql
import xlrd as xl
import  os
import  wx
global selected_cohorts
global DependentAndIndependentVariables
global test
global indVar
global depVar
global test
global table
depVar = []
indVar = []
table = 'Main_10plates_Synap_v2_Per_Image'
p = Properties.getInstance()
p.LoadFile('C:\\Users\\Dalitso\\Desktop\\workspace2\\abhakar\\Properties_README.txt')
db = DBConnect.getInstance()
DependentAndIndependentVariables = [i[0] for i in db.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'Main_10plates_Synap_v2_Per_Image'")]


#---------------------------------------------------------------------------
wildcard = "xls spreadsheet(*.xls)|*.xls|"     \
           "Python source (*.py)|*.py|"     \
           "All files (*.*)|*.*"
#---------------------------------------------------------------------------

pairs = {};
class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        b = wx.Button(self, -1, "select files", (20,20))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        global selected_cohorts
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print paths
            selected_cohorts = [x.encode() for x in paths]
        dlg.Destroy()



class TestComboBox(wx.Panel):
    def OnSetFocus(self, evt):
        #print "OnSetFocus"
        evt.Skip()

    def OnKillFocus(self, evt):
        #print "OnKillFocus"
        evt.Skip()

    def __init__(self, parent):
        global DependentAndIndependentVariables
        wx.Panel.__init__(self, parent, -1)
        wx.StaticText(self, -1, "Select Variables", (20, 10))
        cb = wx.ComboBox(self, 500, "dependent Variable", (20, 50),
                         (160, -1), DependentAndIndependentVariables ,
                         wx.CB_DROPDOWN
                         | wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT
                         )

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, cb)
        cb.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        cb.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        cb1 = wx.ComboBox(self, 501, "independent Variable", (20, 80),
                        (160, -1), DependentAndIndependentVariables,
                        wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox1, cb1)
        self.Bind(wx.EVT_TEXT, self.EvtText1, cb1)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter1, cb1)
        cb1.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        cb1.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


        cb2 = wx.ComboBox(
            self, 502, "Test", (20, 110),
            (160, -1), ['HTS_ANOVA', 'HTS_tTest'],
            wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox2, cb2)
        self.Bind(wx.EVT_TEXT, self.EvtText2, cb2)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter2, cb2)
        cb2.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        cb2.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


        addpair = wx.Button(self, -1, "add= pair", (20,140))
        self.Bind(wx.EVT_BUTTON, self.addPair, addpair)

        cb3 = wx.ComboBox(
            self, 502, "Pair", (100, 140),
            (160, -1), DependentAndIndependentVariables,
            wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox2, cb3)
        self.Bind(wx.EVT_TEXT, self.EvtText2, cb3)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter2, cb3)
        cb3.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        cb3.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        wx.StaticText(self, -1, "=", (271, 140))
        self.tex1 = wx.TextCtrl(self, 502, "Pair", (280, 140))
        self.tex2 = wx.TextCtrl(self, 502, "Pair", (340, 140))
        self.cb3 =cb3

        okay = wx.Button(self, -1, "OK", (20,160))
        self.Bind(wx.EVT_BUTTON, self.okay, okay)

    def addPair(self, evt):
        global pairs
        pairs[self.cb3.Value] = (self.tex1.Value,self.tex2.Value)
        print pairs
        pass

    def EvtComboBox(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        cb = evt.GetEventObject()
        #data = cb.GetClientData(evt.GetSelection())
        print evt.GetString(), 'dependent Variable'
        depVar = evt.GetString()
    def EvtText(self, evt):
        evt.Skip()
    def EvtTextEnter(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        print evt.GetString(), 'dependent Variable'
        depVar = evt.GetString()
        evt.Skip()
    def EvtComboBox1(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        cb = evt.GetEventObject()
        #data = cb.GetClientData(evt.GetSelection())
        print evt.GetString(), 'independent Variable'
        indVar = evt.GetString()
    def EvtText1(self, evt):
        evt.Skip()
    def EvtTextEnter1(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        print evt.GetString(),'independent Variable'
        indVar = evt.GetString()
        evt.Skip()
    def EvtComboBox2(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        cb = evt.GetEventObject()
        #data = cb.GetClientData(evt.GetSelection())
        print evt.GetString(), 'test'
    def EvtText2(self, evt):
        evt.Skip()
    def EvtTextEnter2(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        print evt.GetString(),'test'
        test = evt.GetString()
        evt.Skip()
    def okay(self, evt):
        global test
        global depVar
        global indVar
        selected_files =''
        plateType = [''];
        dataSelector = dataSelectionObject.dataSelecObj()
        ##dependent = ['Total Puncta 2'];
        ###dataSelector.setIndependentVariable('Well');
        ##dataSelector.setIndependentVariable('Neuronal Phenotype Neuron (n)')
        descriptions=('WT','KO');
        ###pairs = {};
        ##pairs['Genotype'] = ('WT','KO');
        ##pairs['Marker'] = ('SynGluR2','GADGeph')
        dependent  =  [depVar]
        dataSelector.setIndependentVariable(indVar)
        mode = 'noalternate'

        [dataSelector,iteratePair] = createGrpPairs(dataSelector,pairs,descriptions,mode);
        for j in range(len(plateType)):
            crossplatePrefix = plateType[j];
            for ndependents in range(len(dependent)):
                dataSelector.setDependentVariable(dependent[ndependents])
            fileMarker = '';
            dataDict =HTS_GroupDataExtractMySql(dataSelector,table)
            if mode=='alternate':
                csubplot = 5
                rsubplot = 1
            else:
                rsubplot = 3
                csubplot = round(len(selected_cohorts)/rsubplot)+1
            levels = ('Genotype','Trt')
            modeltype = [[1, 0], [0, 1], [1,1]]
            if test == 'HTS_tTest':
                print 'running tTest'
                statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)

            #statsStruct3=HTS_ANOVA(dataDict,'inplate',levels,modeltype,{False});
            #statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
            #statsStruct3=HTS_ANOVA(dataDict,selected_cohorts,'inplate',levels,modeltype,{False})
            #statsStruct = HTS_distributionTest(dataDict,'inplate',modeltype,[])
            #stastStruct = HTS_scatter(dataDict,'crossplate',modeltype,[],[],[])
        print "done!!!!!!!!!!"
class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self,False)
        self.frame = wx.Frame(None, wx.ID_ANY, title='My Title')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(TestPanel(self.frame), 0, wx.EXPAND)
        box.Add(TestComboBox(self.frame), 0 , wx.EXPAND)
        self.frame.SetSizer(box)
        self.frame.Show()
if __name__ == '__main__':
    import sys,os
    #import run
    #run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
    app = MyApp()
    app.MainLoop()

###############################################################################################3
selected_files =''
plateType = [''];
dataSelector = dataSelectionObject.dataSelecObj()
##dependent = ['Total Puncta 2'];
###dataSelector.setIndependentVariable('Well');
##dataSelector.setIndependentVariable('Neuronal Phenotype Neuron (n)')
descriptions=('WT','KO');
###pairs = {};
##pairs['Genotype'] = ('WT','KO');
##pairs['Marker'] = ('SynGluR2','GADGeph')
dependent  =  [depVar]
dataSelector.setIndependentVariable(indVar)
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
    #selected_cohorts = ['c:\\Users\\Dalitso\\SkyDrive\\MATLAB\\R21Repeath14Synap 4_well.xls','c:\\Users\\Dalitso\\SkyDrive\\MATLAB\\R22Repeath14Synap 4_well.xls']
    fileMarker = '';
    #selectionStr = sprintf('Trial%s',plateType[j]);
    dataDict =HTS_GroupDataExtractMySql(dataSelector,table)
    #dataDictViewer(dataDict)
    if mode=='alternate':
        csubplot = 5
        rsubplot = 1
    else:
        rsubplot = 3
        csubplot = round(len(selected_cohorts)/rsubplot)+1

    levels = ('Genotype','Trt')
    modeltype = [[1, 0], [0, 1], [1,1]]
    if test == 'HTS_tTest':
        print 'running tTest'
        statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)

    #statsStruct3=HTS_ANOVA(dataDict,'inplate',levels,modeltype,{False});
    #statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
    #statsStruct3=HTS_ANOVA(dataDict,selected_cohorts,'inplate',levels,modeltype,{False})
    #statsStruct = HTS_distributionTest(dataDict,'inplate',modeltype,[])
    #stastStruct = HTS_scatter(dataDict,'crossplate',modeltype,[],[],[])
    print "done!!!!!!!!!!"
##pd = dataSelector.pairDefinitions
##print '###########################'
##print dataDict.dataSelector.groupDefinitions[0].description
##print dataDict.dataSelector.groupDefinitions[0].pairsDict
