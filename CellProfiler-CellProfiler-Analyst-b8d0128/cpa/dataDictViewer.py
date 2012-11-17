def dataDictViewer(dataDict):
    import os
    import sys
    import wx
    import xlrd
    import xlsgrid as XG
    import xlwt
    import datetime
    dic = dataDict.dict
    global workbook
    workbook = xlwt.Workbook()
    #worksheet = workbook.add_sheet('Example_1')
    cursor =0 
    count =0 
    global files 
    files = []
    for header in dic.keys():
        worksheet = workbook.add_sheet(header.split('\\')[-1])
        files += [header.split('\\')[-1]]
        worksheet.write_merge(0, 0,cursor,cursor+3, header) 
        cursor2 = cursor
        for subheader in dic[header].keys():
            worksheet.write_merge(1,1,cursor2,cursor2+1,subheader)
            cellindex = 0
            data =zip(dic[header][subheader]['independentData'],dic[header][subheader]['dependentData'])
            for cell in data:
                worksheet.write(cellindex+2,cursor2,cell[0])
                worksheet.write(cellindex+2,cursor2+1,cell[1])
                cellindex +=1
            cursor2 +=2
        
    # cursor +=4
    #worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style) # Merges row 1 through 2's columns 0 through 3.
    #worksheet.write_merge(0, cursor , 1, cursor+1, header) # Merges row 0's columns 0 through 3.
    workbook.save('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_tmp.xls')
    
    class XLSGridDemo(wx.Frame):
        def __init__(self, parent, size=(950, 730)):
            wx.Frame.__init__(self, parent, title="XLSGrid wxPython Demo", size=size)
            panel = XLSGridPanel(self)
            menubar = wx.MenuBar()
            fileMenu = wx.Menu()
            fitem = fileMenu.Append(wx.ID_EXIT, 'Save', 'save xls')
            menubar.Append(fileMenu, '&File')
            self.SetMenuBar(menubar)
            
            self.Bind(wx.EVT_MENU, self.OnSave, fitem)
#            self.CreateMenuAndStatusBar()
#            box = wx.BoxSizer(wx.VERTICAL)
#            menuBar = wx.MenuBar()
#            menu1 = wx.Menu()
#            menuBar.Append(menu1, '&File')
#            menu2 = wx.Menu()
#            menuBar.Append(menu2, '&Edit')
#            self.SetMenuBar(menuBar)
#            box.Add((5,5) , 0)
#            self.SetSizer(box)
            
        def CreateMenuAndStatusBar(self):
