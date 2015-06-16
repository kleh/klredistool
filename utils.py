import wx
class Util:

    # Decorator for checking connection
    
    def checkConnection(self,func):
        def check(*args):
            # args[0] is self from the calling class
            isconnected = args[0].appframe.connected
            if isconnected == False:
                wx.MessageBox('Not connected','Error',wx.OK | wx.ICON_ERROR)
                return
            else:
                return func(*args)
        return check
