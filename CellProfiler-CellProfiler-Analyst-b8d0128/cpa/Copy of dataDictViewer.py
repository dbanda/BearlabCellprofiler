#def dataDictViewer(*dataDict):
    #import xlsgrid
from wx.lib import sheet
import wx 
import numpy
import xlrd
class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'dataDictViewer',pos=(150, 150), size=(350, 200))
        fonts = ['Times New Roman', 'Times', 'Courier', 'Courier New', 'Helvetica', 'Sans', 'verdana', 'utkal', 'aakar', 'Arial']
        box = wx.BoxSizer(wx.VERTICAL)
        menuBar = wx.MenuBar()
        
        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        menu2 = wx.Menu()
        menuBar.Append(menu2, '&Edit')
        self.SetMenuBar(menuBar)
        
#        toolbar1 = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
#        toolbar1.AddSimpleTool(-1, wx.Image('icons/stock_new.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'New', '')
#        toolbar1.AddSimpleTool(-1, wx.Image('icons/stock_open.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open', '')
#        toolbar1.AddSimpleTool(-1, wx.Image('icons/stock_save.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Save', '')
#        toolbar1.AddSeparator()
#        toolbar1.Realize()
#        
#        toolbar2 = wx.ToolBar(self, wx.TB_HORIZONTAL | wx.TB_TEXT)
   
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
        #self.Show(True)
        
class MySheet(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.row = self.col = 0
        self.SetNumberRows(55)
        self.SetNumberCols(25)
    
        for i in range(55):
            self.SetRowSize(i, 20)
    
    def OnGridSelectCell(self, event):
      self.row, self.col = event.GetRow(), event.GetCol()
      value =  self.GetColLabelValue(self.col) + self.GetRowLabelValue(self.row)
      control.SetValue(value)
      event.Skip()
      
class MyApp(wx.App):
    def __init__(self,*dataDict):
        wx.App.__init__(self,False)
        self.frame = MyFrame(None)
        wx.StaticText(self.frame, -1, "Select Variables", (20, 10))
        self.frame.Show()

app = MyApp()
app.MainLoop()
#app.Show()
#dataDictViewer()