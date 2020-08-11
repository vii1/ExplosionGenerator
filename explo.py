import wx
from ui import Ventana
from explosiongenerator import ExplosionGenerator

def _first(iterable, condition = lambda x: True):
    """
    Returns the first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, returns the first item of
    the iterable.

    Raises `StopIteration` if no item satysfing the condition is found.

    >>> first( (1,2,3), condition=lambda x: x % 2 == 0)
    2
    >>> first(range(3, 100))
    3
    >>> first( () )
    Traceback (most recent call last):
    ...
    StopIteration
    """

    return next(x for x in iterable if condition(x))

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
        size = wx.Size(self.ventana.spinWidth.Value, self.ventana.spinHeight.Value)
        gradient = self.ventana.gradientWidget.GetGradientAsStops()
        _, type = _first(
            {self.ventana.radioTypeA: 'A', self.ventana.radioTypeB: 'B', self.ventana.radioTypeC: 'C'}.items(),
            lambda x: x[0].Value)
        frames = self.ventana.spinNumFrames.Value
        points = self.ventana.spinGranularity.Value
        seed = None
        exp = ExplosionGenerator(size, gradient, type, frames, points, seed)
        dialog = wx.ProgressDialog("Generando...", f"Preparando...", frames, self.ventana, wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT | wx.PD_ESTIMATED_TIME)
        bmps = exp.CreateFrames(dialog)
        dialog.Hide()
        dialog.Destroy()
        if bmps != None:
            for i, bmp in enumerate(bmps):
                bmp.SaveFile("r:\\explo%03d.png" % i, wx.BITMAP_TYPE_PNG)

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
