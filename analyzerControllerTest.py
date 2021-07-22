# -*- coding: utf-8 -*-
import wellplanOperatorTest as test

from protocol.wellplan_pb2 import AnalysisSetting
from analyzerController import *
from launcher import *
import helper
from context import *
import uiautomation as auto


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    aa = AnalysisSetting()
    test.CreateAnalysis(aa)

    aCtl = AnalyzerController(cxt, aa)
    aCtl.do()


