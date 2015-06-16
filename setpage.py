import wx
import redis
import sys

VALUEITEMS = 5

class setPanel(wx.Panel):
    def __init__(self, parent, appframe):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.typeitems = ("Single", "List")

        self.values = []

        self.appframe = appframe

        self.ltypeselection = wx.StaticText(self, label="Type",pos=(20,20))
        self.typeselection = wx.ListBox(self, wx.ID_ANY, pos=(100,20),size=(160,60),
            style=wx.LB_NEEDED_SB | wx.LB_SINGLE, choices=self.typeitems )

        self.typeselection.SetSelection(0)
        self.selectedtype = self.typeitems[0]


        self.lkey = wx.StaticText(self, label="Key",pos=(20,140))

        self.key = wx.TextCtrl(self, wx.ID_ANY, value="",pos=(100,140))

        self.lvalue = wx.StaticText(self, label="Value",pos=(220,140))
        self.value = wx.TextCtrl(self, 400, value="",pos=(270,140),size=(200,20))

        # Create fields for values
        # Show always first one
        for x in range(VALUEITEMS):
            v = wx.TextCtrl(self, wx.ID_ANY, value="",pos=(270,140 + x * 30),size=(200,20))
            if x > 0:
                v.Hide()

            self.values.append(v)

        self.bsave = wx.Button(self,wx.ID_ANY,"Save",pos=(60,190))

        # Bind actions
        self.Bind(wx.EVT_LISTBOX,self.typeSelected, self.typeselection)
        self.Bind(wx.EVT_BUTTON,self.saveToRedis, self.bsave)


    def typeSelected(self, e):
        selindex = self.typeselection.GetSelection()
        self.selectedtype = self.typeitems[selindex]

        for x in range(VALUEITEMS):
            if x > 0 and self.selectedtype == "List":
                self.values[x].Show()
            elif self.selectedtype == "Single":
                self.values[x].SetValue("")
                self.values[x].Hide()

    def saveToRedis(self,e):
        if self.appframe.connected == False:
            wx.MessageBox('Not connected','Error',wx.OK | wx.ICON_ERROR)
            return

        key = self.key.GetValue()
        if key == "":
            wx.MessageBox('Missing key','Error',wx.OK | wx.ICON_ERROR)
            return

        print(self.values[0].GetValue())

        # Save single value
        if self.selectedtype == "Single":
            value = self.values[0].GetValue()
            if value == "":
                wx.MessageBox('Missing value','Error',wx.OK | wx.ICON_ERROR)
                return

            self.appframe.redisconnection.set(key, value)

        # Save list
        elif self.selectedtype == "List":
            cv = 0
            for v in self.values:
                if not v.GetValue() == "":
                    cv = cv +1
                    self.appframe.redisconnection.rpush(key, v.GetValue())
            if cv == 0:
                wx.MessageBox('Missing values','Error',wx.OK | wx.ICON_ERROR)
                return

        else:
            return

        self.appframe.statusbar.SetStatusText("Saved " + key)
