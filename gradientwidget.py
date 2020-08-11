import wx
import wx.lib.newevent
from colorpicker import ColorPicker, ColorPickerEvent, EVT_COLOR_PICKER

GradientWidgetEvent, EVT_GRADIENT_WIDGET = wx.lib.newevent.NewCommandEvent()


class GradientWidget(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString, num_stops=9):
        super(wx.Panel, self).__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        self.parent = parent

        self._numstops = num_stops
        self._colourdata = wx.ColourData()
        self._colourdata.SetChooseAlpha(True)
        self._CreateUI()
        self.UpdateGradient()
        self.Layout()

    def _CreateUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._preview = wx.Control(self)
        self._preview.SetMinSize((-1, 10))
        self._preview.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self._preview.Bind(wx.EVT_PAINT, self._PaintPreview)
        self._preview.Bind(wx.EVT_SIZE, lambda _: self._preview.Refresh())
        sizer.Add(self._preview, 0, wx.EXPAND)

        self._pickers = [ColorPicker(self) for i in range(self._numstops)]
        self._pickers[0].Colour = wx.Colour(255, 255, 255)
        self._pickers[-1].Colour = wx.Colour(0, 0, 0)
        self._checks = [wx.CheckBox(self) for i in range(self._numstops)]
        self._pickers[self._numstops // 3].Colour = wx.YELLOW
        self._checks[self._numstops // 3].Value = True
        self._pickers[self._numstops // 3 * 2].Colour = wx.RED
        self._checks[self._numstops // 3 * 2].Value = True
        for i in (0, -1):
            self._checks[i].SetValue(True)
            self._checks[i].Disable()
        for i in range(self._numstops):
            self._pickers[i].Bind(EVT_COLOR_PICKER, self.OnColorPicked)
        for i in range(1, self._numstops - 1):
            self._checks[i].Bind(wx.EVT_CHECKBOX, self.OnCheckChanged)

        self._grid = wx.FlexGridSizer(2, self._numstops, 0, 1)
        for i in range(self._numstops):
            self._grid.AddGrowableCol(i, 1)
        self._grid.AddMany([(p, 1, wx.EXPAND) for p in self._pickers])
        self._grid.AddMany([(c, 0, wx.ALIGN_CENTER) for c in self._checks])
        sizer.Add(self._grid, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def _PaintPreview(self, event: wx.PaintEvent):
        dc = wx.PaintDC(self._preview)
        gc = wx.GraphicsContext.Create(dc)
        if not gc: return
        rect = self._preview.GetClientRect()
        asStops = self.GetGradientAsStops()
        stops = wx.GraphicsGradientStops(asStops[0][0], asStops[-1][0])
        for col, pos in asStops[1:-1]:
            stops.Add(col, pos)
        brush = gc.CreateLinearGradientBrush(0, 0, rect.GetWidth() - 1, 0, stops)
        gc.SetBrush(brush)
        gc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())

    def GetNumStops(self):
        return self._numstops

    def SetNumStops(self, n):
        n = int(n)
        if n < 2 or n > 32:
            raise ValueError("num_stops must be between 2 and 32")
        if n == self._numstops: return
        # self._grid.Clear(True)
        self.GetSizer().Clear(True)
        self.SetSizer(None)
        self._pickers = None
        self._checks = None
        self._numstops = n
        self._CreateUI()
        self.UpdateGradient()
        self.Layout()

    NumStops = property(GetNumStops, SetNumStops, doc="Number of editable stops in the gradient")

    def OnColorPicked(self, event: ColorPickerEvent):
        obj = event.GetEventObject()
        if not obj in self._pickers: return
        index = self._pickers.index(obj)
        if self._checks[index].GetValue() == False:
            self._checks[index].SetValue(True)
        self.UpdateGradient()
        wx.PostEvent(self, GradientWidgetEvent(self.GetId()))

    def OnCheckChanged(self, event: wx.CommandEvent):
        self.UpdateGradient()
        wx.PostEvent(self, GradientWidgetEvent(self.GetId()))

    def UpdateGradient(self):
        colors = self.GetGradientAsColors()
        enable = [c.GetValue() for c in self._checks]
        desde = 0
        while desde < self._numstops - 2:
            hasta = enable[desde + 1:].index(True) + desde + 1
            if hasta > desde + 1:
                pasos = hasta - desde
                dr = (colors[hasta].red - colors[desde].red) / pasos
                dg = (colors[hasta].green - colors[desde].green) / pasos
                db = (colors[hasta].blue - colors[desde].blue) / pasos
                da = (colors[hasta].alpha - colors[desde].alpha) / pasos
                for i in range(hasta - desde - 1):
                    colors[desde + i + 1] = wx.Colour(
                        round(colors[desde].red + dr * (i + 1)),
                        round(colors[desde].green + dg * (i + 1)),
                        round(colors[desde].blue + db * (i + 1)),
                        round(colors[desde].alpha + da * (i + 1)))
            desde = hasta
        for i in range(self._numstops):
            self._pickers[i].Colour = colors[i]
        self._preview.Refresh()

    def GetGradientAsColors(self):
        return [p.Colour for p in self._pickers]

    def GetGradientAsStops(self):
        colors = self.GetGradientAsColors()
        enable = [c.GetValue() for c in self._checks]
        return [(col, idx / (self._numstops - 1)) for col, idx, _ in
                filter(lambda x: x[2], zip(colors, range(self._numstops), enable))]


def main():
    class TestApp(wx.App):
        def OnInit(self):
            testWindow = wx.Frame(None, wx.ID_ANY, "GradientWidget", style=wx.DEFAULT_FRAME_STYLE)
            sizer = wx.BoxSizer(wx.VERTICAL)
            self._grad = GradientWidget(testWindow)
            sizer.Add(self._grad, 1, wx.EXPAND)
            testWindow.SetSizerAndFit(sizer)
            self.SetTopWindow(testWindow)
            testWindow.SetAutoLayout(True)
            testWindow.Show()
            return True

    app = TestApp(0)
    app.MainLoop()


if __name__ == "__main__":
    main()
