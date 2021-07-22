# -*- coding: utf-8 -*-

from protocol.wellplan_pb2 import NewCase
from network import listener
from launcher import *
from loginManager import *

import helper
import time

import wellplanOperatorTest as test

class ProjectManager:
    cxt: Context = None
    case: NewCase = None
    conn: WebSocket = None

    def __init__(self, cxt : Context, case : NewCase, conn: WebSocket = None):
        self.cxt = cxt
        self.case = case
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def do(self):
        logger.info('on_createProject')

        if self.isConnected():
            listener.sendStatus(self.conn, "初始化项目信息")

        saltText = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        WDialog = self.cxt.TopWindow.WindowControl(searchDepth=1, AutomationId='WindowDialog_1', ClassName='Window')
        helper.ExistCtrl(WDialog, config.MINUTE)

        Tab = WDialog.TabControl(searchDepth=1, AutomationId='TabControl_1', ClassName='TabControl')

        NewProject = Tab.TabItemControl(searchDepth=1, AutomationId='TabItem_2', ClassName='TabItem',
                                        name='创建新的文案')
        helper.ClickOnce(NewProject)

        NewProjectCase = NewProject.CustomControl(searchDepth=1, AutomationId='CreateNewCase:CreateNewCaseControl_1',
                                           ClassName='CreateNewCaseControl')

        CompanyCombo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='CompanyCombo', ClassName='AutoCompleteBox')
        helper.SetCtrlValue(CompanyCombo, self.case.Company + saltText)

        ProjectCombo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='ProjectCombo', ClassName='AutoCompleteBox')
        helper.SetCtrlValue(ProjectCombo, self.case.Project + saltText)

        SiteCombo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='SiteCombo', ClassName='AutoCompleteBox')
        helper.SetCtrlValue(SiteCombo, self.case.Site + saltText)

        WellCombo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='WellCombo', ClassName='AutoCompleteBox')
        helper.SetCtrlValue(WellCombo, self.case.Well + saltText)

        WellboreCombo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='WellboreCombo',
                                                ClassName='AutoCompleteBox')
        helper.SetCtrlValue(WellboreCombo, self.case.Wellbore + saltText)

        DesignCombo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='DesignCombo', ClassName='AutoCompleteBox')
        helper.SetCtrlValue(DesignCombo, self.case.Design + saltText)

        AnalysisName = NewProjectCase.EditControl(searchDepth=2, AutomationId='AnalysisName', ClassName='TextBox')
        helper.ClickOnce(AnalysisName)
        helper.SetCtrlValue(AnalysisName, self.case.Case + saltText)

        wpc = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='wpcontrols:AutoCompleteCombo_1',
                                      ClassName='AutoCompleteBox')
        helper.SetCtrlValue(wpc, self.case.Datum + saltText)

        UMS_Combo = NewProjectCase.ComboBoxControl(searchDepth=2, AutomationId='UMS_Combo', ClassName='ComboBox')
        helper.ComboBoxCtrlRestore(UMS_Combo)
        helper.SetCtrlComboBoxValue(UMS_Combo, self.case.units)

        ##############################################
        DatimCtl = NewProjectCase.CustomControl(searchDepth=1, AutomationId='CreateNewCase:DatumControl_1',
                                         ClassName='DatumControl')
        S1CheckBox = DatimCtl.CheckBoxControl(searchDepth=1, ClassName='CheckBox', Name='深海')
        helper.AutoToggleStateClick(self.case.enableOffshore, S1CheckBox)

            # if S1CheckBox.CurrentToggleState == auto.ToggleState.On:
        H1CheckBox = DatimCtl.CheckBoxControl(searchDepth=1, ClassName='CheckBox', Name='海底')
        helper.AutoToggleStateClick(self.case.enableSubsea, H1CheckBox)

        # 井头高度/井头深度
        wellhead = DatimCtl.EditControl(AutomationId='TextBox_2', ClassName='TextBox')
        wellheadVal = self.case.WellheadElevation
        if S1CheckBox.GetTogglePattern().ToggleState == auto.ToggleState.On:
            if H1CheckBox.GetTogglePattern().ToggleState == auto.ToggleState.On:
                wellheadVal = self.case.WellheadDepath
        helper.SetCtrlValue(wellhead, str(wellheadVal))

        # 坐标高度
        posHigh = DatimCtl.EditControl(AutomationId='Label_13', ClassName='TextBox')
        posHighVal = self.case.DatumElevation
        helper.SetCtrlValue(posHigh, str(posHighVal))

        ###如果深海选项被选中则会出现海水深度数值
        if S1CheckBox.GetTogglePattern().ToggleState == auto.ToggleState.On:
            # TextBox_1  海水深度
            seaDepth = DatimCtl.EditControl(AutomationId='TextBox_1', ClassName='TextBox')
            helper.SetCtrlValue(seaDepth, str(self.case.WaterDepth))
        else:
            # TextBox_1  大地表面标高
            earthFloorHigh = DatimCtl.EditControl(AutomationId='TextBox_1', ClassName='TextBox')
            helper.SetCtrlValue(earthFloorHigh, str(self.case.GroundElevation))

        # 点击创建
        createBtn = WDialog.ButtonControl(searchDepth=1, AutomationId='Button_3', ClassName='Button')
        helper.ClickOnce(createBtn)

        if self.isConnected():
            listener.sendStatus(self.conn, "项目信息初始化完毕")


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    # lg = LoginManager(cxt)
    # lg.do()

    case = pb2.NewCase()
    test.CreateCase(case)

    proManager = ProjectManager(cxt, case)
    proManager.do()

