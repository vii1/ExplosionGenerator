import os
import sys
from explo.explo import MyApp

abspath = os.path.abspath(os.path.realpath(sys.argv[0]))
dname = os.path.dirname(abspath)
os.chdir(dname)

app = MyApp(0)
app.MainLoop()
