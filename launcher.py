# -*- coding: utf-8 -*-

import win32api

import config
import errorcode
import uiautomation as auto

from network import listener
from SimpleWebSocketServer import WebSocket
from context import *
from loguru import logger


class Launcher:
    '''
        用于启动Wellplan软件
    '''
    cxt = Context()
    conn: WebSocket = None

    def isConnected(self):
        return self.conn is not None

    def __init__(self, cxt: Context, conn: WebSocket = None):
        self.cxt = cxt
        self.conn = conn

    '''
        查询相应已打开的
    '''
    def update(self):
        self.cxt.TopWindow = auto.WindowControl(searchDepth=1, AutomationId='AppFoundation', ClassName='Window')
        logger.info('启动该软件，等待 60s 查询该窗口...\n')
        if auto.WaitForExist(self.cxt.TopWindow, config.MINUTE):
            self.cxt.TopWindow.SetActive()
            self.cxt.TopWindow.Show()
        else:
            self.cxt.LastErrorCode = errorcode.LAUNCH_FAILED
            self.cxt.cancel()

    def do(self):
        logger.info('启动软件...')

        self.cxt.TopWindow = auto.WindowControl(searchDepth=1, AutomationId='AppFoundation', ClassName='Window')
        #不存在则启动
        if not self.cxt.TopWindow.Exists(0, 0):
            win32api.ShellExecute(0, 'open', config.LAUNCH, '', config.LAUNCH_ENV, 0)

        if self.isConnected():
            listener.sendStatus(self.conn, "正在启动")

        logger.info('启动该软件，等待 60s 查询该窗口...\n')
        if auto.WaitForExist(self.cxt.TopWindow, config.MINUTE):
            self.cxt.TopWindow.SetActive()
            self.cxt.TopWindow.Show()
        else:
            self.cxt.LastErrorCode = errorcode.LAUNCH_FAILED
            self.cxt.cancel()

        logger.info('启动结束...')

        if self.isConnected():
            listener.sendStatus(self.conn, "启动完毕")


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

