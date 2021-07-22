# -*- coding: utf-8 -*-
import pyperclip
import helper

from loguru import logger
from launcher import *
from protocol import BarTab
from network import listener

class DataController:
    bar: BarTab = None
    cxt: Context = None
    err: bool = False
    errMsg: list = list()
    conn: WebSocket = None

    def __init__(self, cxt: Context, bar: BarTab, conn: WebSocket = None):
        self.cxt = cxt
        self.bar = bar
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def updateOperation(self, EDKResultVisualiser_1: auto.CustomControl):
        bar = self.bar
        if bar is None:
            return

        # 扭矩&摩阻
        if bar.HasField('torqueDrag'):
            torqueDrag = bar.torqueDrag
            opComboBox = None
            # 固定深度图形
            if torqueDrag.HasField('fixeds'):
                # 【管柱间隙】
                if int(torqueDrag.fixeds) == BarTab.TorqueDrag.FixedDepthPlots.fdpStringClearance:
                    # 更新相应的comboBox
                    opComboBox = EDKResultVisualiser_1.ComboBoxControl(searchDepth=1, ClassName='ComboBox',
                                                                       foundIndex=2)
            elif torqueDrag.HasField('roadmaps'): #路线图曲线
                #摩擦系数校正
                if int(torqueDrag.roadmaps) == BarTab.TorqueDrag.RoadmapPlots.rpFrictionCalibration:
                    # 更新相应的comboBox
                    opComboBox = EDKResultVisualiser_1.ComboBoxControl(searchDepth=1, ClassName='ComboBox',
                                                                       foundIndex=2)
            if opComboBox is not None:
                helper.ComboBoxCtrlRestore(opComboBox)
                helper.SetCtrlComboBoxValue(opComboBox, bar.extraData)

    def SpecilHandler(self) -> bool:
        bar = self.bar
        #扭矩&摩阻
        if bar is not None:
            isCopy = False
            if bar.HasField('torqueDrag'):
                torqueDrag = bar.torqueDrag
                #总结
                if torqueDrag.HasField('summary'):
                    #复合模型详情
                    if int(torqueDrag.summary) == BarTab.TorqueDrag.Summary.sHybridModelDetails:
                        DiscreteTDOutputDetailView = self.cxt.TopWindow.CustomControl(searchDepth=2,
                                                                                 ClassName='DiscreteTDOutputDetailView',
                                                                                 AutomationId='UserControl_1',
                                                                                 foundIndex=1)
                        isCopy = True
                        #作业
                        if bar.HasField('extraData'):
                            opComboBox = DiscreteTDOutputDetailView.ComboBoxControl(searchDepth=2, ClassName='ComboBox', AutomationId='ComboBox_1')
                            helper.ComboBoxCtrlRestore(opComboBox)
                            helper.SetCtrlComboBoxValue(opComboBox, bar.extraData)
                    elif int(torqueDrag.summary) == BarTab.TorqueDrag.Summary.sStringAnalysis: #管柱分析
                        isCopy = True
                # 载荷与应力数据 时需要特殊处理来取值
                if torqueDrag.HasField('loadStress'):
                    isCopy = True

                if isCopy:
                    #复制
                    EDKResultGrid_1 = self.cxt.TopWindow.DataGridControl(searchDepth=3, ClassName='EDKResultGrid', AutomationId='PlotControls:EDKResultGrid_1')
                    return helper.CopyDataGrid(EDKResultGrid_1)
        return False

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "获取计算结果")
        self.errMsg = list()
        self.err = False
        if self.SpecilHandler() is False:
            #普通的取值处理
            EDKResultVisualiser_1 = self.cxt.TopWindow.CustomControl(searchDepth=2, ClassName='EDKResultVisualizer',
                                                                     AutomationId='Controls1:EDKResultVisualiser_1',
                                                                     foundIndex=1)
            self.updateOperation(EDKResultVisualiser_1)

            # 判断计算结果
            EDKResultStatus = EDKResultVisualiser_1.CustomControl(searchDepth=1, AutomationId='PlotControls:PlotStatus_1',
                                                                  ClassName='EDKResultStatus')
            #正常的控件
            Normal = EDKResultStatus.TextControl(searchDepth=1, ClassName='TextBlock', Name='Normal')
            #错误时的锚点控件
            Error = EDKResultStatus.TextControl(searchDepth=1, ClassName='TextBlock', Name='无法计算。请解决以下问题：')

            logger.info('开始等待 {} 查询计算结果状态...', config.MINUTE * 3)
            count = 0
            while True:
                if auto.WaitForExist(Error, 1) or auto.WaitForExist(Normal, config.MINUTE):
                    break
                else:
                    count += 1
                helper.CheckStatus()
                logger.info('第 {} 次等待结束...', count)
                if count == 3:
                    self.cxt.LastErrorCode = errorcode.OUT_PUT_WND
                    self.cxt.cancel()
            logger.info('等待结束')

            if Normal.Exists(0, 0):
                # 复制按钮
                copy = EDKResultVisualiser_1.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='Button_1')

                # 转换为数据
                transfor = EDKResultVisualiser_1.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='FlipController')
                helper.AutoToggleStateClick(True, transfor)
                # 点击复制表格数据
                helper.ClickOnce(copy)

                # 复制单元格
                wd = self.cxt.TopWindow.WindowControl(searchDepth=1, ClassName='Window', AutomationId='WindowDialog_1',
                                                      Name='复制单元格')
                if helper.ExistCtrl(wd):
                    Yes = wd.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='yesButton', Name='是')
                    helper.ClickOnce(Yes)


            if Error.Exists(0, 0):
                # 错误时抓取错误信息
                while Error is not None:
                    if Error.ControlType != auto.ControlType.TextControl:
                        continue

                    errInfo = Error.Name
                    self.errMsg.append(errInfo)
                    # #超链接 详细错误信息
                    # link = Error.HyperlinkControl(searchDepth=1, CLassName='Hyperlink')
                    # if link.Exists(0, 0):
                    #     errDetailsInfo = link.Name
                    #     self.errMsg.append(errDetailsInfo)

                    Error = Error.GetNextSiblingControl()
                self.err = True

            if self.isConnected():
                listener.sendStatus(self.conn, "计算结果获取完毕")

    def isErr(self):
        return self.err

    def getErrMsg(self) -> list:
        return self.errMsg

    def get(self):
        return pyperclip.waitForPaste()


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    data = DataController(cxt)
    data.do()
