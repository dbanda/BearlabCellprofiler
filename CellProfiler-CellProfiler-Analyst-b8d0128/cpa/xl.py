#!/usr/bin/python
import xlrd
# spreadsheet.py
from wx.lib import sheet
import wx
import xlsgrid as XG
from XLSGridDemo import *
workbook = xlwt.Workbook()
 worksheet = workbook.add_sheet('My Sheet')
 worksheet.write_merge(0, 0, 0, 3, 'First Merge') # Merges row 0's columns 0 through 3.
 font = xlwt.Font() # Create Font
 font.bold = True # Set font to Bold
 style = xlwt.XFStyle() # Create Style
 style.font = font # Add Bold Font to Style
 worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style) # Merges row 1 through 2's columns 0 through 3.
 workbook.save('Excel_Workbook.xls')

class MySheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.row = self.col = 0
        #self.SetNumberRows(55)
        #self.SetNumberCols(25)
        
        for i in range(55):
            self.SetRowSize(i, 20)
            self.SetCellValue(1,1,'1')
    def OnGridSelectCell(self, event):
        self.row, self.col = event.GetRow(), event.GetCol()
        control = self.GetParent().GetParent().position
        value =  self.GetColLabelValue(self.col) + self.GetRowLabelValue(self.row)
        control.SetValue(value)
        event.Skip()
        
class Newt(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = ( 550, 500))
        fonts = ['Times New Roman', 'Times', 'Courier', 'Courier New', 'Helvetica', 'Sans', 'verdana', 'utkal', 'aakar', 'Arial']
        box = wx.BoxSizer(wx.VERTICAL)
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        menu2 = wx.Menu()
        menuBar.Append(menu2, '&Edit')
        self.SetMenuBar(menuBar)
        toolbar1 = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        toolbar1.AddSimpleTool(-1, wx.Image('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\icons\\next.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'New', '')
        toolbar1.AddSeparator()
        toolbar1.AddSimpleTool(-1, wx.Image('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\icons\\previous.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Cut', '')
        toolbar1.Realize()
        box.Add(toolbar1, border=5)
        box.Add((5,5) , 0)
        self.SetSizer(box)
        notebook = wx.Notebook(self, -1, style=wx.BOTTOM)
        sheet1 = MySheet(notebook)
        sheet2 = MySheet(notebook)
        sheet3 = MySheet(notebook)
        sheet1.SetFocus()
        notebook.AddPage(sheet1, 'Sheet1')
        notebook.AddPage(sheet2, 'Sheet2')
        notebook.AddPage(sheet3, 'Sheet3')
        
        box.Add(notebook, 1, wx.EXPAND)
        self.CreateStatusBar()
        self.Centre()
        self.Show()

app = wx.App()
newt = Newt(None, -1, 'SpreadSheet')
#panel = XLSGridDemo(None)
app.MainLoop()