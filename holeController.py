# -*- coding: utf-8 -*-

from protocol.wellplan_pb2 import HoleSectionEditor
from launcher import *
from network import listener
import helper


class HoleController:
    cxt = Context()
    holeSectionEditor = HoleSectionEditor()
    conn: WebSocket = None

    def __init__(self, cxt: Context, holeSectionEditor: HoleSectionEditor, conn: WebSocket = None):
        self.cxt = cxt
        self.holeSectionEditor = holeSectionEditor
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    # 隔水
    def riser(self, HoleSectionEditorView: auto.CustomControl, holeSectionEditor: HoleSectionEditor):
        # 设置隔水数值
        RiserContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='RiserContainer',
                                                             AutomationId='UserControl_1')
        # 进行删除
        if helper.ExistCtrl(RiserContainer):
            DeleteRiserButton = RiserContainer.ButtonControl(searchDepth=4, ClassName='Button',
                                                             AutomationId='DeleteRiserButton')
            helper.ClickOnce(DeleteRiserButton)

        if holeSectionEditor.HasField('riser'):
            RiserContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='RiserContainer',
                                                                 AutomationId='UserControl_1')
            # 隔水管添加按钮
            HoleSectionEditorDisplayAddRiserButton = HoleSectionEditorView.ButtonControl(searchDepth=2,
                                                                                         ClassName='Button',
                                                                                         AutomationId='HoleSectionEditorDisplayAddRiserButton')
            helper.ClickOnce(HoleSectionEditorDisplayAddRiserButton)

            # 外径
            if holeSectionEditor.riser.HasField('OD'):
                OuterDIA = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_OD_CASING')
                helper.SetCtrlValue(OuterDIA,str(holeSectionEditor.riser.OD))
            # 内径
            if holeSectionEditor.riser.HasField('ID'):
                InnerDIA = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_HOLE_SIZE')
                helper.SetCtrlValue(InnerDIA,str(holeSectionEditor.riser.ID))
            # 摩擦系数
            if holeSectionEditor.riser.HasField('FrictionFactor'):
                Friction = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_COF')
                helper.SetCtrlValue(Friction,str(holeSectionEditor.riser.FrictionFactor))
            # 线性容积
            if holeSectionEditor.riser.HasField('LinearCapacity'):
                Capacity = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_LINEAR_CAPACITY')
                helper.SetCtrlValue(Capacity,str(holeSectionEditor.riser.LinearCapacity))
            # 描述
            if holeSectionEditor.riser.HasField('Desc'):
                Desc = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                  AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_CATALOG_KEY_DESC')
                helper.SetCtrlValue(Desc,holeSectionEditor.riser.Desc)
            # 生产商
            ########暂未设置
            if holeSectionEditor.riser.HasField('manu'):
                pass
            # 模式
            if holeSectionEditor.riser.HasField('Model'):
                Model = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_MODEL')
                helper.SetCtrlValue(Model,holeSectionEditor.riser.Model)
            # 增压泵
            if holeSectionEditor.riser.HasField('Pump'):
                Pump = RiserContainer.CheckBoxControl(searchDepth=4, ClassName='CheckBox',
                                                      AutomationId='BoosterPumpIsEnabledCheckbox')
                if Pump.GetTogglePattern().ToggleState != auto.ToggleState.On:
                    Pump.SetFocus()
                    Pump.SendKey(auto.Keys.VK_SPACE)
                # 注入深度
                if holeSectionEditor.riser.Pump.HasField('InjectionDepth'):
                    InjectDepth = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_CASE_BOOSTER_PUMP_INJECTION_DEPTH')
                    helper.SetCtrlValue(InjectDepth,str(holeSectionEditor.riser.Pump.InjectionDepth))
                # 注入温度
                if holeSectionEditor.riser.Pump.HasField('InjectionTemperature'):
                    InjectTemper = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                              AutomationId='HorizontalTextBox_WP_CASE_BOOSTER_PUMP_INJECTION_TEMPERATURE')
                    helper.SetCtrlValue(InjectTemper,str(holeSectionEditor.riser.Pump.InjectionTemperature))
                # 注入率
                if holeSectionEditor.riser.Pump.HasField('InjectionRate'):
                    InjectRate = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                            AutomationId='HorizontalTextBox_WP_CASE_BOOSTER_PUMP_INJECTION_RATE')
                    helper.SetCtrlValue(InjectRate,str(holeSectionEditor.riser.Pump.InjectionRate))

                helper.ClickOnce(RiserContainer)

    # 摩擦系数
    def frictionFactors(self, HoleSectionEditorView: auto.CustomControl, holeSectionEditor: HoleSectionEditor):
        ExpanderGrp = HoleSectionEditorView.GroupControl(searchDepth=2,
                                                         ClassName='Expander',
                                                         AutomationId='Expander_1')

        HeaderSite = ExpanderGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, HeaderSite)
        # 选择默认
        per1 = ExpanderGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton', AutomationId='RadioButton_1')
        helper.ClickOnce(per1)

        if holeSectionEditor.HasField('frictionFactors'):
            frictionFactors = holeSectionEditor.frictionFactors

            per = ExpanderGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton', AutomationId='RadioButton_2')
            helper.ClickOnce(per)

            # TRIP_IN
            CASING_TRIP_IN = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_CASING_TRIP_IN')
            helper.SetCtrlValue(CASING_TRIP_IN, str(frictionFactors.trippingIn.Casing))

            OH_TRIP_IN = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                 AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_OH_TRIP_IN')
            helper.SetCtrlValue(OH_TRIP_IN, str(frictionFactors.trippingIn.OpenHole))

            # TRIP_OUT
            CASING_TRIP_OUT = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_CASING_TRIP_OUT')
            helper.SetCtrlValue(CASING_TRIP_OUT, str(frictionFactors.trippingOut.Casing))

            OH_TRIP_OUT = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                  AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_OH_TRIP_OUT')
            helper.SetCtrlValue(OH_TRIP_OUT, str(frictionFactors.trippingOut.OpenHole))
            # ROT_ON_BOTTOM
            CASING_ROT_ON_BOTTOM = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_CASING_ROT_ON_BOTTOM')
            helper.SetCtrlValue(CASING_ROT_ON_BOTTOM, str(frictionFactors.rotatingOnBottom.Casing))

            OH_ROT_ON_BOTTOM = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_OH_ROT_ON_BOTTOM')
            helper.SetCtrlValue(OH_ROT_ON_BOTTOM, str(frictionFactors.rotatingOnBottom.OpenHole))

            # SLIDING
            CASING_SLIDING = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_CASING_SLIDING')
            helper.SetCtrlValue(CASING_SLIDING, str(frictionFactors.slideDrilling.Casing))

            OH_SLIDING = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                 AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_OH_SLIDING')
            helper.SetCtrlValue(OH_SLIDING, str(frictionFactors.slideDrilling.OpenHole))

            # BACK_REAMING
            CASING_BACK_REAMING = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_CASING_BACK_REAMING')
            helper.SetCtrlValue(CASING_BACK_REAMING, str(frictionFactors.backReaming.Casing))

            OH_BACK_REAMING = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_OH_BACK_REAMING')
            helper.SetCtrlValue(OH_BACK_REAMING, str(frictionFactors.backReaming.OpenHole))

            # ROT_OFF_BOTTOM
            CASING_ROT_OFF_BOTTOM = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                            AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_CASING_ROT_OFF_BOTTOM')
            helper.SetCtrlValue(CASING_ROT_OFF_BOTTOM, str(frictionFactors.rotatingOffBottom.Casing))

            OH_ROT_OFF_BOTTOM = ExpanderGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_WP_TDA_PARAMS_COF_OH_ROT_OFF_BOTTOM')
            helper.SetCtrlValue(OH_ROT_OFF_BOTTOM, str(frictionFactors.rotatingOffBottom.OpenHole))

    # 套管
    def casing(self, HoleSectionEditorView: auto.CustomControl, holeSectionEditor: HoleSectionEditor):
        # 清空
        while True:
            # 套管
            CasingContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='CasingContainer',
                                                                  AutomationId='UserControl_1', foundIndex=1)
            if helper.ExistCtrl(CasingContainer) is False:
                break

            DeleteHoleSectionCasingButton = CasingContainer.ButtonControl(searchDepth=4, ClassName='Button',
                                                                          AutomationId='DeleteHoleSectionCasingButton')
            helper.ClickOnce(DeleteHoleSectionCasingButton)

        if len(holeSectionEditor.casing) > 0:
            HoleSectionEditorDisplayAddCasingButton = HoleSectionEditorView.ButtonControl(searchDepth=2,
                                                                                          ClassName='Button',
                                                                                          AutomationId='HoleSectionEditorDisplayAddCasingButton')
            count = 1
            for elem in holeSectionEditor.casing:
                helper.ClickOnce(HoleSectionEditorDisplayAddCasingButton)
                # 套管
                CasingContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='CasingContainer',
                                                                      AutomationId='UserControl_1', foundIndex=count)
                CasingContainer.SetFocus()
                # 长度
                if elem.HasField('Length'):
                    Length = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                         AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_LENGTH')
                    helper.SetCtrlValue(Length, str(elem.Length))

                # 变径, 默认是未开启
                Tapered = CasingContainer.CheckBoxControl(searchDepth=4, ClassName='CheckBox',
                                                          AutomationId='CasingItem_Tapered')
                if bool(Tapered.IsEnabled):
                    helper.AutoToggleStateClick(elem.enableTapered, Tapered)
                    if elem.enableTapered:
                        # 套管鞋测深MD
                        if elem.HasField('ShoeMD'):
                            MDShoe = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_MD_SHOE')
                            helper.SetCtrlValue(MDShoe, str(elem.ShoeMD))

                # 外径
                if elem.HasField('OD'):
                    OuterDIA = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_OD_CASING')
                    helper.SetCtrlValue(OuterDIA, str(elem.OD))
                # 内径
                if elem.HasField('ID'):
                    InnerDIA = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_HOLE_SIZE')
                    helper.SetCtrlValue(InnerDIA, str(elem.ID))
                # 内通径
                if elem.HasField('DriftId'):
                    Drift = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_ID_DRIFT')
                    helper.SetCtrlValue(Drift, str(elem.DriftId))
                # 有效井眼直径
                if elem.HasField('EffectiveHoleDiameter'):
                    DIAMETER = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_EFFECTIVE_DIAMETER')
                    helper.SetCtrlValue(DIAMETER, str(elem.EffectiveHoleDiameter))
                # 重量
                if elem.HasField('Weight'):
                    WEIGHT = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                         AutomationId='HorizontalTextBox_CASINGITEM_WEIGHT')
                    helper.SetCtrlValue(WEIGHT, str(elem.Weight))
                # 级  combox未实现
                if elem.HasField('grade'):
                    Lvl = CasingContainer.ComboBoxControl(searchDepth=4, ClassName='ComboBox',
                                                          AutomationId='ComboBox_1')
                    helper.ComboBoxCtrlRestore(Lvl)
                    helper.SetCtrlComboBoxValue(Lvl, elem.grade)
                # 最小屈服强度
                if elem.HasField('MinYieldStrength'):
                    MinYieleStress = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_MIN_YIELD_STRESS')
                    helper.SetCtrlValue(MinYieleStress, str(elem.MinYieldStrength))
                # 抗内压度
                if elem.HasField('BurstRating'):
                    BURST = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_PRESSURE_BURST')
                    helper.SetCtrlValue(BURST, str(elem.BurstRating))
                # 抗挤强度率
                if elem.HasField('CollapseRating'):
                    COLLAPSE = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_PRESSURE_COLLAPSE')
                    helper.SetCtrlValue(COLLAPSE, str(elem.CollapseRating))
                # 摩擦系数
                if not holeSectionEditor.HasField('frictionFactors') and elem.HasField('FrictionFactor'):
                    try:
                        COF = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_COF')

                        helper.SetCtrlValue(COF, str(elem.FrictionFactor))
                    except Exception as e:
                        logger.exception(e)
                        #摩擦系数2
                        COF2 = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_COF2')
                        helper.SetCtrlValue(COF2, str(elem.FrictionFactor))
                # 线性容积
                if elem.HasField('LinearCapacity'):
                    CAPACITY = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_LINEAR_CAPACITY')
                    helper.SetCtrlValue(CAPACITY, str(elem.LinearCapacity))
                # 描述
                if elem.HasField('Desc'):
                    DESC = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_CATALOG_KEY_DESC')
                    helper.SetCtrlValue(DESC, elem.Desc)
                # 生产商 combox未实现
                if elem.HasField('Manu'):
                    Manu = CasingContainer.ComboBoxControl(searchDepth=4, ClassName='ComboBox',
                                                           AutomationId='ComboBox_2')
                    ### DOTO: 完善选项逻辑
                    helper.ComboBoxCtrlRestore(Manu)
                    helper.SetCtrlComboBoxValue(Manu, elem.Manu)
                # 模式
                if elem.HasField('Model'):
                    Model = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_MODEL')
                    helper.SetCtrlValue(Model, elem.Model)

                count += 1

    # 裸眼
    def openHole(self, HoleSectionEditorView: auto.CustomControl, holeSectionEditor: HoleSectionEditor):
        # 清空
        while True:
            # 套管
            OpenHoleContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='OpenHoleContainer',
                                                                  AutomationId='UserControl_1', foundIndex=1)
            if helper.ExistCtrl(OpenHoleContainer) is False:
                break
            DeleteOpenHoleSectionButton = OpenHoleContainer.ButtonControl(searchDepth=4, ClassName='Button',
                                                                          AutomationId='DeleteOpenHoleSectionButton')
            helper.ClickOnce(DeleteOpenHoleSectionButton)

        if len(holeSectionEditor.openHole) > 0:
            # 祼眼
            HoleSectionEditorDisplayAddOpenHoleButton = HoleSectionEditorView.ButtonControl(searchDepth=2,
                                                                                            ClassName='Button',
                                                                                            AutomationId='HoleSectionEditorDisplayAddOpenHoleButton')
            count = 1
            for elem in holeSectionEditor.openHole:
                helper.ClickOnce(HoleSectionEditorDisplayAddOpenHoleButton)

                # 裸眼容器
                OpenHoleContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='OpenHoleContainer',
                                                                        AutomationId='UserControl_1', foundIndex=count)
                OpenHoleContainer.SetFocus()
                # 长度
                if elem.HasField('Length'):
                    Length = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_LENGTH')
                    helper.SetCtrlValue(Length, str(elem.Length))
                # 内径
                if elem.HasField('ID'):
                    Inner = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_HOLE_SIZE')
                    helper.SetCtrlValue(Inner, str(elem.ID))
                # 有效直径
                if elem.HasField('EffectiveDiameter'):
                    DIAMETER = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_EFFECTIVE_DIAMETER')
                    helper.SetCtrlValue(DIAMETER, str(elem.EffectiveDiameter))
                # 摩擦系数
                if not holeSectionEditor.HasField('frictionFactors') and elem.HasField('FrictionFactor'):
                    COF = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_COF')
                    helper.SetCtrlValue(COF, str(elem.FrictionFactor))
                    ## 摩擦系数2
                    # COF2 = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                    #                                     AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_COF2')
                    # helper.SetCtrlValue(COF2, str(elem.FrictionFactor))
                # 线性容积
                # CAPACITY = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                #                                         AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_LINEAR_CAPACITY')
                #
                # print('裸眼--线性容积可修改')
                # 体积超量
                VOLUME = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_VOLUME_EXCESS')
                helper.SetCtrlValue(VOLUME, str(elem.VolumeExcess))
                # 描述
                if elem.HasField('Desc'):
                    DESC = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox',
                                                         AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_CATALOG_KEY_DESC')
                    helper.SetCtrlValue(DESC, elem.Desc)
                count += 1

    def annulusEccentricity(self, HoleSectionEditorView: auto.CustomControl, holeSectionEditor: HoleSectionEditor):
        if holeSectionEditor.HasField('annulusEccentricity'):
            pass

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化井身信息")
        HoleSectionTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock',
                                                        AutomationId='HoleSectionTab')
        helper.ClickOnce(HoleSectionTab)
        # 点击井身后的操作
        HoleSectionEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                 ClassName='HoleSectionEditorView',
                                                                 AutomationId='HoleSectionEditorView')
        helper.ExistCtrl(HoleSectionEditorView)

        self.riser(HoleSectionEditorView, self.holeSectionEditor)
        self.frictionFactors(HoleSectionEditorView, self.holeSectionEditor)
        self.casing(HoleSectionEditorView, self.holeSectionEditor)
        self.openHole(HoleSectionEditorView, self.holeSectionEditor)
        self.annulusEccentricity(HoleSectionEditorView, self.holeSectionEditor)

        if self.isConnected():
            listener.sendStatus(self.conn, "井身信息初始化完毕")
