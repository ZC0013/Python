# -*- coding: utf-8 -*-

import config
import pyperclip

from protocol.wellplan_pb2 import WellpathEditor
from launcher import *
from wellpathController import *

import wellplanOperatorTest as test

if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    we = WellpathEditor()
    test.CreateWellpathEditor(we)

    wellpath = WellpathController(cxt, we)
    wellpath.do()
