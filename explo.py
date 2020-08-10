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
        self.ventana.buttonLockSize.SetValue(True)

        self.ventana.gridGradient.Clear()
        gradientPanels = [wx.Panel(self.ventana, size=(24, 24), style=wx.TAB_TRAVERSAL|wx.BORDER_SUNKEN) for i in range(9)]
        self.ventana.gridGradient.AddMany([(panel, wx.ALIGN_CENTER_HORIZONTAL) for panel in gradientPanels])

        gradientChecks = [wx.CheckBox(self.ventana) for i in range(9)]
        self.ventana.gridGradient.AddMany([(check, 0, wx.ALIGN_CENTER_HORIZONTAL) for check in gradientChecks])
        
        for i in (0, -1):
            gradientChecks[i].SetValue(True)
            gradientChecks[i].Disable()

        gradientPanels[0].SetBackgroundColour(wx.Colour(255,255,255))
        gradientPanels[8].SetBackgroundColour(wx.Colour(0,0,0))

        self.gradientPanels = gradientPanels
        self.gradientChecks = gradientChecks

        for i in range(9):
            gradientPanels[i].index = i
            gradientPanels[i].Bind(wx.EVT_LEFT_UP, self.panelGradient_OnClick)
            gradientChecks[i].index = i
            gradientChecks[i].Bind(wx.EVT_CHECKBOX, self.panelCheck_OnCheck)

        self.ventana.panelPreviewGradient.Bind(wx.EVT_PAINT, self.panelPreviewGradient_OnPaint)
        
        self.ventana.Layout()
        self.UpdateGradient()
        self.ventana.Show()
        return True

    def spinWidth_OnChange(self, event : wx.SpinEvent):
        if self.ventana.buttonLockSize.GetValue():
            self.ventana.spinHeight.SetValue(self.ventana.spinWidth.GetValue())

    def spinHeight_OnChange(self, event : wx.SpinEvent):
        if self.ventana.buttonLockSize.GetValue():
            self.ventana.spinWidth.SetValue(self.ventana.spinHeight.GetValue())

    def panelCheck_OnCheck(self, event : wx.CommandEvent):
        self.UpdateGradient()

    def panelGradient_OnClick(self, event : wx.MouseEvent):
        index = event.GetEventObject().index
        self.colourData.SetColour(self.gradientPanels[index].GetBackgroundColour())
        dialog = wx.ColourDialog(self.ventana, self.colourData)
        if dialog.ShowModal() == wx.ID_OK:
            self.colourData = dialog.GetColourData()
            index = event.GetEventObject().index
            self.gradientPanels[index].SetBackgroundColour(self.colourData.GetColour())
            # self.gradientPanels[index].Refresh()
            if self.gradientChecks[index].GetValue() == False:
                self.gradientChecks[index].SetValue(True)
            self.UpdateGradient()


    def panelPreviewGradient_OnPaint(self, event : wx.PaintEvent):
        dc = wx.PaintDC(self.ventana.panelPreviewGradient)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
        rect = self.ventana.panelPreviewGradient.GetClientRect()
        colors = [p.GetBackgroundColour() for p in self.gradientPanels]
        enable = [c.GetValue() for c in self.gradientChecks]
        stops = wx.GraphicsGradientStops(colors[0], colors[-1])
        for col, idx, _ in filter(lambda x: x[2], zip(colors[1:-1], range(1, len(colors)-1), enable[1:-1])):
            stops.Add(col, idx / len(colors))
        brush = gc.CreateLinearGradientBrush(0, 0, rect.GetWidth()-1, 0, stops)
        gc.SetBrush(brush)
        gc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())

    def UpdateGradient(self):
        colors = [p.GetBackgroundColour() for p in self.gradientPanels]
        enable = [c.GetValue() for c in self.gradientChecks]
        desde = 0
        while desde < 7:
            hasta = enable[desde+1:].index(True) + desde + 1
            if hasta > desde + 1:
                pasos = hasta - desde
                dr = (colors[hasta].red - colors[desde].red) / pasos
                dg = (colors[hasta].green - colors[desde].green) / pasos
                db = (colors[hasta].blue - colors[desde].blue) / pasos
                da = (colors[hasta].alpha - colors[desde].alpha) / pasos
                for i in range(hasta-desde-1):
                    colors[desde+i+1] = wx.Colour(
                        round(colors[desde].red + dr*(i+1)),
                        round(colors[desde].green + dg*(i+1)),
                        round(colors[desde].blue + db*(i+1)),
                        round(colors[desde].alpha + da*(i+1)))
            desde = hasta
        for i in range(9):
            self.gradientPanels[i].SetBackgroundColour(colors[i])
            self.gradientPanels[i].Refresh()
        self.ventana.panelPreviewGradient.Refresh()

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
