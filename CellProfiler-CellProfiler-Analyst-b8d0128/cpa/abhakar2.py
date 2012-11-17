from dbconnect import DBConnect, UniqueImageClause, image_key_columns
from multiclasssql import filter_table_prefix
from properties import Properties
import datamodel
import guiutils as ui
from wx.combo import OwnerDrawnComboBox as ComboBox
import sqltools as sql
import imagetools
import logging
import numpy as np
import os
import sys
import re
import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from cpatool import CPATool
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
p = Properties.getInstance()
db = DBConnect.getInstance()

NO_GROUP = "Whole column"
ID_EXIT = wx.NewId()
SELECT_MULTIPLE = '<MULTIPLE SELECTED>'

class DataSourcePanel(wx.Panel):
    '''
    A panel with controls for selecting the source data for a boxplot
    '''
    def __init__(self, parent, figpanel, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        # the panel to draw charts on
        self.figpanel = figpanel

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.x_columns = [] # column names to plot if selecting multiple columns

        self.table_choice = ui.TableComboBox(self, -1, style=wx.CB_READONLY)
        self.x_choice = ComboBox(self, -1, size=(200,-1), style=wx.CB_READONLY)
        self.x_multiple = wx.Button(self, -1, 'select multiple')
        self.group_choice = ComboBox(self, -1, choices=[NO_GROUP]+p._groups_ordered, style=wx.CB_READONLY)
        self.group_choice.Select(0)
        self.filter_choice = ui.FilterComboBox(self, style=wx.CB_READONLY)
        self.update_chart_btn = wx.Button(self, -1, "Update Chart")

        self.update_column_fields()

        sz = wx.BoxSizer(wx.HORIZONTAL)
        sz.Add(wx.StaticText(self, -1, "table:"), 0, wx.TOP, 4)
        sz.AddSpacer((3,-1))
        sz.Add(self.table_choice, 1, wx.EXPAND)
        sz.AddSpacer((3,-1))
        sz.Add(wx.StaticText(self, -1, "measurement:"), 0, wx.TOP, 4)
        sz.AddSpacer((3,-1))
        sz.Add(self.x_choice, 2, wx.EXPAND)
        sz.AddSpacer((3,-1))
        sz.Add(self.x_multiple, 0, wx.EXPAND|wx.TOP, 2)
        sizer.Add(sz, 1, wx.EXPAND)
        sizer.AddSpacer((-1,3))

        sz = wx.BoxSizer(wx.HORIZONTAL)
        sz.Add(wx.StaticText(self, -1, "group x-axis by:"), 0, wx.TOP, 4)
        sz.AddSpacer((3,-1))
        sz.Add(self.group_choice, 1, wx.EXPAND)
        sizer.Add(sz, 1, wx.EXPAND)
        sizer.AddSpacer((-1,3))

        sz = wx.BoxSizer(wx.HORIZONTAL)
        sz.Add(wx.StaticText(self, -1, "filter:"), 0, wx.TOP, 4)
        sz.AddSpacer((3,-1))
        sz.Add(self.filter_choice, 1, wx.EXPAND)
        sizer.Add(sz, 1, wx.EXPAND)
        sizer.AddSpacer((-1,3))

        sizer.Add(self.update_chart_btn)

        wx.EVT_BUTTON(self.x_multiple, -1, self.on_select_multiple)
        wx.EVT_COMBOBOX(self.table_choice, -1, self.on_table_selected)
        wx.EVT_COMBOBOX(self.x_choice, -1, self.on_column_selected)
        wx.EVT_BUTTON(self.update_chart_btn, -1, self.update_figpanel)

        self.SetSizer(sizer)
        self.Show(1)

    def on_select_multiple(self, evt):
        tablename = self.table_choice.GetStringSelection()
        column_names = self.get_numeric_columns_from_table(tablename)
        dlg = wx.MultiChoiceDialog(self,
                                   'Select the columns you would like to plot',
                                   'Select Columns', column_names)
        dlg.SetSelections([column_names.index(v) for v in self.x_columns])
        if (dlg.ShowModal() == wx.ID_OK):
            self.x_choice.SetValue(SELECT_MULTIPLE)
            self.x_columns = [column_names[i] for i in dlg.GetSelections()]
            self.group_choice.Disable()
            self.group_choice.SetStringSelection(NO_GROUP)

    def on_table_selected(self, evt):
        table = self.table_choice.Value
        if table == ui.TableComboBox.OTHER_TABLE:
            t = ui.get_other_table_from_user(self)
            if t is not None:
                self.table_choice.Items = self.table_choice.Items[:-1] + [t] + self.table_choice.Items[-1:]
                self.table_choice.Select(self.table_choice.Items.index(t))
            else:
                self.table_choice.Select(0)
                return
        self.group_choice.Enable()
        self.x_columns = []
        self.update_column_fields()

    def on_column_selected(self, evt):
        self.group_choice.Enable()

    def update_column_fields(self):
        tablename = self.table_choice.GetStringSelection()
        fieldnames = self.get_numeric_columns_from_table(tablename)
        self.x_choice.Clear()
        self.x_choice.AppendItems(fieldnames)
        self.x_choice.SetSelection(0)

    def get_numeric_columns_from_table(self, table):
        ''' Fetches names of numeric columns for the given table. '''
        measurements = db.GetColumnNames(table)
        types = db.GetColumnTypes(table)
        return [m for m,t in zip(measurements, types) if t in [float, int, long]]

    def update_figpanel(self, evt=None):
        table = self.table_choice.Value
        fltr = self.filter_choice.get_filter_or_none()
        grouping = self.group_choice.Value
        if self.x_choice.Value == SELECT_MULTIPLE:
            points_dict = {}
            for col in self.x_columns:
                pts = self.loadpoints(table, col, fltr, NO_GROUP)
                for k in pts.keys(): assert k not in points_dict.keys()
                points_dict.update(pts)
        else:
            col = self.x_choice.Value
            points_dict = self.loadpoints(table, col, fltr, grouping)

        # Check if the user is creating a plethora of plots by accident
        if 100 >= len(points_dict) > 25:
            res = wx.MessageDialog(self, 'Are you sure you want to show %s box '
                                   'plots on one axis?'%(len(points_dict)),
                                   'Warning', style=wx.YES_NO|wx.NO_DEFAULT
                                   ).ShowModal()
            if res != wx.ID_YES:
                return
        elif len(points_dict) > 100:
            wx.MessageBox('Sorry, boxplot can not show more than 100 plots on\n'
                          'a single axis. Your current settings would plot %d.\n'
                          'Try using a filter to narrow your query.'
                          %(len(points_dict)), 'Too many groups to plot')
            return

        self.figpanel.setpoints(points_dict)
        if self.group_choice.Value != NO_GROUP:
            self.figpanel.set_x_axis_label(grouping)
            self.figpanel.set_y_axis_label(self.x_choice.Value)
        self.figpanel.draw()

    def loadpoints(self, tablename, col, fltr=None, grouping=NO_GROUP):
        '''
        Returns a dict mapping x label values to lists of values from col
        '''
        q = sql.QueryBuilder()
        select = [sql.Column(tablename, col)]
        if grouping != NO_GROUP:
            dm = datamodel.DataModel.getInstance()
            group_cols = dm.GetGroupColumnNames(grouping, include_table_name=True)
            select += [sql.Column(*col.split('.')) for col in group_cols]
        q.set_select_clause(select)
        if fltr is not None:
            q.add_filter(fltr)

        res = db.execute(str(q))
        res = np.array(res, dtype=object)
        # replaces Nones with NaNs
        for row in res:
            if row[0] is None:
                row[0] = np.nan

        points_dict = {}
        if self.group_choice.Value != NO_GROUP:
            for row in res:
                groupkey = tuple(row[1:])
                points_dict[groupkey] = points_dict.get(groupkey, []) + [row[0]]
        else:
            points_dict = {col : [r[0] for r in res]}
        return points_dict

    def save_settings(self):
        '''
        Called when saving a workspace to file.
        returns a dictionary mapping setting names to values encoded as strings
        '''
        if self.x_choice.Value == SELECT_MULTIPLE:
            cols = self.x_columns
        else:
            cols = [self.x_choice.GetStringSelection()]
        return {'table'  : self.table_choice.Value,
                'x-axis' : ','.join(cols),
                'filter' : self.filter_choice.Value,
                'x-lim'  : self.figpanel.subplot.get_xlim(),
                'y-lim'  : self.figpanel.subplot.get_ylim(),
##                'grouping': self.group_choice.Value,
##                'version': '1',
                }

    def load_settings(self, settings):
        '''load_settings is called when loading a workspace from file.

        settings - a dictionary mapping setting names to values encoded as
                   strings.
        '''
##        if 'version' not in settings:
##            settings['grouping'] = NO_GROUP
##            settings['version'] = '1'
        if 'table' in settings:
            self.table_choice.SetStringSelection(settings['table'])
            self.update_column_fields()
        if 'x-axis' in settings:
            cols = map(str.strip, settings['x-axis'].split(','))
            if len(cols) == 1:
                self.x_choice.SetStringSelection(cols[0])
            else:
                self.x_choice.SetValue(SELECT_MULTIPLE)
                self.x_columns = cols
        if 'filter' in settings:
            self.filter_choice.SetStringSelection(settings['filter'])
        self.update_figpanel()
        if 'x-lim' in settings:
            self.figpanel.subplot.set_xlim(eval(settings['x-lim']))
        if 'y-lim' in settings:
            self.figpanel.subplot.set_ylim(eval(settings['y-lim']))
        self.figpanel.draw()


class BoxPlotPanel(FigureCanvasWxAgg):
    def __init__(self, parent, points, **kwargs):
        '''
        points -- a dictionary mapping x axis values to lists of values to plot
        '''
        self.figure = Figure()
        FigureCanvasWxAgg.__init__(self, parent, -1, self.figure, **kwargs)
        self.canvas = self.figure.canvas
        self.SetMinSize((100,100))
        self.figure.set_facecolor((1,1,1))
        self.figure.set_edgecolor((1,1,1))
        self.canvas.SetBackgroundColour('white')

        self.navtoolbar = None
        self.setpoints(points)

    def setpoints(self, points):
        '''
        Updates the data to be plotted and redraws the plot.
        points - list of array samples, where each sample will be plotted as a
                 separate box plot against the same y axis
        '''
        self.xlabels = []
        self.points = []
        ignored = 0
        for label, values in sorted(points.items()):
            if type(label) in [tuple, list]:
                self.xlabels += [','.join([str(l) for l in label])]
            else:
                self.xlabels += [label]
            self.points += [np.array(values).astype('f')[~ np.isnan(values)]]
            ignored += len(np.array(values)[np.isnan(values)])

        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(111)
        self.subplot.clear()
        # nothing to plot?
        if len(self.points)==0:
            logging.warn('No data to plot.')
            return
        self.subplot.boxplot(self.points)
        if len(self.points) > 1:
            self.figure.autofmt_xdate()
        self.subplot.set_xticklabels(self.xlabels)
        self.reset_toolbar()
        if ignored == 0:
            logging.info('Boxplot: Plotted %s points.'%(sum(map(len, self.points))))
        else:
            logging.warn('Boxplot: Plotted %s points. Ignored %s NaNs.'
                          %(sum(map(len, self.points)), ignored))

    def set_x_axis_label(self, label):
        self.subplot.set_xlabel(label)

    def set_y_axis_label(self, label):
        self.subplot.set_ylabel(label)

    def get_point_lists(self):
        return self.points

    def get_xlabels(self):
        return self.xlabels

    def get_toolbar(self):
        if not self.navtoolbar:
            self.navtoolbar = NavigationToolbar(self.canvas)
            self.navtoolbar.DeleteToolByPos(6)
        return self.navtoolbar

    def reset_toolbar(self):
        # Cheat since there is no way reset
        if self.navtoolbar:
            self.navtoolbar._views.clear()
            self.navtoolbar._positions.clear()
            self.navtoolbar.push_current()


class BoxPlot(wx.Frame, CPATool):
    '''
    A very basic boxplot with controls for setting it's data source.
    '''
    def __init__(self, parent, size=(600,600), **kwargs):
        wx.Frame.__init__(self, parent, -1, size=size, title='BoxPlot', **kwargs)
        CPATool.__init__(self)
        self.SetName(self.tool_name)
        self.SetBackgroundColour(wx.NullColor)
        points = {}
        figpanel = BoxPlotPanel(self, points)
        configpanel = DataSourcePanel(self, figpanel)
        self.SetToolBar(figpanel.get_toolbar())
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(figpanel, 1, wx.EXPAND)
        sizer.Add(configpanel, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)

        #
        # Forward save and load settings functionality to the configpanel
        #
        self.save_settings = configpanel.save_settings
        self.load_settings = configpanel.load_settings
if __name__ == "__main__":
    wx.App.__init__(self,False)
    self.frame = wx.Frame(None, wx.ID_ANY, title='My Title')
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(TestPanel(self.frame), 0, wx.EXPAND)
    box.Add(TestComboBox(self.frame), 0 , wx.EXPAND)
    self.frame.SetSizer(box)
    self.frame.Show()
    app = wx.PySimpleApp()
    logging.basicConfig(level=logging.DEBUG,)

    if len(sys.argv) > 1:
        # Load a properties file if passed in args
        p = Properties.getInstance()
        p.LoadFile(sys.argv[1])
    elif not p.show_load_dialog():
        print 'BoxPlot requires a properties file.  Exiting.'
        # necessary in case other modal dialogs are up
        wx.GetApp().Exit()
        sys.exit()
        afraser
    boxplot = BoxPlot(None)
    boxplot.Show()

    app.MainLoop()

    #
    # Kill the Java VM
    #
    try:
        from bioformats import jutil
        jutil.kill_vm()
    except:
        import traceback
        traceback.print_exc()
        print "Caught exception while killing VM"
