# -*- coding: utf-8 -*-

import uiautomation as auto

class Context(object):
    LastErrorCode = None
    TopWindow: auto.WindowControl = None

    #选项
    bar_t = None
    bar_high = None
    bar_idx = None

    def cancel(self):
        pass