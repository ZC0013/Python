# -*- coding: utf-8 -*-
from protocol.wellplan_pb2 import RigEquipment
from launcher import *
from network import listener
import helper

class RigController:
    cxt = Context()
    rigEquipment = RigEquipment()
    conn: WebSocket = None

    def __init__(self, cxt : Context, rigEquipment : RigEquipment, conn: WebSocket = None):
        self.cxt = cxt
        self.rigEquipment = rigEquipment
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def mechanicalLimits(self, RigEquipmentEditorView : auto.CustomControl, rigEquipment : RigEquipment):
        # 机械极限
        MechanicalLimits = RigEquipmentEditorView.CustomControl(searchDepth=2, ClassName='MechanicalLimits',
                                                                AutomationId='UserControl_1')

        # 游动滑车等级
        BlockRatingCheckbo = MechanicalLimits.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                              AutomationId='CheckBox_1')
        helper.AutoToggleStateClick(False, BlockRatingCheckbo)
        # 扭矩
        TorqueRatingCheckbo = MechanicalLimits.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                               AutomationId='CheckBox_2')
        helper.AutoToggleStateClick(False, TorqueRatingCheckbo)

        if not rigEquipment.HasField('mechanicalLimits'):
            return

        mechanicalLimits = rigEquipment.mechanicalLimits
        helper.AutoToggleStateClick(mechanicalLimits.EnableBlockRating, BlockRatingCheckbo)
        if mechanicalLimits.EnableBlockRating:
            RIG_CAPACITY = MechanicalLimits.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_CD_CASE_RIG_CAPACITY')
            helper.SetCtrlValue(RIG_CAPACITY, str(mechanicalLimits.BlockRating))

        helper.AutoToggleStateClick(mechanicalLimits.EnableTorqueRating, TorqueRatingCheckbo)
        if mechanicalLimits.EnableTorqueRating:
            TORQUE_RATING = MechanicalLimits.EditControl(searchDepth=1, ClassName='TextBox',
                                                         AutomationId='HorizontalTextBox_WP_TDA_OPTIONS_TORQUE_RATING')
            helper.SetCtrlValue(TORQUE_RATING,str(mechanicalLimits.TorqueRating))

    def circulatingSystemControl(self, RigEquipmentEditorView : auto.CustomControl, rigEquipment : RigEquipment):
        # 循环系统
        CirculatingSystemControl = RigEquipmentEditorView.CustomControl(searchDepth=2,
                                                                        ClassName='CirculatingSystemControl',
                                                                        AutomationId='UserControl_2')
        # 循环系统 -- 评估工作压力
        WORKING_PRESS = CirculatingSystemControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_CASE_CIRC_SYSTEM_MAX_WORKING_PRESS')
        helper.ClearCtrlValue(WORKING_PRESS)
        # 循环系统 -- 防喷器压力等级
        PRESS_RATING = CirculatingSystemControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                            AutomationId='HorizontalTextBox_WP_KILL_SHEET_GEN_BOP_PRESS_RATING')
        helper.ClearCtrlValue(PRESS_RATING)

        # 循环系统 -- 地表压力流失
        SurfacePressureLossGrp = CirculatingSystemControl.GroupControl(searchDepth=1, ClassName='Expander',
                                                                       AutomationId='SurfacePressureLossExpander')
        SurfacePressureLossBtn = SurfacePressureLossGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                      AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, SurfacePressureLossBtn)

        # 循环系统 -- 地表压力流失 -- 自定义
        CustomRadio = SurfacePressureLossGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                AutomationId='RadioButton_1')
        helper.ClickOnce(CustomRadio)
        PRESSURE_DROP = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_PRESSURE_DROP')
        helper.SetCtrlValue(PRESSURE_DROP, "0.00")

        if not rigEquipment.HasField('circulatingSystem'):
            return

        circulatingSystem = rigEquipment.circulatingSystem

        if circulatingSystem.HasField('RatedWorkingPressure'):
            helper.SetCtrlValue(WORKING_PRESS,str(circulatingSystem.RatedWorkingPressure))

        if circulatingSystem.HasField('BOPPressureRating'):
            helper.SetCtrlValue(PRESS_RATING,str(circulatingSystem.BOPPressureRating))

        surfacePressureLoss_Specify = circulatingSystem.surfacePressureLoss_Specify

        # 循环系统 -- 地表压力流失
        if surfacePressureLoss_Specify.enableSpecify:
            helper.ClickOnce(CustomRadio)
            if surfacePressureLoss_Specify.HasField('specify'):
                helper.SetCtrlValue(PRESSURE_DROP,str(surfacePressureLoss_Specify.specify))
        else:
            CalRadio = SurfacePressureLossGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                           AutomationId='RadioButton_2')
            helper.ClickOnce(CalRadio)

            if surfacePressureLoss_Specify.HasField('calculateType'):
                CalTypeCombo = SurfacePressureLossGrp.ComboBoxControl(searchDepth=1, AutomationId='ComboBox_1',
                                                                ClassName='ComboBox')
                helper.ComboBoxCtrlRestore(CalTypeCombo)
                helper.SetCtrlComboBoxValue(CalTypeCombo, surfacePressureLoss_Specify.calculateType)

                # 立管
                # checkbox
                checkboxStandpipe = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                           AutomationId='CheckBox_1')
                if bool(checkboxStandpipe.IsEnabled):
                    helper.AutoToggleStateClick(False, checkboxStandpipe)

                # 软管
                # checkbox
                checkboxHOSE = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                      AutomationId='CheckBox_2')
                if bool(checkboxHOSE.IsEnabled):
                    helper.AutoToggleStateClick(False, checkboxHOSE)
                # 水龙头
                # checkbox
                checkboxSwivel = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                        AutomationId='CheckBox_3')
                if bool(checkboxSwivel.IsEnabled):
                    helper.AutoToggleStateClick(False, checkboxSwivel)
                # 方管柱
                # checkbox
                checkboxKelly = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                       AutomationId='CheckBox_4')
                if bool(checkboxKelly.IsEnabled):
                    helper.AutoToggleStateClick(False, checkboxKelly)
                # 泵排放线路
                # checkbox
                checkboxPumpDischargeLine = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                                   AutomationId='CheckBox_7')
                if bool(checkboxPumpDischargeLine.IsEnabled):
                    helper.AutoToggleStateClick(False, checkboxPumpDischargeLine)
                # 驱动叠加顶
                # checkbox
                checkboxTopDriveStackup = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1,
                                                                                 ClassName='CheckBox',
                                                                                 AutomationId='CheckBox_6')
                if bool(checkboxTopDriveStackup.IsEnabled):
                    helper.AutoToggleStateClick(False, checkboxTopDriveStackup)

                if surfacePressureLoss_Specify.calculateType == surfacePressureLoss_Specify.CalculateType.Custom_Rotary:
                    if bool(checkboxStandpipe.IsEnabled):
                        helper.AutoToggleStateClick(surfacePressureLoss_Specify.customRotary.enableStandpipe, checkboxStandpipe)

                    if bool(checkboxStandpipe.IsEnabled) and surfacePressureLoss_Specify.customRotary.enableStandpipe:
                        # 长度
                        STAND_PIPE_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_WP_CASE_SURFACE_STAND_PIPE_LENGTH')
                        helper.SetCtrlValue(STAND_PIPE_LENGTH,str(surfacePressureLoss_Specify.customRotary.standpipeLength))
                        # 内径
                        STAND_PIPE_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_STAND_PIPE_ID')
                        helper.SetCtrlValue(STAND_PIPE_ID,str(surfacePressureLoss_Specify.customRotary.standpipeID))
                    #初始化
                    if bool(checkboxHOSE.IsEnabled):
                        helper.AutoToggleStateClick(surfacePressureLoss_Specify.customRotary.enableHose, checkboxHOSE)

                    if bool(checkboxHOSE.IsEnabled) and surfacePressureLoss_Specify.customRotary.enableHose:
                        # 长度
                        HOSE_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                         AutomationId='HorizontalTextBox_WP_CASE_SURFACE_HOSE_LENGTH')
                        helper.SetCtrlValue(HOSE_LENGTH,str(surfacePressureLoss_Specify.customRotary.hoseLength))
                        # 内径
                        HOSE_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_CASE_SURFACE_HOSE_ID')
                        helper.SetCtrlValue(HOSE_ID,str(surfacePressureLoss_Specify.customRotary.hoseID))
                    # 初始化
                    if bool(checkboxSwivel.IsEnabled):
                        helper.AutoToggleStateClick(surfacePressureLoss_Specify.customRotary.enableSwivel, checkboxSwivel)

                    if bool(checkboxSwivel.IsEnabled) and not surfacePressureLoss_Specify.customRotary.enableTopDriveStackup and surfacePressureLoss_Specify.customRotary.enableSwivel:
                        # 长度
                        SWIVEL_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_SWIVEL_LENGTH')
                        helper.SetCtrlValue(SWIVEL_LENGTH,str(surfacePressureLoss_Specify.customRotary.swivelLength))
                        # 内径
                        SWIVEL_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_CASE_SURFACE_SWIVEL_ID')
                        helper.SetCtrlValue(SWIVEL_ID,str(surfacePressureLoss_Specify.customRotary.swivelID))

                    # 初始化
                    if bool(checkboxKelly.IsEnabled):
                        helper.AutoToggleStateClick(surfacePressureLoss_Specify.customRotary.enableKelly, checkboxKelly)

                    if bool(checkboxKelly.IsEnabled) and not surfacePressureLoss_Specify.customRotary.enableTopDriveStackup and surfacePressureLoss_Specify.customRotary.enableKelly:
                        # 长度
                        KELLY_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_WP_CASE_SURFACE_KELLY_LENGTH')
                        helper.SetCtrlValue(KELLY_LENGTH,str(surfacePressureLoss_Specify.customRotary.kellyLength))
                        # 内径
                        KELLY_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                      AutomationId='HorizontalTextBox_WP_CASE_SURFACE_KELLY_ID')
                        helper.SetCtrlValue(KELLY_ID,str(surfacePressureLoss_Specify.customRotary.kellyID))

                    # 初始化
                    if bool(checkboxPumpDischargeLine.IsEnabled):
                        helper.AutoToggleStateClick(surfacePressureLoss_Specify.customRotary.enablePumpDischargeLine, checkboxPumpDischargeLine)
                    if bool(checkboxPumpDischargeLine.IsEnabled) and surfacePressureLoss_Specify.customRotary.enablePumpDischargeLine:
                        # 长度
                        RUN_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                        AutomationId='HorizontalTextBox_WP_CASE_SURFACE_RUN_LENGTH')
                        helper.SetCtrlValue(RUN_LENGTH,str(surfacePressureLoss_Specify.customRotary.pupmDischargeLineLength))
                        # 内径
                        RUN_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_WP_CASE_SURFACE_RUN_ID')
                        helper.SetCtrlValue(RUN_ID,str(surfacePressureLoss_Specify.customRotary.pupmDischargeLineID))

                    # 初始化
                    if bool(checkboxTopDriveStackup.IsEnabled):
                        helper.AutoToggleStateClick(surfacePressureLoss_Specify.customRotary.enableTopDriveStackup, checkboxTopDriveStackup)

                    if bool(checkboxTopDriveStackup.IsEnabled) and surfacePressureLoss_Specify.customRotary.enableTopDriveStackup:
                        # 长度
                        STACK_HEIGHT = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_WP_CASE_SURFACE_TOP_STACK_HEIGHT')
                        helper.SetCtrlValue(STACK_HEIGHT,str(surfacePressureLoss_Specify.customRotary.topDriveStackupLength))
                        # 内径
                        HEIGHT_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_CASE_SURFACE_STACK_HEIGHT_ID')
                        helper.SetCtrlValue(HEIGHT_ID,str(surfacePressureLoss_Specify.customRotary.topDriveStackupID))
                elif surfacePressureLoss_Specify.calculateType == surfacePressureLoss_Specify.CalculateType.Coiled_Tubing and surfacePressureLoss_Specify.HasField('coiledTubing'):
                    coiledTubing = surfacePressureLoss_Specify.coiledTubing

                    # 泵排放线路
                    PumpDischargeLineCheckBo = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1,
                                                                                      ClassName='CheckBox',
                                                                                      AutomationId='CheckBox_8')
                    helper.AutoToggleStateClick(coiledTubing.PumpDischargeLine, PumpDischargeLineCheckBo)
                    if coiledTubing.PumpDischargeLine:
                        #长度
                        if coiledTubing.HasField('PumpDischargeLineLength'):
                            RUN_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox', foundIndex=2,
                                                                            AutomationId='HorizontalTextBox_WP_CASE_SURFACE_RUN_LENGTH')
                            helper.SetCtrlValue(RUN_LENGTH,str(coiledTubing.PumpDischargeLineLength))
                        #内径
                        if coiledTubing.HasField('PumpDischargeLineID'):
                            RUN_ID = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox', foundIndex=2,
                                                                        AutomationId='HorizontalTextBox_WP_CASE_SURFACE_RUN_ID')
                            helper.SetCtrlValue(RUN_ID,str(coiledTubing.PumpDischargeLineID))

                    #CoiledTubingWrapType
                    #默认为 Inline
                    CoiledTubingWrapTypeCheckBo = SurfacePressureLossGrp.ComboBoxControl(searchDepth=1,
                                                                                         ClassName='ComboBox',
                                                                                         AutomationId='ComboBox_2')
                    helper.ComboBoxCtrlRestore(CoiledTubingWrapTypeCheckBo)
                    #柔性软管类型
                    if coiledTubing.type == RigEquipment.CirculatingSystem.SurfacePressureLoss_Specify.CoiledTubing.CoiledTubingWrapType.Offset:
                        helper.SetCtrlComboBoxValue(CoiledTubingWrapTypeCheckBo,  1)

                    #卷筒外径
                    if coiledTubing.HasField('ReelOD'):
                        REEL_DIAMETER = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_WP_CASE_SURFACE_REEL_DIAMETER')
                        helper.SetCtrlValue(REEL_DIAMETER,str(coiledTubing.ReelOD))

                    # 取心外径
                    if coiledTubing.HasField('CoreOD'):
                        CORE_DIAMETER = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_CORE_DIAMETER')
                        helper.SetCtrlValue(CORE_DIAMETER,str(coiledTubing.CoreOD))

                    # 卷筒宽度
                    if coiledTubing.HasField('ReelWrapWidth'):
                        INSIDE_WIDTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_INSIDE_WIDTH')
                        helper.SetCtrlValue(INSIDE_WIDTH,str(coiledTubing.ReelWrapWidth))

                    # 剩余的柔性软管的长度
                    if coiledTubing.HasField('RemainingCTLength'):
                        REEL_LENGTH = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_WP_CASE_SURFACE_REEL_LENGTH')
                        helper.SetCtrlValue(REEL_LENGTH,str(coiledTubing.RemainingCTLength))

                    # 注入器/叠加器高度
                    if coiledTubing.HasField('Injector_StackupHeight'):
                        INJ_STACK_HEIGHT = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                         AutomationId='HorizontalTextBox_WP_CASE_SURFACE_INJ_STACK_HEIGHT')
                        helper.SetCtrlValue(INJ_STACK_HEIGHT,str(coiledTubing.Injector_StackupHeight))

                    #控制管缆
                    UmbilicalCheckbo = SurfacePressureLossGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                           AutomationId='CheckBox_9')
                    helper.AutoToggleStateClick(surfacePressureLoss_Specify.coiledTubing.Umbilical, UmbilicalCheckbo)
                    if surfacePressureLoss_Specify.coiledTubing.Umbilical:
                        if coiledTubing.HasField('Umbilical_OD'):
                            UMBILICAL_OD = SurfacePressureLossGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                         AutomationId='HorizontalTextBox_WP_CASE_SURFACE_UMBILICAL_OD')
                            helper.SetCtrlValue(UMBILICAL_OD,str(coiledTubing.Umbilical_OD))

        #循环系统 -- 泥浆池
        MudPitGrp = CirculatingSystemControl.GroupControl(searchDepth=1, ClassName='Expander',
                                                                       AutomationId='MudPitExpander')
        MudPitBtn = MudPitGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                      AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, MudPitBtn)
        # 使用平均注入温度
        AvgTempRadio = MudPitGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                    AutomationId='RadioButton_5')
        helper.ClickOnce(AvgTempRadio)

        if circulatingSystem.HasField('mudPit_UseAverageInletTemperature'):
            mudPit_UseAverageInletTemperature = circulatingSystem.mudPit_UseAverageInletTemperature
            if mudPit_UseAverageInletTemperature.enableUseAverageInletTemperature:
                helper.ClickOnce(AvgTempRadio)
                if mudPit_UseAverageInletTemperature.HasField('UseAverageInletTemperature'):
                    MUD_INLET_TEMP = MudPitGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_CASE_SURFACE_MUD_INLET_TEMP')
                    helper.SetCtrlValue(MUD_INLET_TEMP,str(mudPit_UseAverageInletTemperature.UseAverageInletTemperature))
            else:
                MudPitToCalRadio = MudPitGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                            AutomationId='RadioButton_6')
                helper.ClickOnce(MudPitToCalRadio)
                #泥浆搅拌器马力（每罐）
                if mudPit_UseAverageInletTemperature.HasField('MudStirrerPower_PerTank'):
                    AGITATOR_POWER = MudPitGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_PIT_AGITATOR_POWER')
                    helper.SetCtrlValue(AGITATOR_POWER,str(mudPit_UseAverageInletTemperature.MudStirrerPower_PerTank))
                #地表泥浆体积
                if mudPit_UseAverageInletTemperature.HasField('SurfaceMudVolume'):
                    SURFACE_VOL_MUD = MudPitGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_CASE_SURFACE_SURFACE_VOL_MUD')
                    helper.SetCtrlValue(SURFACE_VOL_MUD,str(mudPit_UseAverageInletTemperature.SurfaceMudVolume))
                #泥浆池地表环境
                if mudPit_UseAverageInletTemperature.HasField('environment'):
                    environment = mudPit_UseAverageInletTemperature.environment
                    EnvGrp = MudPitGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                                            AutomationId='GroupBox_2')
                    #空气温度
                    if environment.HasField('AirTemperature'):
                        AIR_TEMPERATURE = MudPitGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                AutomationId='HorizontalTextBox_WP_CASE_SURFACE_AIR_TEMPERATURE')
                        helper.SetCtrlValue(AIR_TEMPERATURE,str(environment.AirTemperature))
                    #风速
                    if environment.HasField('WindSpeed'):
                        WIND_SPEED = MudPitGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_CASE_SURFACE_WIND_SPEED')
                        helper.SetCtrlValue(WIND_SPEED,str(environment.WindSpeed))
                    #最初泥浆池温度
                    if environment.HasField('InitialMudPitTemperature'):
                        INITIAL_PIT_TEMP = MudPitGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_CASE_SURFACE_INITIAL_PIT_TEMP')
                        helper.SetCtrlValue(INITIAL_PIT_TEMP,str(environment.InitialMudPitTemperature))

        #循环系统 -- 节流/压井管汇
        if circulatingSystem.HasField('chokeKillLine'):
            ChokeKillLineView = CirculatingSystemControl.CustomControl(searchDepth=1, ClassName='ChokeKillLineView')
            ChokeKillLineGrp = ChokeKillLineView.GroupControl(searchDepth=1, ClassName='Expander',
                                                              AutomationId='ChokeKillLineExpander')
            ChokeKillLineHeaderSiteBtn = ChokeKillLineGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                        AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, ChokeKillLineHeaderSiteBtn)
            chokeKillLine = circulatingSystem.chokeKillLine
            #指定压耗
            SpecifyPressureLossCheckbo = ChokeKillLineGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                          foundIndex=1)
            helper.AutoToggleStateClick(False, SpecifyPressureLossCheckbo)

            if chokeKillLine.HasField('SpecifyPressureLoss'):
                helper.AutoToggleStateClick(True, SpecifyPressureLossCheckbo)
                PRESSURE_LOSS = ChokeKillLineGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                  AutomationId='HorizontalTextBox_WP_WCN_PARAMS_PRESSURE_LOSS')
                helper.SetCtrlValue(PRESSURE_LOSS,str(chokeKillLine.SpecifyPressureLoss))
            #节流/压并管汇尺寸
            if chokeKillLine.HasField('DimensionsChokeline'):
                DimensionsChokeline = chokeKillLine.DimensionsChokeline
                #管汇长度
                CHOKE_LINE_LENGTH = ChokeKillLineGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_WCN_PARAMS_CHOKE_LINE_LENGTH')
                helper.SetCtrlValue(CHOKE_LINE_LENGTH,str(DimensionsChokeline.LineLength))
                #节流管汇内径
                CHOKE_LINE_ID = ChokeKillLineGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_WCN_PARAMS_CHOKE_LINE_ID')
                helper.SetCtrlValue(CHOKE_LINE_ID,str(DimensionsChokeline.ChokeLineID))

            #压井管汇
            ChokeModeCheckBox = ChokeKillLineGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                          AutomationId='ChokeModeCheckBox')
            helper.AutoToggleStateClick(False, ChokeModeCheckBox)
            if chokeKillLine.HasField('KillLineID'):
                helper.AutoToggleStateClick(True, ChokeModeCheckBox)
                #压井管汇内径
                KILL_LINE_ID = ChokeKillLineGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_WCN_PARAMS_KILL_LINE_ID')
                helper.SetCtrlValue(KILL_LINE_ID,str(chokeKillLine.KillLineID))

        # 循环系统 -- 地表返回线

        if circulatingSystem.HasField('returnSurfaceLine'):
            ReturnSurfaceLineGrp = CirculatingSystemControl.GroupControl(searchDepth=1, ClassName='Expander',
                                                                         AutomationId='ReturnSurfaceLineExpander')
            ReturnSurfaceLineBtn = ReturnSurfaceLineGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                      AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, ReturnSurfaceLineBtn)
            returnSurfaceLine = circulatingSystem.returnSurfaceLine
            # 管线内径
            if returnSurfaceLine.HasField('LineID'):
                INNER_DIAMETER = ReturnSurfaceLineGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_CASE_BLOOIE_LINE_INNER_DIAMETER')
                helper.SetCtrlValue(INNER_DIAMETER,str(returnSurfaceLine.LineID))
            # 管线长度
            if returnSurfaceLine.HasField('LineLength'):
                LINE_LENGTH = ReturnSurfaceLineGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                  AutomationId='HorizontalTextBox_CD_CASE_BLOOIE_LINE_LENGTH')
                helper.SetCtrlValue(LINE_LENGTH,str(returnSurfaceLine.LineLength))

        self.mudPumps(CirculatingSystemControl, self.rigEquipment)

    def mudPumps(self, CirculatingSystemControl : auto.CustomControl, rigEquipment : RigEquipment):
        MudPumpsControl = CirculatingSystemControl.CustomControl(searchDepth=1,
                                                               ClassName='MudPumpsControl',
                                                               AutomationId='UserControl_3')
        #进行清空
        while True:
            MudPumpsContainer = MudPumpsControl.CustomControl(foundIndex=1, searchDepth=1,
                                                              ClassName='MudPumpContainer',
                                                              AutomationId='UserControl_1')
            if helper.ExistCtrl(MudPumpsContainer) is False:
                break

            MudPumpGrp = MudPumpsContainer.GroupControl(searchDepth=2, ClassName='Expander')
            HeaderSiteBtn = MudPumpGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, HeaderSiteBtn)

            DeleteMudPumpButton = HeaderSiteBtn = MudPumpGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='DeleteMudPumpButton')
            helper.ClickOnce(DeleteMudPumpButton)

        if not rigEquipment.HasField('circulatingSystem'):
            return

        # 泥浆泵
        if len(rigEquipment.circulatingSystem.mudPumps) <= 0:
            return

        mudPumps = rigEquipment.circulatingSystem.mudPumps
        #
        AddMudPumpButton = MudPumpsControl.ButtonControl(searchDepth=1, ClassName='Button',
                                                         AutomationId='AddMudPumpButton')
        idx = 1
        for elem in mudPumps:
            if not isinstance(elem, RigEquipment.CirculatingSystem.MudPumps):
                return
            helper.ClickOnce(AddMudPumpButton)

            MudPumpsContainer = MudPumpsControl.CustomControl(foundIndex=idx, searchDepth=1,
                                                                ClassName='MudPumpContainer',
                                                                AutomationId='UserControl_1')
            MudPumpGrp = MudPumpsContainer.GroupControl(searchDepth=2, ClassName='Expander')
            HeaderSiteBtn = MudPumpGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, HeaderSiteBtn)

            # 泵名称
            if elem.HasField('pumpName'):
                PUMP_NO = MudPumpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_MUDPUMPITEM_WP_CASE_PUMP_PUMP_NO')
                helper.SetCtrlValue(PUMP_NO,str(elem.pumpName))
            # 每冲程体积
            if elem.HasField('VolumePerStroke'):
                VOLUME_PER_STROKE = MudPumpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                               AutomationId='HorizontalTextBox_MUDPUMPITEM_WP_CASE_PUMP_VOLUME_PER_STROKE')
                helper.SetCtrlValue(VOLUME_PER_STROKE,str(elem.VolumePerStroke))
            # 最大速度
            if elem.HasField('MaximumSpeed'):
                MAX_SPEED = MudPumpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_MUDPUMPITEM_WP_CASE_PUMP_MAX_SPEED')
                helper.SetCtrlValue(MAX_SPEED,str(elem.MaximumSpeed))
            # 最大排放压力
            if elem.HasField('MaxDischargePressure'):
                MAX_DISCHARGE_PRESS = MudPumpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_MUDPUMPITEM_WP_CASE_PUMP_MAX_DISCHARGE_PRESS')
                helper.SetCtrlValue(MAX_DISCHARGE_PRESS,str(elem.MaxDischargePressure))
            # 马力
            if elem.HasField('HorsepowerRating'):
                HP_RATING = MudPumpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_MUDPUMPITEM_WP_CASE_PUMP_HP_RATING')
                helper.SetCtrlValue(HP_RATING,str(elem.HorsepowerRating))
            # 容积效率
            if elem.HasField('VolumetricEfficiency'):
                MUD_PUMP_EFFICIENCY = MudPumpGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_MUDPUMPITEM_WP_CASE_PUMP_MUD_PUMP_EFFICIENCY')
                helper.SetCtrlValue(MUD_PUMP_EFFICIENCY,str(elem.VolumetricEfficiency))
            idx += 1

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化钻井平台信息")
        RigEquipmentTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock',
                                                         AutomationId='RigEquipmentTab')
        helper.ClickOnce(RigEquipmentTab)
        RigEquipmentEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                           ClassName='RigEquipmentEditorView',
                                                                           AutomationId='StackPanel_1')
        self.mechanicalLimits(RigEquipmentEditorView, self.rigEquipment)
        self.circulatingSystemControl(RigEquipmentEditorView, self.rigEquipment)
        if self.isConnected():
            listener.sendStatus(self.conn, "钻井平台信息初始化完毕")