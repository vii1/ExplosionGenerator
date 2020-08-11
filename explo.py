import wx
from ui import Ventana


class MyApp(wx.App):

    def OnInit(self):
        # Data for the color dialog
        self.colourData = wx.ColourData()
        self.colourData.SetChooseAlpha(True)

        self.ventana = Ventana(None, wx.ID_ANY, "")
        self.SetTopWindow(self.ventana)

        # Image size widgets
        self.ventana.spinWidth.Bind(wx.EVT_SPINCTRL, self.spinWidth_OnChange)
        self.ventana.spinHeight.Bind(wx.EVT_SPINCTRL, self.spinHeight_OnChange)

        # Generate! button
        self.ventana.buttonGenerate.Bind(wx.EVT_BUTTON, self.buttonGenerate_OnClick)
        self.ventana.Layout()
        self.ventana.Show()
        return True

    def spinWidth_OnChange(self, event : wx.SpinEvent):
        if self.ventana.buttonLockSize.GetValue():
            self.ventana.spinHeight.SetValue(self.ventana.spinWidth.GetValue())

    def spinHeight_OnChange(self, event : wx.SpinEvent):
        if self.ventana.buttonLockSize.GetValue():
            self.ventana.spinWidth.SetValue(self.ventana.spinHeight.GetValue())

    def buttonGenerate_OnClick(self, event : wx.CommandEvent):
        pass

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
