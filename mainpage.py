import wx
import redis
import sys

class mainPanel(wx.Panel):
    def __init__(self, parent, appframe):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.appframe = appframe

        self.lhost = wx.StaticText(self, label="Host",pos=(20,20))
        self.host = wx.TextCtrl(self, wx.ID_ANY, value="localhost",pos=(60,20))

        self.lport = wx.StaticText(self, label="Port",pos=(20,60))
        self.port = wx.TextCtrl(self, wx.ID_ANY, value="6379",pos=(60,60))

        self.bconnect = wx.Button(self,wx.ID_ANY,"Connect",pos=(60,120))

        self.Bind(wx.EVT_BUTTON,self.doConnect,self.bconnect)


    def doConnect(self, e):
        print "Connect"

        host = self.host.GetValue()
        port = self.port.GetValue()

        if host == "" or port == "":
            wx.MessageBox('You must define host and port','Error',wx.OK | wx.ICON_ERROR)
            return

        try:
            self.appframe.redisconnection = redis.StrictRedis(host=host, port=port, db=0)
            info = self.appframe.redisconnection.info()
            if isinstance(info,dict):
                self.appframe.statusbar.SetStatusText("Connected to " + host + " " + port)
                self.appframe.connected = True

        except:
            self.appframe.connected = False
            wx.MessageBox('Connection failed ' + str(sys.exc_info()),'Error',wx.OK | wx.ICON_ERROR)