#            menuBar = wx.MenuBar()
#            fileMenu = wx.Menu()
#            helpMenu = wx.Menu()
#            item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit", "Exit XLSGrid demo")
#            self.Bind(wx.EVT_MENU, self.OnClose, item)
#            fileMenu.AppendItem(item)
#            item = wx.MenuItem(helpMenu, wx.ID_ANY, "About...", "Shows the about dialog")
#            self.Bind(wx.EVT_MENU, self.OnAbout, item)
#            helpMenu.AppendItem(item)
#            menuBar.Append(fileMenu, "&File")
#            menuBar.Append(helpMenu, "&Help")
#            self.SetMenuBar(menuBar)
            
            menubar = wx.MenuBar()
            fileMenu = wx.Menu()
            fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
            menubar.Append(fileMenu, '&File')
            self.SetMenuBar(menubar)
            
            self.Bind(wx.EVT_MENU, self.OnSave, fitem)
    
            
            #self.Show(True)

            
            statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
            statusbar.SetStatusWidths([-2, -1])
            statusbar_fields = [("wxPython XLSGrid Demo, Andrea Gavana @ 08 Aug 2011"),
                                ("Welcome To wxPython!")]
            for i in xrange(len(statusbar_fields)):
                statusbar.SetStatusText(statusbar_fields[i], i)
            
        def OnClose(self, event):
            wx.CallAfter(self.Destroy)
            
        def OnAbout(self, event):
            dlg = wx.MessageDialog(self, _msg, "XLSGrid wxPython Demo",
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        
        def OnSave(self,event):
            global workbook
            
            stamp = str(datetime.datetime.now())
            stamp= stamp.replace(' ', '')
            stamp = stamp.replace('.','_')
            box = wx.TextEntryDialog(None, 'EnterName','save',str(stamp))
            if box.ShowModal() == wx.ID_OK:
                stamp = box.GetValue()
                print stamp
            workbook.save('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_'+ stamp +'.xls')
    
    
    
    class XLSGridPanel(wx.Panel):
        def __init__(self, parent):
            global files
            self.files = files
            self.ind =0
            wx.Panel.__init__(self, parent)
            self.grid = XG.XLSGrid(self)
            #self.grid.Hide()        
            self.DoLayout()
            self.filename = 'C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_tmp.xls'
            busy = wx.BusyInfo("Reading Excel file, please wait...")
            sheetname = self.files[self.ind]
            self.book = xlrd.open_workbook(self.filename, formatting_info=1)
            sheet = self.book.sheet_by_name(sheetname)
            if not sheet.defcolwidth:
                sheet.defcolwidth = 10 
            rows, cols = sheet.nrows, sheet.ncols
            comments, texts = XG.ReadExcelCOM(self.filename, sheetname, rows, cols)
            del busy
            self.grid.Show()
            self.grid.PopulateGrid(self.book, sheet, texts, comments)
            self.Layout()
    
        def DoLayout(self):
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            top_sizer = wx.BoxSizer(wx.HORIZONTAL)
            top_right_sizer = wx.BoxSizer(wx.VERTICAL)
            top_center_sizer = wx.BoxSizer(wx.VERTICAL)
            toolbar1 = wx.ToolBar(self, -1, style= wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
            toolbar1.AddSimpleTool(1, wx.Image('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\icons\\previous.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'previous', '')
            toolbar1.AddSeparator()
            toolbar1.AddSimpleTool(2, wx.Image('C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\icons\\next.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Next', '')
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
            
            self.Bind(wx.EVT_TOOL, self.OnPrevious, id=1)
            self.Bind(wx.EVT_TOOL, self.OnNext, id=2)

        def OnPrevious(self, event):
            event.Skip()
            busy = wx.BusyInfo("Reading Excel file, please wait...")
            self.ind += -1
            if self.ind < 0: self.ind = len(self.files)-1
            sheetname = self.files[self.ind]
            sheet = self.book.sheet_by_name(sheetname)
            if not sheet.defcolwidth:
                sheet.defcolwidth = 10 
            rows, cols = sheet.nrows, sheet.ncols
            comments, texts = XG.ReadExcelCOM(self.filename, sheetname, rows, cols)
            del busy
            self.grid.Show()
            self.grid.PopulateGrid(self.book, sheet, texts, comments)
            self.Layout()

        def OnNext(self, event):
            event.Skip()
            filename = 'C:\\Users\Dalitso\\SkyDrive\\workspace2\\abhakar\\Workbook_tmp.xls'
            busy = wx.BusyInfo("Reading Excel file, please wait...")
            self.ind += 1
            if self.ind > len(self.files)-1: sef.ind = 0
            sheetname = self.files[self.ind]
            sheet = self.book.sheet_by_name(sheetname)
            if not sheet.defcolwidth:
                sheet.defcolwidth = 10 
            rows, cols = sheet.nrows, sheet.ncols
            comments, texts = XG.ReadExcelCOM(self.filename, sheetname, rows, cols)
            del busy
            self.grid.Show()
            self.grid.PopulateGrid(self.book, sheet, texts, comments)
            self.Layout()
    
    
    app = wx.PySimpleApp()
    frame = XLSGridDemo(None)
    frame.CenterOnScreen()
    frame.Show()
    app.MainLoop()
    del frame, app
