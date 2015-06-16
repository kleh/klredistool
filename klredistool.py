# Small wxpython exercise
# Graphical Redis tool
# Connection and get+set for single value & lists
# About Redis see: http://redis.io/
# Python redis module: https://pypi.python.org/pypi/redis

# KL , 2015

import wx
import mainpage
import setpage
import getpage

FRAME_TITLE = "KL Redistool"
FRAME_SIZE  = (600,400)

def main():
    app = wx.App(False)
    frame = AppFrame()
    app.MainLoop()

class AppFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__( self, None, -1, FRAME_TITLE, size=FRAME_SIZE, style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU )
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.redisconnection = None
        self.connected = False

        # menu
        self.menu_bar  = wx.MenuBar()
        self.help_menu = wx.Menu()

        self.SetMenuBar(self.menu_bar)

        # Tabbed pages
        self.tabpage =  wx.Notebook(self,wx.ID_ANY)

        self.mainpanel = mainpage.mainPanel(self.tabpage, self)
        self.setpanel = setpage.setPanel(self.tabpage, self)
        self.getpanel = getpage.getPanel(self.tabpage, self)

        self.tabpage.AddPage(self.mainpanel, "Connection")
        self.tabpage.AddPage(self.setpanel, "Set data")
        self.tabpage.AddPage(self.getpanel, "Get data")

        self.sizer.Add(self.tabpage,1,wx.EXPAND)

        # statysbar
        self.statusbar = self.CreateStatusBar()

        # apply sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Show(1)

    

    def OnQuit(self, e):
        self.Close()


if __name__ == "__main__" :
    main()
