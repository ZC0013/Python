# -*- coding: utf-8 -*-
from protocol.wellplan_pb2 import RigEquipment
from launcher import *
import helper
from rigController import *
import wellplanOperatorTest as test


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    re = pb2.RigEquipment()
    test.CreateRigEquipment(re)

    rig = RigController(cxt, re)
    rig.do()
