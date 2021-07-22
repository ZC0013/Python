import pyperclip

from protocol.wellplan_pb2 import FluidsEditor
from protocol.wellplan_pb2 import BarTab
from launcher import *
import helper
import wellplanOperatorTest as test
from fluidsController import *


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    f = pb2.FluidsEditor()
    test.CreateFluidsEditor(f)

    cxt.bar_t, cxt.bar_high, cxt.bar_idx = BarTab.TorqueDrag.FixedDepthPlots, BarTab.TorqueDrag(), BarTab.TorqueDrag.FixedDepthPlots.fdpTorque

    fluids = FluidsController(cxt, f)
    fluids.do()
