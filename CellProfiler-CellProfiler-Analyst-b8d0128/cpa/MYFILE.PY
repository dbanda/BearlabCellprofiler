import scatter2; from scatter2 import *
class bar(wx.Frame, CPATool):
    '''
    A very basic bar plot with controls for setting it's data source.
    '''
    def __init__(self, parent, size=(600,600), **kwargs):
        wx.Frame.__init__(self, parent, -1, size=size, title='bar Plot', **kwargs)
        CPATool.__init__(self)
        self.SetName(self.tool_name)
        self.SetBackgroundColour(wx.NullColor)
        
        
        figpanel = barPanel(self)
        figpanel2 = barPanel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(figpanel, 1, wx.EXPAND)
        
        
        configpanel = barControlPanel(self, figpanel)
        configpanel2 = barControlPanel(self,figpanel2)
        figpanel.set_configpanel(configpanel)
        figpanel2.set_configpanel(configpanel2)
        sizer.Add(configpanel, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(figpanel2, 1, wx.EXPAND)
        sizer.Add(configpanel2, 0, wx.EXPAND|wx.ALL, 5)
        self.SetToolBar(figpanel.get_toolbar())            
        self.SetSizer(sizer)
        #
        # Forward save and load settings functionality to the configpanel
        #
        self.save_settings = configpanel.save_settings
        self.load_settings = configpanel.load_settings

    
    
if __name__ == "__main__":
    app = wx.PySimpleApp()
    logging.basicConfig(level=logging.DEBUG,)
    bar = bar(None)
    bar.Show()
    
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
