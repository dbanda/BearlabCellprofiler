import os
import sys
import wx
import xlrd
import xlsgrid as XG
import xlwt
dic = {'file':{'wt':[2,4,6], 'ko':[8,10,12]},'odnums':{'wt':[1,3,5], 'ko':[7,9,11]}}
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Example_1')
cursor =0 
count =0 
for header in dic.keys():
    worksheet.write_merge(0, 0,cursor,cursor+1, header) # Merges row 0's columns 0 through 3.
    cursor2 = cursor
    for subheader in dic[header].keys():
        worksheet.write(1,cursor2,subheader)
        cellindex = 2
        for cell in dic[header][subheader]:
            print cell
            worksheet.write(cellindex,cursor2,cell)
            cellindex +=1
        cursor2 +=1
    cursor +=2
#worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style) # Merges row 1 through 2's columns 0 through 3.
#worksheet.write_merge(0, cursor , 1, cursor+1, header) # Merges row 0's columns 0 through 3.
workbook.save('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_tmp.xls')

class XLSGridDemo(wx.Frame):
    def __init__(self, parent, size=(950, 730)):
        wx.Frame.__init__(self, parent, title="XLSGrid wxPython Demo", size=size)
        panel = XLSGridPanel(self)
        self.CreateMenuAndStatusBar()
        box = wx.BoxSizer(wx.VERTICAL)
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuBar.Append(menu1, '&File')
        menu2 = wx.Menu()
        menuBar.Append(menu2, '&Edit')
        self.SetMenuBar(menuBar)
        box.Add((5,5) , 0)
        self.SetSizer(box)
    def CreateMenuAndStatusBar(self):
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit", "Exit XLSGrid demo")
        self.Bind(wx.EVT_MENU, self.OnClose, item)
        fileMenu.AppendItem(item)
        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About...", "Shows the about dialog")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.AppendItem(item)
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        statusbar.SetStatusWidths([-2, -1])
        statusbar_fields = [("wxPython XLSGrid Demo, Andrea Gavana @ 08 Aug 2011"),
                            ("Welcome To wxPython!")]
        for i in xrange(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)
    def OnClose(self, event):
        wx.CallAfter(self.Destroy)
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, _msg, "XLSGrid wxPython Demo", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class XLSGridPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.grid = XG.XLSGrid(self)
        #self.grid.Hide()        
        self.DoLayout()
        filename = 'C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_tmp.xls'
        busy = wx.BusyInfo("Reading Excel file, please wait...")
        sheetname = "Example_1"
        book = xlrd.open_workbook(filename, formatting_info=1)
        sheet = book.sheet_by_name(sheetname)
        print sheet
        if not sheet.defcolwidth:
            sheet.defcolwidth = 10 
        rows, cols = sheet.nrows, sheet.ncols
        comments, texts = XG.ReadExcelCOM(filename, sheetname, rows, cols)
        del busy
        self.grid.Show()
        self.grid.PopulateGrid(book, sheet, texts, comments)
        self.Layout()

    def DoLayout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_center_sizer = wx.BoxSizer(wx.VERTICAL)
        toolbar1 = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        toolbar1.AddSimpleTool(-1, wx.Image('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\icons\\next.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'New', '')
        toolbar1.AddSeparator()
        toolbar1.AddSimpleTool(-1, wx.Image('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\icons\\previous.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Cut', '')
        toolbar1.Realize()
        top_center_sizer.Add(toolbar1, border=5)
        #box.Add((5,5) , 0)
        
        top_sizer.Add(top_center_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        top_right_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        top_sizer.Add(top_right_sizer, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        main_sizer.Add(top_sizer, 0, wx.ALL|wx.EXPAND, 5)
        main_sizer.Add((0, 10))
        main_sizer.Add(self.grid, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(main_sizer)

        main_sizer.Layout()
        

    def OnStart(self, event):

        event.Skip()
        filename = 'C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_tmp.xls'
        busy = wx.BusyInfo("Reading Excel file, please wait...")
        sheetname = "Example_1"
        book = xlrd.open_workbook(filename, formatting_info=1)
        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols
        comments, texts = XG.ReadExcelCOM(filename, sheetname, rows, cols)
        del busy
        self.grid.Show()
        self.grid.PopulateGrid(book, sheet, texts, comments)
        self.start_button.Enable(False)
        self.Layout()


app = wx.PySimpleApp()
frame = XLSGridDemo(None)
frame.CenterOnScreen()
frame.Show()
app.MainLoop()
del frame, app
