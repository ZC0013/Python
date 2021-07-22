# -*- coding: utf-8 -*-
import helper

from protocol.wellplan_pb2 import OperationalParameters
from launcher import *
from context import *
from network import listener

class WorkerController:
    cxt = Context()
    operationParam = OperationalParameters()
    conn: WebSocket = None

    def __init__(self, cxt: Context, operationParam: OperationalParameters, conn: WebSocket = None):
        self.cxt = cxt
        self.operationParam = operationParam
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    # 验证是否支持 扭矩与摩阻标准分析
    def validTorqueAndDragNormalAnalysis(self) -> bool:
        return True

    # 验证是否支持 扭矩与摩阻自上而下分析
    def validTorqueAndDragTopDownAnalysis(self) -> bool:
        return True

    # 验证是否支持 扭矩与摩阻混合模型
    def validTorqueAndDragDiscreteModel(self) -> bool:
        return True

    # 验证是否支持 抽吸 & 波动
    def validSwabAndSurgeOperations(self) -> bool:
        return True

    # 验证是否支持 井控压井施工单
    def validWellControlOperations(self) -> bool:
        return True

    #验证是否支持 注水泥
    def vaildCementingOperations(self) -> bool:
        return True

    #验证是否支持 BHA 动态
    def validCriticalSpeedOperations(self) -> bool:
        return True

    #验证是否支持 卡钻分析
    def validStuckPipeOperations(self) -> bool:
        return True

    #处理 扭矩与摩阻标准分析
    def handleTorqueAndDragNormalAnalysis(self,
                                          TorqueAndDragNormalAnalysisGrp : auto.GroupControl,
                                          operationParam : OperationalParameters):
        if not operationParam.HasField('tdNormalAnalysis'):
            return

        tdNormalAnalysis = operationParam.tdNormalAnalysis
        tdGrp = TorqueAndDragNormalAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox')
        if not tdGrp.Exists(0, 0):
            return

        while tdGrp != None:
            if tdGrp.ControlType != auto.ControlType.GroupControl:
                tdGrp = tdGrp.GetNextSiblingControl()
                continue

            tdCheckBox = tdGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox', AutomationId='CheckBox_8')
            if helper.ExistCtrl(tdCheckBox) and bool(tdCheckBox.IsEnabled):
                if tdCheckBox.Name == '下钻' and tdNormalAnalysis.HasField('trippingIn') and tdNormalAnalysis.enableTrippingIn:
                    trippingIn = tdNormalAnalysis.trippingIn
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    #速度
                    TRIP_SPEED = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                AutomationId='HorizontalTextBox_WP_TDA_PARAMS_TRIP_IN_TRIP_SPEED')
                    helper.SetCtrlValue(TRIP_SPEED,str(trippingIn.Speed))
                    #转盘转速
                    ROTATION_SPEED = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_PARAMS_TRIP_IN_ROTATION_SPEED')
                    helper.SetCtrlValue(ROTATION_SPEED,str(trippingIn.RPM))
                elif tdCheckBox.Name == '起钻' and tdNormalAnalysis.HasField('trippingOut') and tdNormalAnalysis.enableTrippingOut:
                    trippingOut = tdNormalAnalysis.trippingOut
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    #速度
                    TRIP_SPEED = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_PARAMS_TRIP_OUT_TRIP_SPEED')
                    helper.SetCtrlValue(TRIP_SPEED,str(trippingOut.Speed))
                    #转盘转速
                    ROTATION_SPEED = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                            AutomationId='HorizontalTextBox_WP_TDA_PARAMS_TRIP_OUT_ROTATION_SPEED')
                    helper.SetCtrlValue(ROTATION_SPEED,str(trippingOut.RPM))
                elif tdCheckBox.Name == '在井底旋转' and tdNormalAnalysis.HasField('rotatingOnBottom') and tdNormalAnalysis.enableRotatingOnBottom:
                    rotatingOnBottom = tdNormalAnalysis.rotatingOnBottom
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    #钻压
                    ROTARY_WOB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_PARAMS_ROTARY_WOB')
                    helper.SetCtrlValue(ROTARY_WOB,str(rotatingOnBottom.WOB))
                    #钻头扭矩
                    ROTARY_TAB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_PARAMS_ROTARY_TAB')
                    helper.SetCtrlValue(ROTARY_TAB,str(rotatingOnBottom.TorqueAtBit))
                elif tdCheckBox.Name == '滑动钻进' and tdNormalAnalysis.HasField('slideDrilling') and tdNormalAnalysis.enableSlideDrilling:
                    slideDrilling = tdNormalAnalysis.slideDrilling
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    #钻压
                    SLIDE_WOB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_PARAMS_SLIDE_WOB')
                    helper.SetCtrlValue(SLIDE_WOB,str(slideDrilling.WOB))
                    #钻头扭矩
                    SLIDE_TAB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_WP_TDA_PARAMS_SLIDE_TAB')
                    helper.SetCtrlValue(SLIDE_TAB,str(slideDrilling.TorqueAtBit))
                elif tdCheckBox.Name == '倒划眼' and tdNormalAnalysis.HasField('backreaming') and tdNormalAnalysis.enableBackreaming:
                    backreaming = tdNormalAnalysis.backreaming
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    #过提
                    OVERPULL_WEIGHT = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_WP_TDA_PARAMS_OVERPULL_WEIGHT')
                    helper.SetCtrlValue(OVERPULL_WEIGHT,str(backreaming.Overpull))
                    #钻头扭矩
                    OPULL_TAB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_TDA_PARAMS_OPULL_TAB')
                    helper.SetCtrlValue(OPULL_TAB,str(backreaming.TorqueAtBit))
                elif tdCheckBox.Name == '旋转提离井底' and tdNormalAnalysis.RotatingOffBottom:
                    helper.AutoToggleStateClick(True, tdCheckBox)
                else:
                    helper.AutoToggleStateClick(False, tdCheckBox)
            tdGrp = tdGrp.GetNextSiblingControl()

    #处理 扭矩与摩阻自上而下分析
    def handleTorqueAndDragTopDownAnalysis(self,
                                           TorqueAndDragTopDownAnalysisGrp: auto.GroupControl,
                                           operationParam : OperationalParameters):
        tdGrp = TorqueAndDragTopDownAnalysisGrp.GroupControl(searchDepth=1, ClassName='GroupBox')
        if bool(tdGrp.IsEnabled) is False:
            return

        if helper.ExistCtrl(tdGrp) is False:
            return
        #勾住
        tdCheckBox = tdGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox', AutomationId='CheckBox_8')
        if helper.ExistCtrl(tdCheckBox):
            helper.AutoToggleStateClick(False, tdCheckBox)
            #若存在该值则表明使用用户定义的操作
            if not operationParam.HasField('tdTopDownAnalysis'):
                return
            helper.AutoToggleStateClick(True, tdCheckBox)
            tdTopDownAnalysis = operationParam.tdTopDownAnalysis
            #设置 自上而下
            if tdTopDownAnalysis.AnalysisDirection:
                # 钻压
                SINGLE_WOB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                         AutomationId='HorizontalTextBox_WP_TDA_PARAMS_SINGLE_WOB')
                helper.SetCtrlValue(SINGLE_WOB,str(tdTopDownAnalysis.WeightOnBit))
                # 钻头扭矩
                SINGLE_TAB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_WP_TDA_PARAMS_SINGLE_TAB')
                helper.SetCtrlValue(SINGLE_TAB,str(tdTopDownAnalysis.TorqueAtBit))
            else:
                topDown = tdGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton', AutomationId='RadioButton_2')
                helper.ClickOnce(topDown)
                # 地面载荷
                INJECTOR_FORCE = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_WP_TDA_PARAMS_INJECTOR_FORCE')
                helper.SetCtrlValue(INJECTOR_FORCE,str(tdTopDownAnalysis.SurfaceLoad))
                # 地面扭矩
                INJECTOR_TORQUE = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_WP_TDA_PARAMS_INJECTOR_TORQUE')
                helper.SetCtrlValue(INJECTOR_TORQUE,str(tdTopDownAnalysis.SurfaceTorque))
            # 速度
            TRIP_SPEED = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                AutomationId='HorizontalTextBox_WP_TDA_PARAMS_SINGLE_TRIP_SPEED')
            helper.SetCtrlValue(TRIP_SPEED,str(tdTopDownAnalysis.Speed))
            # 转盘转速
            ROTATION_SPEED = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                           AutomationId='HorizontalTextBox_WP_TDA_PARAMS_SINGLE_ROTATION_SPEED')
            helper.SetCtrlValue(ROTATION_SPEED,str(tdTopDownAnalysis.RPM))



    #处理 扭矩与摩阻混合模型
    def handleTorqueAndDragDiscreteModel(self,
                                               TorqueAndDragDiscreteModelGrp : auto.GroupControl,
                                               operationParam : OperationalParameters):
        if not operationParam.HasField('tdHybridModel'):
            return

        tdHybridModel = operationParam.tdHybridModel

        # 钻压
        wob = TorqueAndDragDiscreteModelGrp.RadioButtonControl(searchDepth=1,
                                                                ClassName='RadioButton',
                                                                AutomationId='RadioButton_7')
        # 钩载
        hook = TorqueAndDragDiscreteModelGrp.RadioButtonControl(searchDepth=1,
                                                                ClassName='RadioButton',
                                                                AutomationId='RadioButton_8')
        if tdHybridModel.UnknownParameter:
            helper.ClickOnce(wob)
        else:
            helper.ClickOnce(hook)

        tdGrp = TorqueAndDragDiscreteModelGrp.GroupControl(searchDepth=1, ClassName='GroupBox')

        if helper.ExistCtrl(tdGrp) is False:
            return

        while tdGrp != None:
            if tdGrp.ControlType != auto.ControlType.GroupControl:
                tdGrp = tdGrp.GetNextSiblingControl()
                continue

            tdCheckBox = tdGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox', AutomationId='CheckBox_8')
            if helper.ExistCtrl(tdCheckBox) and bool(tdCheckBox.IsEnabled):
                if tdCheckBox.Name == '下钻' and tdHybridModel.HasField('trippingIn') and tdHybridModel.enableTrippingIn:
                    trippingIn = tdHybridModel.trippingIn
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    if tdHybridModel.UnknownParameter:
                        # 钩载
                        TRIP_IN_HOOKLOAD = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_TRIP_IN_HOOKLOAD')
                        helper.SetCtrlValue(TRIP_IN_HOOKLOAD,str(trippingIn.HookLoad))
                    else:
                        # 钻压
                        TRIP_IN_WOB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_TRIP_IN_WOB')
                        helper.SetCtrlValue(TRIP_IN_WOB,str(trippingIn.WOB))
                elif tdCheckBox.Name == '起钻' and tdHybridModel.HasField('trippingOut') and tdHybridModel.enableTrippingOut:
                    trippingOut = tdHybridModel.trippingOut
                    helper.AutoToggleStateClick(True, tdCheckBox)
                    if tdHybridModel.UnknownParameter:
                        # 钩载
                        TRIP_OUT_HOOKLOAD = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_TRIP_OUT_HOOKLOAD')
                        helper.SetCtrlValue(TRIP_OUT_HOOKLOAD,str(trippingOut.HookLoad))
                    else:
                        # 钻压
                        TRIP_OUT_WOB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_TRIP_OUT_WOB')
                        helper.SetCtrlValue(TRIP_OUT_WOB,str(trippingOut.WOB))
                elif tdCheckBox.Name == '旋转' and tdHybridModel.HasField('rotating') and tdHybridModel.enableRotating:
                    rotating = tdHybridModel.rotating
                    helper.AutoToggleStateClick(True, tdCheckBox)

                    #地面扭矩
                    SURFACE_TORQUE = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_ROTATE_SURFACE_TORQUE')
                    helper.SetCtrlValue(SURFACE_TORQUE,str(rotating.SurfaceTorque))

                    if tdHybridModel.UnknownParameter:
                        # 钩载
                        ROTATE_HOOKLOAD = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_ROTATE_HOOKLOAD')
                        helper.SetCtrlValue(ROTATE_HOOKLOAD,str(rotating.HookLoad))
                    else:
                        # 钻压
                        PARAMS_ROTATE_WOB = tdGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_DISCRETE_PARAMS_ROTATE_WOB')
                        helper.SetCtrlValue(PARAMS_ROTATE_WOB,str(rotating.WOB))
                else:
                    helper.AutoToggleStateClick(False, tdCheckBox)
            tdGrp = tdGrp.GetNextSiblingControl()


    #处理 抽吸 & 波动
    def handleSwabAndSurge(self,
                           SwabAndSurgeGrp : auto.GroupControl,
                           operationParam : OperationalParameters):
        pass

    #处理 井控压井施工单
    def handleWellControlOperations(self,
                                    WellControlOperationsGrp: auto.GroupControl,
                                    operationParam: OperationalParameters):
        pass

    #处理 注水泥
    def handleCementingOperations(self,
                                  CementingOperationsGrp: auto.GroupControl,
                                  operationParam: OperationalParameters):
        pass
    #处理 BHA 动态
    def handleCriticalSpeedOperations(self,
                                      CriticalSpeedOperationsGrp: auto.GroupControl,
                                      operationParam: OperationalParameters):
        pass

    #处理 卡钻分析
    def handleStuckPipeOperations(self,
                                  StuckPipeOperationsGrp: auto.GroupControl,
                                  operationParam: OperationalParameters):
        pass


    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化作业信息")
        OperationalDataTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock',
                                                            AutomationId='OperationalDataTab')
        helper.ClickOnce(OperationalDataTab)

        OperationalDataEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                     ClassName='OperationalDataEditorView',
                                                                     AutomationId='StackPanel_1')

        UserControl_1 = OperationalDataEditorView.CustomControl(searchDepth=2, ClassName='OperationsEditorControl',
                                                                AutomationId='UserControl_1')
        # 扭矩与摩阻标准分析
        if self.validTorqueAndDragNormalAnalysis():
            TorqueAndDragNormalAnalysisGrp = UserControl_1.GroupControl(searchDepth=1, ClassName='Expander',
                                                                        AutomationId='TorqueAndDragNormalAnalysisExpander')
            TorqueAndDragNormalAnalysisBtn = TorqueAndDragNormalAnalysisGrp.ButtonControl(searchDepth=1,
                                                                                          ClassName='Button',
                                                                                          AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, TorqueAndDragNormalAnalysisBtn)
            self.handleTorqueAndDragNormalAnalysis(TorqueAndDragNormalAnalysisGrp, self.operationParam)

        # 扭矩与摩阻自上而下分析
        if self.validTorqueAndDragTopDownAnalysis():
            TorqueAndDragTopDownAnalysisGrp = UserControl_1.GroupControl(searchDepth=1, ClassName='Expander',
                                                                         AutomationId='TorqueAndDragTopDownAnalysisExpander')
            TorqueAndDragTopDownAnalysisBtn = TorqueAndDragTopDownAnalysisGrp.ButtonControl(searchDepth=1,
                                                                                            ClassName='Button',
                                                                                            AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, TorqueAndDragTopDownAnalysisBtn)
            self.handleTorqueAndDragTopDownAnalysis(TorqueAndDragTopDownAnalysisGrp, self.operationParam)

        # 扭矩与摩阻混合模型
        if self.validTorqueAndDragDiscreteModel():
            TorqueAndDragDiscreteModelGrp = UserControl_1.GroupControl(searchDepth=1, ClassName='Expander',
                                                                       AutomationId='TorqueAndDragDiscreteModelExpander')
            TorqueAndDragDiscreteModelBtn = TorqueAndDragDiscreteModelGrp.ButtonControl(searchDepth=1,
                                                                                        ClassName='Button',
                                                                                        AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, TorqueAndDragDiscreteModelBtn)
            self.handleTorqueAndDragDiscreteModel(TorqueAndDragDiscreteModelGrp, self.operationParam)

        # 抽吸 & 波动
        if self.validSwabAndSurgeOperations():
            SwabAndSurgeGrp = OperationalDataEditorView.GroupControl(searchDepth=3, ClassName='Expander',
                                                                     AutomationId='SwabAndSurgeOperationsTabExpander')
            SwabAndSurgeBtn = SwabAndSurgeGrp.ButtonControl(searchDepth=1,
                                                            ClassName='Button',
                                                            AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, SwabAndSurgeBtn)
            self.handleSwabAndSurge(SwabAndSurgeGrp, self.operationParam)

        # 井控压井施工单
        if self.validWellControlOperations():
            wellcontrolExpander = OperationalDataEditorView.CustomControl(searchDepth=2,
                                                                          ClassName='OperationsEditorControl',
                                                                          AutomationId='_wellcontrolExpander')
            WellControlOperationsGrp = wellcontrolExpander.GroupControl(searchDepth=1, ClassName='Expander',
                                                                     AutomationId='WellControlOperationsTabExpander')
            WellControlOperationsBtn = WellControlOperationsGrp.ButtonControl(searchDepth=1,
                                                            ClassName='Button',
                                                            AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, WellControlOperationsBtn)
            self.handleWellControlOperations(WellControlOperationsGrp, self.operationParam)

        # 注水泥
        if self.vaildCementingOperations():
            CementingOperationsExpander = OperationalDataEditorView.CustomControl(searchDepth=2,
                                                                          ClassName='CementingOperationsEditorControl')
            CementingOperationsGrp = CementingOperationsExpander.GroupControl(searchDepth=1, ClassName='Expander',
                                                                              AutomationId='CementingOperationsTabExpanDer')
            CementingOperationsBtn = CementingOperationsGrp.ButtonControl(searchDepth=1,
                                                                              ClassName='Button',
                                                                              AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, CementingOperationsBtn)
            self.handleCementingOperations(CementingOperationsGrp, self.operationParam)

        # BHA 动态
        if self.validCriticalSpeedOperations():
            CriticalSpeedOperationsExpander = OperationalDataEditorView.CustomControl(searchDepth=2,
                                                                                  ClassName='CriticalSpeedOperationsEditorControl')
            CriticalSpeedOperationsGrp = CriticalSpeedOperationsExpander.GroupControl(searchDepth=1, ClassName='Expander',
                                                                              AutomationId='TorqueAndDragAnalysisSettingsExpander')
            CriticalSpeedOperationsBtn = CriticalSpeedOperationsGrp.ButtonControl(searchDepth=1,
                                                                          ClassName='Button',
                                                                          AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, CriticalSpeedOperationsBtn)
            self.handleCriticalSpeedOperations(CriticalSpeedOperationsGrp, self.operationParam)

        # 卡钻分析
        if self.validStuckPipeOperations():
            StuckPipeOperationsExpander = OperationalDataEditorView.CustomControl(searchDepth=2,
                                                                                      ClassName='StuckPipeOperationsEditorControl')
            StuckPipeOperationsGrp = StuckPipeOperationsExpander.GroupControl(searchDepth=1, ClassName='Expander',
                                                                                      AutomationId='TorqueAndDragAnalysisSettingsExpander')
            StuckPipeOperationsBtn = StuckPipeOperationsGrp.ButtonControl(searchDepth=1,
                                                                                  ClassName='Button',
                                                                                  AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, StuckPipeOperationsBtn)
            self.handleStuckPipeOperations(StuckPipeOperationsGrp, self.operationParam)
        if self.isConnected():
            listener.sendStatus(self.conn, "作业信息初始化完毕")


