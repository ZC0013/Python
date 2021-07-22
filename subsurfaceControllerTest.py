# -*- coding: utf-8 -*-
import pyperclip

from protocol.wellplan_pb2 import SubsurfaceEditor
from launcher import *
import helper
from subsurfaceController import *

import wellplanOperatorTest as test

if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    s = pb2.SubsurfaceEditor()
    test.CreateSubsurfaceEditor(s)

    subsurface = SubsurfaceController(cxt, s)
    subsurface.do()

