# -*- coding: utf-8 -*-
import pyperclip

from protocol.wellplan_pb2 import StringEditor
from launcher import *
import helper
from stringController import *

import wellplanOperatorTest as test


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    s = pb2.StringEditor()
    test.CreateStringEditor(s)

    string = StringController(cxt, s)
    string.do()



