import wx

_pattern_bmp = None
_pattern_brush = None

def GetPatternBitmap():
    global _pattern_bmp
    if _pattern_bmp == None:
        _pattern_bmp = wx.Bitmap("pattern.png")
    return _pattern_bmp

def GetPatternBrush():
    global _pattern_brush
    if _pattern_brush == None:
        _pattern_brush = wx.Brush(GetPatternBitmap())
    return _pattern_brush
