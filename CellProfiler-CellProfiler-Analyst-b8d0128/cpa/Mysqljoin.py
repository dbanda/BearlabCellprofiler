#import dataSelectionObject
from createGrpPairs import *
from HTS_GroupDataExtract import *
from HTS_Ttest import *
from HTS_dataDict import *
from HTS_ANOVA import *
from HTS_distributionTest import *
import xlrd as xl
import  os
import  wx
import csv
global selected_cohorts
global DependentAndIndependentVariables
global test
global indVar
global depVar
import xlrd as xl
import numpy as np
import matplotlib.pyplot as plt
from properties import Properties
from dbconnect import DBConnect, UniqueImageClause, UniqueObjectClause, GetWhereClauseForImages, GetWhereClauseForObjects, image_key_columns, object_key_columns
import sqltools as sql

global tables
p = Properties.getInstance()
p.LoadFile('C:\\Users\\Dalitso\\Desktop\\CellProfiler-CellProfiler-Analyst-b8d0128\\cpa\\Properties_README.txt')
db = DBConnect.getInstance()
tables = db.execute('show tables')
tables = [x[0] for x in tables]
#################################################################################################333
wildcard = "csv spreadsheet(*.csv)|*.csv|"     \
           "xls spreadsheet(*.xls)|*.xls|"     \
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
        global tables
        wx.Panel.__init__(self, parent, -1)
        wx.StaticText(self, -1, "Select Variables", (20, 10))
        cb = wx.ComboBox(self, 500, "table", (20, 50),
                         (160, -1), tables,
                         wx.CB_DROPDOWN)
                         #| wx.TE_PROCESS_ENTER
                         #| wx.CB_SORT


        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, cb)
        cb.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        cb.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        cb.Append("foo", "This is some client data for this item")


    def EvtComboBox(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        cb = evt.GetEventObject()
        data = cb.GetClientData(evt.GetSelection())
        print evt.GetString(), 'table'
        depVar = evt.GetString()
    def EvtText(self, evt):
        evt.Skip()
    def EvtTextEnter(self, evt):
        global selected_cohorts
        global DependentAndIndependentVariables
        global test
        global indVar
        global depVar
        print evt.GetString(), 'table'
        depVar = evt.GetString()
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
    app = MyApp()
    app.MainLoop()

#######################################################
def creatTableFromCsv(filename):
    ifile  = open(filename, "rb")
    reader = csv.reader(ifile)
    header =  reader.next()
    headerVals =  reader.next()
    zipheader = zip(header,headerVals)

    columns = []
    def isnum(string):
        try:
            int(string)
            return False
        except:
            return False

    for i in zipheader:

        if isnum(i[1]):
            columns.append([i[0],'int'])
        else:
            columns.append([i[0],'varchar(255)'])

    columnheaders = '\n'.join([i[0] + ' ' + i[1]+', ' for i in columns])
    columnnames =  '\n'.join([i[0] + ', ' for i in columns])
    #print columnheaders
    query = 'DROP TABLE `'+str(TableFromFile) + '`'

    try:
        db.execute(query)
    except:
        pass
    query = 'CREATE TABLE ' + '`'+ str(TableFromFile) + '` \n' + '( \n' + columnheaders
    query = query[:-2]
    query = query + '\n)'
    db.execute(query)
    query = r"load data local infile '"'' +filename+''"' into table `"+ str(TableFromFile)+ "` fields terminated by '"','"' enclosed by '"' '"' lines terminated by '"'\\r\\n'"'" + '( \n' + columnnames[:-2] + '\n)'
    print query
    db.execute(query)
    return (columnnames,columns)

def joinTables(Table,TableFromFile):
    query = 'DROP VIEW `'+  'joined'+str(Table)+'_'+str(TableFromFile) + '`'
    try:
        db.execute(query)
    except:
        pass
    realdbColumns =[i[0] for i in db.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '" + Table +"'")]
    whereclause = [ i for i in realdbColumns if i in columnnames]
    for i in whereclause:
        realdbColumns.remove(i)
    dbColumns = ', \n'.join(realdbColumns)
    query = 'CREATE VIEW`'+  'joined'+str(Table)+'_'+str(TableFromFile) + '`' + 'AS \n' + 'SELECT ' + '\n'.join(['`'+str(TableFromFile)+'`'+'.'+ i for i in columnnames.splitlines()]) +'\n'+ '\n'.join(['`'+str(Table)+'`'+'.'+ i for i in dbColumns.splitlines()])+ '\n' + 'FROM `'+ str(TableFromFile) + '` \nINNER JOIN ' + '`'+str(Table)+'`' + '\n'

    if whereclause == []:
        print ' no columns to join objects'
    whereclause = ' AND '.join(['`'+str(Table)+'`'+'.'+ i + ' = '+ '`'+str(TableFromFile)+'`'+'.'+ i for i in whereclause])
    whereclause = 'WHERE '+ whereclause
    print query+ whereclause

    #print query
    db.execute(query+whereclause)


################################################################3
TableFromFile =  selected_cohorts[0].split('\\')[-1]
filename =  selected_cohorts[0].split('\\')
filename = r"\\\\".join(filename)
print filename
Table = depVar
(columnnames,csvcolumns) = creatTableFromCsv(filename)
joinTables(Table,TableFromFile)
##query = r"load data local infile '"'' +str(selected_cohorts[0])+''"' \
##into table '"+ str(TableFromFile)+ "'fields terminated by '"','"' enclosed by '"' '"' \
##lines terminated by '"'\\n'"''"
#print query
#db.execute(query)
#creatTableFromCsv(filename)


