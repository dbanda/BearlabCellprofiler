import dataSelectionObject
from createGrpPairs import *
from HTS_GroupDataExtract import *
from HTS_Ttest import *
from HTS_dataDict import *
from HTS_ANOVA import *
import xlrd as xl
import  os
import  wx
global selected_cohorts
global DependentAndIndependentVariables
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
# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it to.
wildcard = "xls spreadsheet(*.xls)|*.xls|"     \
           "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"
#---------------------------------------------------------------------------
class TestPanel(wx.Panel):
    def __init__(self, parent):
        #self.log = log
        wx.Panel.__init__(self, parent, -1)
        b = wx.Button(self, -1, "select files", (80,20))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
    def OnButton(self, evt):
        global selected_cohorts
        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            print paths
            selected_cohorts = [x.encode() for x in paths]
        # Compare this with the debug above; did we change working dirs?
        #self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()
            

#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#---------------------------------------------------------------------------


overview = """\
This class provides the file selection dialog. It incorporates OS-native features
depending on the OS in use, and can be used both for open and save operations. 
The files displayed can be filtered by setting up a wildcard filter, multiple files
can be selected (open only), and files can be forced in a read-only mode.

There are two ways to get the results back from the dialog. GetFiles() returns only
the file names themselves, in a Python list. GetPaths() returns the full path and 
filenames combined as a Python list.

"""

#-----------------------------------------------------------------------------
class TestComboBox(wx.Panel):
    def OnSetFocus(self, evt):
        print "OnSetFocus"
        evt.Skip()

    def OnKillFocus(self, evt):
        print "OnKillFocus"
        evt.Skip()

    def __init__(self, parent):
        global DependentAndIndependentVariables
        wx.Panel.__init__(self, parent, -1)
        wx.StaticText(self, -1, "Select Variables", (80, 10))
        #wx.StaticText(self, -1, "Select one:", (15, 50), (75, 18))

        # This combobox is created with a preset list of values.
        cb = wx.ComboBox(self, 500, "dependent Variable", (90, 50), 
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

        # Once the combobox is set up, we can append some more data to it.
        cb.Append("foo", "This is some client data for this item")

        # This combobox is created with no values initially.
        cb = wx.ComboBox(
            self, 501, "independent Variable", (90, 80),
            (160, -1), DependentAndIndependentVariables,
            wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        
        cb = wx.ComboBox(
            self, 502, "Test", (90, 110),
            (160, -1), ['HTS_ANOVA', 'HTS_tTest'],
            wx.CB_DROPDOWN)
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)

    # When the user selects something, we go here.
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        data = cb.GetClientData(evt.GetSelection())
        if evt.GetString() == 'one':
            self.log.WriteText("You follow directions well!\n\n")

    # Capture events every time a user hits a key in the text entry field.
    def EvtText(self, evt):
        self.log.WriteText('EvtText: %s\n' % evt.GetString())
        evt.Skip()

    # Capture events when the user types something into the control then
    # hits ENTER.
    def EvtTextEnter(self, evt):
        print evt.GetString()
        evt.Skip()

        


class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self,False)
        self.frame = wx.Frame(None, wx.ID_ANY, title='My Title')
        #self.panel = TestPanel(self.frame)
        #self.combo = TestComboBox(self.frame)
        #self.panel = TestPanel(self.frame)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(TestPanel(self.frame), 0, wx.EXPAND)
        box.Add(TestComboBox(self.frame), 0 , wx.EXPAND)
        self.frame.SetSizer(box)
        self.frame.Show()
        
if __name__ == '__main__':
    import sys,os
    import run
    #run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
    app = MyApp()
    app.MainLoop()


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
    selected_cohorts = ['c:\\Users\\Dalitso\\Documents\\MATLAB\\R20Repeath14Synap 4_well.xls','c:\\Users\\Dalitso\\Documents\\MATLAB\\R21Repeath14Synap 4_well.xls']
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
    statsStruct2 = HTS_Ttest(dataDict,'inplate',modeltype)
    #statsStruct3=HTS_ANOVA(dataDict,'inplate',levels,modeltype,{False}); 
##pd = dataSelector.pairDefinitions
##print '###########################'
##print dataDict.dataSelector.groupDefinitions[0].description
##print dataDict.dataSelector.groupDefinitions[0].pairsDict
