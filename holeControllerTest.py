# -*- coding: utf-8 -*-

from protocol.wellplan_pb2 import HoleSectionEditor
from launcher import *
import helper
from holeController import *
import wellplanOperatorTest as test

if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    hs = pb2.HoleSectionEditor()
    test.CreateHoleSectionEditor(hs)

    holeSection = HoleController(cxt, hs)
    holeSection.do()
