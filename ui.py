# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Thu Aug 13 11:34:56 2020
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade
from gettext import gettext as _

# begin wxGlade: extracode
from imagedisplay import ImageDisplay
from gradientwidget import GradientWidget
# end wxGlade


class Ventana(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Ventana.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((815, 494))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.spinWidth = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "128", min=1, max=65535)
        self.spinHeight = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "128", min=1, max=65535)
        self.buttonLockSize = wx.ToggleButton(self.panel_1, wx.ID_ANY, "", style=wx.BU_EXACTFIT)
        self.gradientWidget = GradientWidget(self.panel_1, wx.ID_ANY)
        self.radioTypeA = wx.RadioButton(self.panel_1, wx.ID_ANY, _("Type A"), style=wx.RB_GROUP)
        self.radioTypeB = wx.RadioButton(self.panel_1, wx.ID_ANY, _("Type B"))
        self.radioTypeC = wx.RadioButton(self.panel_1, wx.ID_ANY, _("Type C"))
        self.spinNumFrames = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "6", min=1, max=65535)
        self.spinGranularity = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        self.buttonGenerate = wx.Button(self.panel_1, wx.ID_ANY, _("Generate!"))
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.imageDisplay = ImageDisplay(self.panel_2, wx.ID_ANY)
        self.buttonPlayPause = wx.ToggleButton(self.panel_2, wx.ID_ANY, "", style=wx.BU_EXACTFIT)
        self.sliderPreview = wx.Slider(self.panel_2, wx.ID_ANY, 0, 0, 10)
        self.labelVelocidad = wx.StaticText(self.panel_2, wx.ID_ANY, _("Speed"))
        self.spinFps = wx.SpinCtrlDouble(self.panel_2, wx.ID_ANY, "24.0", min=0.1, max=100.0)
        self.labelFPS = wx.StaticText(self.panel_2, wx.ID_ANY, _("FPS"))
        self.buttonSave = wx.Button(self.panel_2, wx.ID_ANY, _("Save"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Ventana.__set_properties
        self.SetTitle(_("Explosion generator"))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("img/icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.buttonLockSize.SetToolTip(_(u"Forzar proporción cuadrada"))
        self.buttonLockSize.SetValue(True)
        self.buttonLockSize.SetBitmap(wx.Bitmap("img/lock_open.png", wx.BITMAP_TYPE_ANY))
        self.buttonLockSize.SetBitmapPressed(wx.Bitmap("img/lock.png", wx.BITMAP_TYPE_ANY))
        self.radioTypeA.SetValue(1)
        self.spinNumFrames.SetMinSize((60, 23))
        self.spinGranularity.SetMinSize((60, 23))
        self.buttonGenerate.SetBitmap(wx.Bitmap("img/lightning.png", wx.BITMAP_TYPE_ANY))
        self.buttonPlayPause.SetBitmap(wx.Bitmap("img/control_play_blue.png", wx.BITMAP_TYPE_ANY))
        self.buttonPlayPause.SetBitmapPressed(wx.Bitmap("img/control_pause_blue.png", wx.BITMAP_TYPE_ANY))
        self.spinFps.SetMinSize((80, 23))
        self.buttonSave.SetBitmap(wx.Bitmap("img/diskette.png", wx.BITMAP_TYPE_ANY))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Ventana.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerResultado = wx.StaticBoxSizer(wx.StaticBox(self.panel_2, wx.ID_ANY, _("Result")), wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, _("Parameters")), wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(5, 2, 2, 2)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Size"))
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(self.spinWidth, 0, 0, 0)
        label_7 = wx.StaticText(self.panel_1, wx.ID_ANY, _(u"×"))
        sizer_2.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 3)
        sizer_2.Add(self.spinHeight, 0, 0, 0)
        label_8 = wx.StaticText(self.panel_1, wx.ID_ANY, _("pixels"))
        sizer_2.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 3)
        sizer_2.Add((8, 1), 0, 0, 0)
        sizer_2.Add(self.buttonLockSize, 0, 0, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.ALL | wx.EXPAND, 0)
        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Gradient"))
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.gradientWidget, 1, wx.EXPAND, 0)
        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Type"))
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.radioTypeA, 0, 0, 0)
        sizer_8.Add(self.radioTypeB, 0, 0, 0)
        sizer_8.Add(self.radioTypeC, 0, 0, 0)
        grid_sizer_1.Add(sizer_8, 1, wx.EXPAND, 0)
        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Frames"))
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.spinNumFrames, 0, 0, 0)
        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Granularity"))
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.spinGranularity, 0, 0, 0)
        sizer_6.Add(grid_sizer_1, 0, wx.ALL | wx.EXPAND, 5)
        sizer_6.Add(self.buttonGenerate, 0, wx.ALIGN_CENTER, 0)
        self.panel_1.SetSizer(sizer_6)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        sizerResultado.Add(self.imageDisplay, 1, wx.EXPAND, 0)
        sizer_5.Add(self.buttonPlayPause, 0, 0, 0)
        sizer_5.Add(self.sliderPreview, 1, wx.EXPAND, 0)
        sizerResultado.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_4.Add(self.labelVelocidad, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(self.spinFps, 0, wx.LEFT | wx.RIGHT, 3)
        sizer_4.Add(self.labelFPS, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add((20, 20), 1, 0, 0)
        sizer_4.Add(self.buttonSave, 0, wx.ALL, 0)
        sizerResultado.Add(sizer_4, 0, wx.EXPAND, 0)
        self.panel_2.SetSizer(sizerResultado)
        sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class Ventana
