import wx
from explo.pattern import GetPatternBrush

class ImageDisplay(wx.Window):
    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name=wx.PanelNameStr):
        super(wx.Window, self).__init__(parent, id=id, pos=pos, size=size, style=style, name=name)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, lambda _: self.Refresh())
        self._image = None

    def GetImage(self) -> wx.Bitmap:
        return self._image

    def SetImage(self, image: wx.Bitmap):
        self._image = image
        self.Refresh()

    Image = property(GetImage, SetImage)

    def OnPaint(self, event: wx.PaintEvent):
        dc = wx.PaintDC(self)
        if self._image == None:
            dc.SetBrush(wx.GREY_BRUSH)
            it = wx.RegionIterator(self.GetUpdateRegion())
            while it.HaveRects():
                rect = it.GetRect()
                dc.DrawRectangle(rect)
                it.Next()
            return
        clientRect = self.GetClientRect()
        bmp = wx.Bitmap(clientRect.Size)
        dc2 = wx.MemoryDC()
        dc2.SelectObject(bmp)
        gc = wx.GraphicsContext.Create(dc2)
        if not gc: return
        gc.SetBrush(wx.GREY_BRUSH)
        gc.DrawRectangle(clientRect.x, clientRect.y, clientRect.width, clientRect.height)
        rect = wx.Rect(self._image.Size)
        ratio = rect.width / rect.height
        if rect.width > rect.height:
            if rect.width > clientRect.width:
                rect.width = clientRect.width
                rect.height = clientRect.width / ratio
            elif rect.height > clientRect.height:
                rect.height = clientRect.height
                rect.width = clientRect.height * ratio
        else:
            if rect.height > clientRect.height:
                rect.height = clientRect.height
                rect.width = clientRect.height * ratio
            elif rect.width > clientRect.width:
                rect.width = clientRect.width
                rect.height = clientRect.width / ratio
        rect = rect.CenterIn(clientRect)
        gc.SetBrush(GetPatternBrush())
        gc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)
        gc.DrawBitmap(self._image, rect.x, rect.y, rect.width, rect.height)
        dc.Blit(0, 0, clientRect.width, clientRect.height, dc2, 0, 0)