import dataSelectionObject
from createGrpPairs import *
from HTS_GroupDataExtract import *
from HTS_Ttest import *
from HTS_dataDict import *
from HTS_ANOVA import *
from HTS_distributionTest import *
import xlrd as xl
import  os
import  wx
global selected_cohorts
global DependentAndIndependentVariables
global test
global indVar
global depVar
DependentAndIndependentVariables = ['Percent cFos+ Neurons'
'Cell Count',
'NeuN Pos (n)','NeuN Pos (%)','Percent cFos+ Neurons',
'Percent cFos+ Neurons (Normalized to Treatment)',
'Total Puncta 2 (Normalized to Treatment)',
'Total Puncta 1 (Normalized to Treatment)','Total Puncta 2',
'Nuclei Count','NeuN+ cells','Apoptotic nuclei',
'BrdU+ cells','BrdU+NeuN+ cells',
'NeuN Pos (%)','Apoptotic (%)','BrdU Pos (%)','BrdU Pos Neurons (%)',
'Change in Neuron number (from Day 1)',
'Change in Apoptotic nuclei (from Day 1)','Change in BrdU+ cells (from Day 1)',
'Change in BrdU+ neurons (from Day 1)','Change in % Neurons (from Day 1)',
'Change in % Apoptotic Cells (from Day 1)','Change in % BrdU pos cells (from Day 1)',
'Change in % BrdU pos Neurons (from Day 1)',
'Co-Localized Overlap Count','Colocalized Puncta Per Neuron',
'Cell Count','Neuronal Phenotype Neuron (n)',
'Neuronal Phenotype Non neuronal (n)',
'Puncta 2 per Neuron','Puncta 1 per Neuron',
'Puncta 2 per Neuron','Neuronal Phenotype Neuron (n)',
'Puncta Intensity Per Neuron 2','Total Puncta Intensity 2']

#---------------------------------------------------------------------------
wildcard = "xls spreadsheet(*.xls)|*.xls|"     \
           "Python source (*.py)|*.py|"     \
           "All files (*.*)|*.*"
#---------------------------------------------------------------------------
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
##        cb = wx.ComboBox(self, 500, "dependent Variable", (20, 50),
##                         (160, -1), DependentAndIndependentVariables ,
##                         wx.CB_DROPDOWN
##                         | wx.TE_PROCESS_ENTER
##                         #| wx.CB_SORT
##                         )
##
##        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
##        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
##        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, cb)
##        cb.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
##        cb.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
##        cb.Append("foo", "This is some client data for this item")

##        cb1 = wx.ComboBox(self, 501, "independent Variable", (20, 80),
##                        (160, -1), DependentAndIndependentVariables,
##                        wx.CB_DROPDOWN)
##        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox1, cb1)
##        self.Bind(wx.EVT_TEXT, self.EvtText1, cb1)
##        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter1, cb1)
##        cb1.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
##        cb1.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
##        cb1.Append("foo", "This is some client data for this item")
##
##        cb2 = wx.ComboBox(
##            self, 502, "Test", (20, 110),
##            (160, -1), ['HTS_ANOVA', 'HTS_tTest'],
##            wx.CB_DROPDOWN)
##        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox2, cb2)
##        self.Bind(wx.EVT_TEXT, self.EvtText2, cb2)
##        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter2, cb2)
##        cb2.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
##        cb2.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
##        cb2.Append("foo", "This is some client data for this item")
    def EvtComboBox(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        cb = evt.GetEventObject()
        data = cb.GetClientData(evt.GetSelection())
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
        data = cb.GetClientData(evt.GetSelection())
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
        data = cb.GetClientData(evt.GetSelection())
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
##########################################################3333
#   program starts here
###############################################################################################3
selected_files =''
plateType = [''];
dataSelector = dataSelectionObject.dataSelecObj()
dependent = ['Total Puncta 2'];
#dataSelector.setIndependentVariable('Well');
dataSelector.setIndependentVariable('Neuronal Phenotype Neuron (n)')
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
    #selected_cohorts = ['c:\\Users\\Dalitso\\Documents\\MATLAB\\R20Repeath14Synap 4_well.xls','c:\\Users\\Dalitso\\Documents\\MATLAB\\R21Repeath14Synap 4_well.xls']
    fileMarker = '';
    #selectionStr = sprintf('Trial%s',plateType[j]);
    dataDict = HTS_GroupDataExtract(dataSelector,selected_cohorts);
    #dataDictViewer(dataDict)
    if mode=='alternate':
        csubplot = 5
        rsubplot = 1
    else:
        rsubplot = 3
        csubplot = round(len(selected_cohorts)/rsubplot)+1

    levels = ('Genotype','Trt')
    modeltype = [[1, 0], [0, 1], [1,1]]
    #statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
    #statsStruct3=HTS_ANOVA(dataDict,'inplate',levels,modeltype,{False});
    statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
    #statsStruct3=HTS_ANOVA(dataDict,selected_cohorts,'inplate',levels,modeltype,{False})
    #statsStruct = HTS_distributionTest(dataDict,'inplate',modeltype,[])
    #stastStruct = HTS_scatter(dataDict,'crossplate',modeltype,[],[],[])

##pd = dataSelector.pairDefinitions
##print '###########################'
##print dataDict.dataSelector.groupDefinitions[0].description
##print dataDict.dataSelector.groupDefinitions[0].pairsDict
