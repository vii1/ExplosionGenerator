import wx
import wx.lib.newevent
from pattern import GetPatternBrush

try:
    from agw import cubecolourdialog as CCD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.cubecolourdialog as CCD

ColorPickerEvent, EVT_COLOR_PICKER = wx.lib.newevent.NewCommandEvent()

class ColorPicker(wx.Button):
    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition,
       size=wx.DefaultSize, style=wx.BU_EXACTFIT, validator=wx.DefaultValidator,
       name=wx.ButtonNameStr):
        super(wx.Button, self).__init__(parent, id=id, label=label, size=size, style=style, validator=validator, name=name)
        self.parent = parent

        self._colour = wx.Colour()
        self.SetWindowStyle(wx.BORDER_SUNKEN)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_BUTTON, self.OnClick)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.Create(parent)

    def GetColour(self):
        return self._colour

    def SetColour(self, colour : wx.Colour):
        self._colour = colour
        self.Refresh()

    Colour = property(GetColour, SetColour, doc="Selected colour")

    def OnClick(self, event : wx.CommandEvent):
        if self.parent and '_colourdata' in self.parent.__dict__:
            colourdata = self.parent._colourdata
        else:
            colourdata = wx.ColourData()
        colourdata.Colour = self._colour
        dialog = CCD.CubeColourDialog(self, colourdata)
        if dialog.ShowModal() == wx.ID_OK:
            colourdata = dialog.GetColourData()
            self.Colour = wx.Colour(colourdata.GetColour())
            if self.parent and '_colourdata' in self.parent.__dict__:
                self.parent._colourdata = colourdata
            e = ColorPickerEvent(self.GetId())
            e.SetEventObject(self)
            wx.PostEvent(self, e)

    def OnPaint(self, event : wx.PaintEvent):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        upd = wx.RegionIterator(self.GetUpdateRegion())
        while upd.HaveRects():
            rect = upd.GetRect()
            if self._colour.alpha < wx.ALPHA_OPAQUE:
                gc.SetBrush(GetPatternBrush())
                gc.DrawRectangle(rect.X, rect.Y, rect.Width, rect.Height)
            gc.SetBrush(wx.TheBrushList.FindOrCreateBrush(self._colour))
            gc.DrawRectangle(rect.X, rect.Y, rect.Width, rect.Height)
            upd.Next()
        gc.SetBrush(wx.TRANSPARENT_BRUSH)
        gc.SetPen(wx.BLACK_PEN)
        rect = self.GetClientRect()
        gc.DrawRectangle(rect.X, rect.Y, rect.Width-1, rect.Height-1)
        if self.HasFocus():
            rect.Deflate(2)
            renderer = wx.RendererNative.Get()
            renderer.DrawFocusRect(self, dc, rect)