# -*- coding: utf-8 -*-
import pyperclip
import config

import uiautomation as auto

import helper
from protocol.wellplan_pb2 import AnalysisSetting
from launcher import *
from network import listener

class AnalyzerController:
    cxt = None
    anaysisSetting = AnalysisSetting()
    conn: WebSocket = None

    def __init__(self, cxt, anaysisSetting: AnalysisSetting, conn: WebSocket = None):
        self.cxt = cxt
        self.anaysisSetting = anaysisSetting
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    # 处理通用
    def handleCommonAnalysis(self, CommonAnalysisGrp: auto.GroupControl,
                             common: AnalysisSetting.Common):
        if common.HasField('PumpRate'):
            # 泵排量
            FLOW_RATE = CommonAnalysisGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_WP_HYD_PARAMS_FLOW_RATE')
            helper.SetCtrlValue(FLOW_RATE, str(common.PumpRate))
        # 计算选项
        if common.HasField('SeaDensity'):
            calcGrp = CommonAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                     AutomationId='GroupBox_21', Name='计算选项')
            if calcGrp.Exists(0, 0):
                # 海水密度
                SEA_WATER_DENSITY = calcGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_CASE_CEM_JOB_DATA_SEA_WATER_DENSITY')
                # 若该编辑控件可以进行编辑
                if bool(SEA_WATER_DENSITY.IsEnabled):
                    helper.SetCtrlValue(SEA_WATER_DENSITY, str(common.SeaDensity))

        # 下入参数
        if common.HasField('runParam'):
            # 下入参数
            runGrp = CommonAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                    AutomationId='GroupBox_5', Name='下入参数')
            if helper.ExistCtrl(runGrp):
                # 起始深度
                START_MD = runGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                              AutomationId='HorizontalTextBox_WP_TDA_PARAMS_DRAG_START_MD')
                helper.SetCtrlValue(START_MD, str(common.runParam.StartMD))
                # 终止深度
                END_MD = runGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                            AutomationId='HorizontalTextBox_WP_TDA_PARAMS_DRAG_END_MD')
                helper.SetCtrlValue(END_MD, str(common.runParam.EndMD))
                # 步长
                DRAG_STEP = runGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                               AutomationId='HorizontalTextBox_WP_TDA_PARAMS_DRAG_STEP')
                helper.SetCtrlValue(DRAG_STEP, str(common.runParam.StepSize))

    def handleTorqueDragAnalysis(self, TorqueDragAnalysisGrp: auto.GroupControl,
                                 torqueDrag: AnalysisSetting.TorqueDrag):
        # 实际载荷值
        if len(torqueDrag.actuals) > 0:
            ActualBtn = TorqueDragAnalysisGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='Button_4')

        # 钩载/悬重校正
        if torqueDrag.HasField('hookload'):
            hookload = torqueDrag.hookload
            hookloadGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                             AutomationId='GroupBox_6',
                                                             Name='钩载/悬重校正')
            # 考虑切削摩擦校正
            correctionCheckbox = hookloadGrp.CheckBoxControl(searchDepth=1,
                                                             ClassName='CheckBox',
                                                             AutomationId='CheckBox_1',
                                                             Name='考虑切削摩擦校正')
            helper.AutoToggleStateClick(False, correctionCheckbox)

            if helper.ExistCtrl(hookloadGrp):
                # 游动滑车重量
                HOIST_EQUIP_WEIGHT = hookloadGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_TDA_OPTIONS_HOIST_EQUIP_WEIGHT')
                helper.SetCtrlValue(HOIST_EQUIP_WEIGHT, str(hookload.BlockWeight))
                # 考虑切削摩擦校正
                if hookload.HasField('correction'):
                    helper.AutoToggleStateClick(True, correctionCheckbox)
                    # 大绳道数
                    NO_OF_LINES = hookloadGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_WP_TDA_OPTIONS_NO_OF_LINES')
                    helper.SetCtrlValue(NO_OF_LINES, str(hookload.correction.LinesStrung))
                    # 机械效率
                    SHEAVE_EFFICIENCY = hookloadGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                AutomationId='HorizontalTextBox_WP_TDA_OPTIONS_SHEAVE_EFFICIENCY')
                    helper.SetCtrlValue(SHEAVE_EFFICIENCY, str(hookload.correction.MechanicalEfficiency))
        # 分析方法
        analyticalGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                           AutomationId='GroupBox_17',
                                                           Name='分析方法')
        if helper.ExistCtrl(analyticalGrp):
            # 考虑弯曲应力放大
            analyticalCheckbox = analyticalGrp.CheckBoxControl(searchDepth=1,
                                                               ClassName='CheckBox',
                                                               AutomationId='CheckBox_5',
                                                               Name='考虑弯曲应力放大')
            helper.AutoToggleStateClick(False, analyticalCheckbox)
            if torqueDrag.HasField('analytical'):
                analytical = torqueDrag.analytical
                helper.AutoToggleStateClick(analytical.UseBendingStressMagnification, analyticalCheckbox)

        # 管柱分析模型
        stringAnalysisGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                                   AutomationId='GroupBox_18',
                                                                   Name='管柱分析模型')

        if helper.ExistCtrl(stringAnalysisGrp):
            stiffStringCheckbox = stringAnalysisGrp.CheckBoxControl(searchDepth=1,
                                                                    ClassName='CheckBox',
                                                                    AutomationId='CheckBox_8',
                                                                    Name='使用刚性管柱模型')
            helper.AutoToggleStateClick(False, stiffStringCheckbox)

            viscousTorqueAndDragCheckbox = stringAnalysisGrp.CheckBoxControl(searchDepth=1,
                                                                             ClassName='CheckBox',
                                                                             AutomationId='CheckBox_10',
                                                                             Name='考虑粘滞扭矩和摩阻')
            helper.AutoToggleStateClick(False, viscousTorqueAndDragCheckbox)

            if torqueDrag.HasField('stringAnalysis'):
                stringAnalysis = torqueDrag.stringAnalysis
                # 使用刚性管柱模型
                helper.AutoToggleStateClick(stringAnalysis.UseStiffString, stiffStringCheckbox)
                # 考虑粘滞扭矩和摩阻
                helper.AutoToggleStateClick(stringAnalysis.UseViscousTorqueAndDrag, viscousTorqueAndDragCheckbox)

                # 屈曲极限系数
                RSRLSS_BLF = stringAnalysisGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_TDA_PARAMS_RSRLSS_BLF')
                helper.SetCtrlValue(RSRLSS_BLF, str(stringAnalysis.BucklingLimitFactor))

        # 最大上提拉力
        overpullGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                             AutomationId='GroupBox_7',
                                                             Name='最大上提拉力')
        if helper.ExistCtrl(overpullGrp):
            if torqueDrag.HasField('overpull'):
                overpull = torqueDrag.overpull
                # 使用屈服强度的
                YIELD_PERCENT_1 = overpullGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_WP_TDA_OPTIONS_YIELD_PERCENT_1')
                helper.SetCtrlValue(YIELD_PERCENT_1, str(overpull.UsingOfYield))

        # 液柱
        columnGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                           AutomationId='GroupBox_19',
                                                           Name='液柱')
        if helper.ExistCtrl(columnGrp):
            useColumnCheckbox = columnGrp.CheckBoxControl(searchDepth=1,
                                                              ClassName='CheckBox',
                                                              AutomationId='CheckBox_9',
                                                              Name='使用液柱梯度')
            helper.AutoToggleStateClick(False, useColumnCheckbox)
            if torqueDrag.HasField('column'):
                column = torqueDrag.column
                # 使用液柱梯度
                helper.AutoToggleStateClick(True, useColumnCheckbox)
                # 钻柱
                stringGrp = columnGrp.GroupControl(searchDepth=1, ClassName='Expander',
                                                   AutomationId='Expander_5',
                                                   Name='钻柱')
                HeaderSite = stringGrp.ButtonControl(searchDepth=1,
                                                     ClassName='Button',
                                                     AutomationId='HeaderSite')
                helper.AutoToggleStateClick(True, HeaderSite)
                # 地面压力
                if column.ss.HasField('SurfacePressure'):
                    SURFACE_PRESS = stringGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_WP_TDA_PARAMS_STRING_SURFACE_PRESS')
                    helper.SetCtrlValue(SURFACE_PRESS, str(column.ss.SurfacePressure))
                # 空气段长度
                GRAD_BOTTOM_MD = stringGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_WP_TDA_STRING_FLUID_GRAD_BOTTOM_MD')
                helper.SetCtrlValue(GRAD_BOTTOM_MD, str(column.ss.AirColumnLength))
                # 空气密度
                GRAD_MUD_WEIGHT = stringGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_STRING_FLUID_GRAD_MUD_WEIGHT')
                helper.SetCtrlValue(GRAD_MUD_WEIGHT, str(column.ss.AirDensity))

                DataGrid = stringGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                     AutomationId='StringFluidGradientsGrid')
                helper.ClearDataGrid(DataGrid)

                if len(column.ss.Items) > 0:
                    tableData = ''
                    for elem in column.ss.Items:
                        row = '{}		{}\r\n'.format(elem.ColumTopFromBottomOfString, elem.MudWeight)
                        tableData += row
                    helper.WriteDataToDataGrid(DataGrid, tableData)

                # ---------------------------------------------------------------------------
                # 环空
                annulusGrp = columnGrp.GroupControl(searchDepth=1, ClassName='Expander',
                                                    AutomationId='Expander_6',
                                                    Name='环空')
                HeaderSite = annulusGrp.ButtonControl(searchDepth=1,
                                                      ClassName='Button',
                                                      AutomationId='HeaderSite')
                helper.AutoToggleStateClick(True, HeaderSite)

                # 地面压力
                if column.aa.HasField('SurfacePressure'):
                    SURFACE_PRESS = annulusGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_TDA_PARAMS_ANNULAR_SURFACE_PRESS')
                    helper.SetCtrlValue(SURFACE_PRESS, str(column.aa.SurfacePressure))

                DataGrid = annulusGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                     AutomationId='AnnulusFluidGradientsGrid')
                helper.ClearDataGrid(DataGrid)
                if len(column.aa.Items) > 0:
                    tableData = ''
                    for elem in column.aa.Items:
                        row = '{}		{}\r\n'.format(elem.ColumTopFromBottomOfString, elem.MudWeight)
                        tableData += row
                    helper.WriteDataToDataGrid(DataGrid, tableData)

                # ----------------------------------------------------------------------
                # 内插管
                if column.HasField('ii'):
                    innerGrp = columnGrp.GroupControl(searchDepth=1, ClassName='Expander',
                                                        AutomationId='InnerStringExpander',
                                                        Name='内插管')
                    if helper.ExistCtrl(innerGrp):
                        HeaderSite = innerGrp.ButtonControl(searchDepth=1,
                                                              ClassName='Button',
                                                              AutomationId='HeaderSite')
                        helper.AutoToggleStateClick(True, HeaderSite)

                        DataGrid = innerGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                              AutomationId='InnerStringFluidGradientsGrid')
                        helper.ClearDataGrid(DataGrid)
                        if len(column.ii.Items) > 0:
                            tableData = ''
                            for elem in column.ii.Items:
                                row = '{}		{}\r\n'.format(elem.ColumTopFromBottomOfString, elem.MudWeight)
                                tableData += row
                            helper.WriteDataToDataGrid(DataGrid, tableData)


        # 管柱灌浆
        fillUpGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                       AutomationId='GroupBox_21',
                                                       Name='管柱灌浆')
        if helper.ExistCtrl(fillUpGrp):
            useColumnCheckbox = fillUpGrp.CheckBoxControl(searchDepth=1,
                                                              ClassName='CheckBox',
                                                              AutomationId='CheckBox_8')

            helper.AutoToggleStateClick(False, useColumnCheckbox)
            if torqueDrag.HasField('fillUp'):
                fillUp = torqueDrag.fillUp
                helper.AutoToggleStateClick(True, useColumnCheckbox)
                # 时长
                FILL_PERIOD = fillUpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_WP_TDA_PARAMS_CASING_FILL_PERIOD')
                helper.SetCtrlValue(FILL_PERIOD, str(fillUp.Period))

        # 井口详细参数
        columnGrp = TorqueDragAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                           AutomationId='GroupBox_20',
                                                           Name='井口详细参数')
        if helper.ExistCtrl(columnGrp):
            if torqueDrag.HasField('wellheadDetails'):
                wellheadDetails = torqueDrag.wellheadDetails
                # 指定侧向力
                specifySideForceRadioBtn = columnGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                        AutomationId='RadioButton_1')
                # 计算侧向力
                calcSideForceRadioBtn = columnGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                     AutomationId='RadioButton_2')
                if wellheadDetails.SpecifySideForce:
                    specifySideForceRadioBtn.SetFocus()
                    specifySideForceRadioBtn.SendKey(auto.Keys.VK_SPACE)
                    if wellheadDetails.HasField('specify'):
                        RSRLSS_SIDE_LOAD = columnGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_WELLHEADDETAILS_WP_TDA_PARAMS_RSRLSS_SIDE_LOAD')
                        helper.SetCtrlValue(RSRLSS_SIDE_LOAD, str(wellheadDetails.specify))
                else:
                    # 计算侧向力
                    calcSideForceRadioBtn.SetFocus()
                    calcSideForceRadioBtn.SendKey(auto.Keys.VK_SPACE)
                    # 井口偏移
                    if wellheadDetails.HasField('offsetFromWellhead'):
                        RSRLSS_OFFSET_WH = columnGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_WELLHEADDETAILS_WP_TDA_PARAMS_RSRLSS_OFFSET_WH')
                        helper.SetCtrlValue(RSRLSS_OFFSET_WH, str(wellheadDetails.offsetFromWellhead))
                    # 井口角度
                    if wellheadDetails.HasField('angleAtWellhead'):
                        RSRLSS_ANGLE_WH = columnGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                AutomationId='HorizontalTextBox_WELLHEADDETAILS_WP_TDA_PARAMS_RSRLSS_ANGLE_WH')
                        helper.SetCtrlValue(RSRLSS_ANGLE_WH, str(wellheadDetails.angleAtWellhead))

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化分析设置信息")

        AnalysisTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock',
                                                     AutomationId='AnalysisTab')
        helper.ClickOnce(AnalysisTab)
        AnalysisSettingsEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                      ClassName='AnalysisSettingsEditorView',
                                                                      AutomationId='StackPanel_1')
        # 扭矩 & 摩阻
        if self.anaysisSetting.HasField('torqueDrag'):
            TorqueDragAnalysis = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                          ClassName='TorqueDragAnalysis',
                                                                          AutomationId='UserControl_1')
            TorqueDragAnalysisGrp = TorqueDragAnalysis.GroupControl(searchDepth=1, ClassName='Expander',
                                                                    AutomationId='TorqueAndDragAnalysisSettingsExpander')
            HeaderSite = TorqueDragAnalysisGrp.ButtonControl(searchDepth=1,
                                                             ClassName='Button',
                                                             AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, HeaderSite)
            self.handleTorqueDragAnalysis(TorqueDragAnalysisGrp, self.anaysisSetting.torqueDrag)

        # 通用分析
        if self.anaysisSetting.HasField('common'):
            CommonAnalysis = AnalysisSettingsEditorView.CustomControl(searchDepth=2, ClassName='CommonAnalysis',
                                                                      AutomationId='UserControl_1')
            CommonAnalysisGrp = CommonAnalysis.GroupControl(searchDepth=1, ClassName='Expander',
                                                            AutomationId='CommonAnalysisSettingsExpander')
            HeaderSite = CommonAnalysisGrp.ButtonControl(searchDepth=1,
                                                         ClassName='Button',
                                                         AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, HeaderSite)
            self.handleCommonAnalysis(CommonAnalysisGrp, self.anaysisSetting.common)

        '''
        #注水泥
        CementingAnalysisSettingsView = AnalysisSettingsEditorView.CustomControl(searchDepth=2, ClassName='CementingAnalysisSettingsView')

        #扶正计算
        CentralizerOptimizationView = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                  ClassName='CentralizerOptimizationView',
                                                                  AutomationId='UserControl_1')
        #水力参数
        HydraulicsAnalysis = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                  ClassName='HydraulicsAnalysis',
                                                                  AutomationId='UserControl_1')
        #抽吸 & 波动
        SwabSurgeAnalysisSettingsView = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                  ClassName='SwabSurgeAnalysisSettingsView')
        #欠平衡水力
        UnderbalanceAnalysisSettingsView = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                          ClassName='UnderbalanceAnalysisSettingsView')
        #井控
        WellControlAnalysisSettingsView = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                                  ClassName='WellControlAnalysisSettingsView')
        #BHA 动态
        CriticalSpeedAnalysisSettingsView = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                  ClassName='CriticalSpeedAnalysisSettingsView')
        #卡钻分析
        StuckPipeAnalysisSettingsView = AnalysisSettingsEditorView.CustomControl(searchDepth=2,
                                                                  ClassName='StuckPipeAnalysisSettingsView')
        '''
        if self.isConnected():
            listener.sendStatus(self.conn, "分析设置信息初始化完毕")
