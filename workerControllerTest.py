# -*- coding: utf-8 -*-
from protocol.wellplan_pb2 import OperationalParameters
from launcher import *
import helper
from workerController import *

import wellplanOperatorTest as test


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    op = OperationalParameters()
    test.CreateOperations(op)

    worker = WorkerController(cxt, op)
    worker.do()