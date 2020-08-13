#
# Explosion Generator
#
# Main program module
#

import wx
from .ui import Ventana
from .explosiongenerator import ExplosionGenerator

def _first(iterable, condition=lambda x: True):
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
    "Main application class"

    def OnInit(self):
        return True

    def Start(self):
        "UI setup and event bindings"

        # Data for the color dialog
        self.colourData = wx.ColourData()
        self.colourData.SetChooseAlpha(True)

        # Main window
        self.ventana = Ventana(None, wx.ID_ANY, "")
        self.SetTopWindow(self.ventana)

        # Image size widgets
        self.ventana.spinWidth.Bind(wx.EVT_SPINCTRL, self.spinWidth_OnChange)
        self.ventana.spinHeight.Bind(wx.EVT_SPINCTRL, self.spinHeight_OnChange)

        # Generate! button
        self.ventana.buttonGenerate.Bind(wx.EVT_BUTTON, self.buttonGenerate_OnClick)

        # Animation controls and display
        self.bmps = None
        self.ventana.sliderPreview.Bind(wx.EVT_SLIDER, self.sliderPreview_OnChange)
        self.ventana.buttonPlayPause.Bind(wx.EVT_TOGGLEBUTTON, self.buttonPlayPause_OnToggle)
        self.ventana.spinFps.Bind(wx.EVT_SPINCTRL, self.spinFps_OnChange)
        self.controlesResultado = (
            self.ventana.buttonPlayPause,
            self.ventana.sliderPreview,
            self.ventana.labelVelocidad,
            self.ventana.spinFps,
            self.ventana.labelFPS,
            self.ventana.buttonSave
        )
        for w in self.controlesResultado:
            w.Enable(False)
        self.ventana.spinFps.Value = 10
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_Tick)

        # Save button
        self.ventana.buttonSave.Bind(wx.EVT_BUTTON, self.buttonSave_OnClick)

        self.ventana.Layout()
        self.ventana.Show()

    def spinWidth_OnChange(self, event: wx.SpinEvent):
        # Change both spinners if buttonLockSize is pushed
        if self.ventana.buttonLockSize.GetValue():
            self.ventana.spinHeight.SetValue(self.ventana.spinWidth.GetValue())

    def spinHeight_OnChange(self, event: wx.SpinEvent):
        # Change both spinners if buttonLockSize is pushed
        if self.ventana.buttonLockSize.GetValue():
            self.ventana.spinWidth.SetValue(self.ventana.spinHeight.GetValue())

    def buttonGenerate_OnClick(self, event: wx.CommandEvent):
        # Collect all configured properties
        size = wx.Size(self.ventana.spinWidth.Value, self.ventana.spinHeight.Value)
        gradient = self.ventana.gradientWidget.GetGradientAsStops()
        _x, type = _first(
            {self.ventana.radioTypeA: 'A', self.ventana.radioTypeB: 'B', self.ventana.radioTypeC: 'C'}.items(),
            lambda x: x[0].Value)
        frames = self.ventana.spinNumFrames.Value
        points = self.ventana.spinGranularity.Value
        # TODO: Allow the user to specify a seed
        seed = None

        # Begin the process
        dialog = wx.ProgressDialog(_("Generating..."), _("Starting..."), frames, self.ventana,
                                   wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT | wx.PD_REMAINING_TIME | wx.PD_ESTIMATED_TIME)
        exp = ExplosionGenerator(size, gradient, type, frames, points, seed)
        try:
            bmps = exp.CreateFrames(dialog)
        finally:
            dialog.Hide()
            dialog.Destroy()
        if bmps != None:
            self.SetAnimation(bmps)

    def SetAnimation(self, bmps):
        "Does everything needed when a new animation is created"
        self.timer.Stop()
        self.bmps = bmps
        for w in self.controlesResultado:
            w.Enable(True)
        self.ventana.buttonPlayPause.Value = False
        self.ventana.sliderPreview.Value = 0
        self.ventana.sliderPreview.SetMax(len(bmps) - 1)
        self.ventana.imageDisplay.SetImage(bmps[0])

    def sliderPreview_OnChange(self, event: wx.CommandEvent):
        "Selects current frame of animation"
        self.ventana.imageDisplay.SetImage(self.bmps[self.ventana.sliderPreview.Value])

    def timer_Tick(self, event: wx.TimerEvent):
        "Timer for animation preview"
        frame = self.ventana.sliderPreview.Value
        if frame < self.ventana.sliderPreview.Max:
            frame += 1
        else:
            frame = 0
        self.ventana.sliderPreview.Value = frame
        self.ventana.imageDisplay.SetImage(self.bmps[frame])

    def buttonPlayPause_OnToggle(self, event: wx.CommandEvent):
        "Starts/stops the animation"
        if self.ventana.buttonPlayPause.Value:
            self.timer.Start(round(1000 / self.ventana.spinFps.Value))
        else:
            self.timer.Stop()

    def spinFps_OnChange(self, event: wx.SpinEvent):
        "If the animation is playing, changes speed on the fly"
        if self.ventana.buttonPlayPause.Value:
            self.timer.Stop()
            self.timer.Start(round(1000 / self.ventana.spinFps.Value))

    def buttonSave_OnClick(self, event: wx.CommandEvent):
        import os.path
        tipos = '|'.join((
            _("PNG (*.png)"), "*.png"
        ))
        with wx.FileDialog(parent=self.ventana, message=_("Save animation"), wildcard=tipos,
                           style=wx.FD_SAVE) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dialog.GetPath()
        try:
            dir, name = os.path.split(path)
            name, ext = os.path.splitext(name)
            if ext == "": ext = ".png"
            width = len(str(len(self.bmps) - 1))
            fmt = os.path.join(dir, name) + "%0" + str(width) + "d" + ext
            for i, bmp in enumerate(self.bmps):
                bmp.SaveFile(fmt % i, wx.BITMAP_TYPE_PNG)
        except Exception as e:
            wx.MessageBox(_("An error occured while saving: %s") % str(e), caption=_("Error while saving"),
                          style=wx.OK | wx.CENTRE | wx.ICON_ERROR, parent=self.ventana)
