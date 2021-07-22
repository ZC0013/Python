# -*- coding: utf-8 -*-

import sys
import time
from wellplan import *
import wellplanOperatorTest as test
from protocol.wellplan_pb2 import BarTab

if __name__ == '__main__':
    op = WellPlanState()
    op.on_open()
    op.on_loginUser()
    op.on_resource()
