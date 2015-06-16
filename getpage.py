import wx
import redis
import sys

class getPanel(wx.Panel):
    def __init__(self, parent, appframe):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.appframe = appframe

        self.lkey = wx.StaticText(self, label="Key",pos=(20,20))

        self.key = wx.TextCtrl(self, wx.ID_ANY, value="",pos=(100,20))

        self.value = wx.TextCtrl(self, 400, value="",pos=(20,70),size=(400,200),
            style=wx.TE_MULTILINE | wx.TE_READONLY )

        self.bget = wx.Button(self,wx.ID_ANY,"Get data",pos=(200,20))

        # Bind actions
        self.Bind(wx.EVT_BUTTON,self.getData, self.bget)


    def getData(self,e):
        if self.appframe.connected == False:
            wx.MessageBox('Not connected','Error',wx.OK | wx.ICON_ERROR)
            return

        key = self.key.GetValue()
        if key == "":
            wx.MessageBox('Missing key','Error',wx.OK | wx.ICON_ERROR)
            return

        keytype = self.appframe.redisconnection.type(key)

        if keytype == "string":
            self.value.SetValue(str(self.appframe.redisconnection.get(key)))
        elif keytype == "list":
            self.value.SetValue(str(self.appframe.redisconnection.lrange(key,0,-1)))
