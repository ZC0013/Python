# -*- coding: utf-8 -*-

import helper

from protocol.wellplan_pb2 import BarTab
from launcher import *
from barController import *


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    bar = BarController(cxt)
    #bar.Layout_Reset()
    bar.do(BarTab.TorqueDrag(), BarTab.TorqueDrag.FixedDepthPlots, BarTab.TorqueDrag.FixedDepthPlots.fdpTorque)
