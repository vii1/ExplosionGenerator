import os
import sys
import gettext
import wx
from explo.explo import MyApp

abspath = os.path.abspath(os.path.realpath(sys.argv[0]))
dname = os.path.dirname(abspath)
os.chdir(os.path.join(dname, "explo"))

localedir = os.path.join(dname, "locale")
domain = 'explo'

app = MyApp(0)

# Set locale for wxWidgets
langid = wx.Locale.GetSystemLanguage()
if langid == wx.LANGUAGE_UNKNOWN:
    langid = wx.LANGUAGE_DEFAULT
mylocale = wx.Locale(langid)
mylocale.AddCatalogLookupPathPrefix(localedir)
mylocale.AddCatalog(domain)

# Set up Python's gettext
mytranslation = gettext.translation(domain, localedir, [mylocale.GetCanonicalName()], fallback=True)
mytranslation.install()

if __name__ == '__main__':
    app.Start()
    app.MainLoop()
