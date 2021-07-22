# -*- coding: utf-8 -*-

import helper
from loguru import logger
from launcher import *
from network import listener

class LoginManager:
    cxt = Context()
    conn: WebSocket = None

    def __init__(self, cxt : Context, conn: WebSocket = None):
        self.cxt = cxt
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def do(self):
        logger.info('开始登陆用户...')
        if self.isConnected():
            listener.sendStatus(self.conn, "登陆中")
        if helper.ExistCtrl(self.cxt.TopWindow):
            Datasource = self.cxt.TopWindow.ComboBoxControl(searchDepth=2, ClassName='ComboBox', AutomationId='_dataSources')
            User = self.cxt.TopWindow.EditControl(searchDepth=2, AutomationId='_user', ClassName='TextBox')
            PWD = self.cxt.TopWindow.EditControl(searchDepth=2, AutomationId='_password', ClassName='PasswordBox')
            Login = self.cxt.TopWindow.ButtonControl(searchDepth=3, Name='登录', ClassName='Button')

            helper.SetCtrlComboBoxValue(Datasource, 1)
            helper.SetCtrlValue(User, 'edm')
            helper.SetCtrlValue(PWD, 'Landmark1')
            helper.ClickOnce(Login)

        logger.info('登陆结束...')
        if self.isConnected():
            listener.sendStatus(self.conn, "登陆完毕")

if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    login = LoginManager(cxt)
    login.do()