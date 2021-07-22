# -*- coding: utf-8 -*-
import pyperclip

from protocol.wellplan_pb2 import FluidsEditor
from protocol.wellplan_pb2 import BarTab
from launcher import *
from network import listener
import helper

class FluidsController:
    cxt = Context()
    fluidsEditor = FluidsEditor()
    rowCount = 1
    conn: WebSocket = None

    def __init__(self, cxt : Context, fluidsEditor : FluidsEditor, conn: WebSocket = None):
        self.cxt = cxt
        self.fluidsEditor = fluidsEditor
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    #用于判断所选 指标 是否会导致流体编辑窗体 产生动态变化
    def validRheologyBar(self) -> bool:
        if config.TEST_MODE:
            return True

        if isinstance(self.cxt.bar_high, BarTab.TorqueDrag):
            return True
        elif isinstance(self.cxt.bar_high, BarTab.Hydraulics):
            return True
        elif isinstance(self.cxt.bar_high, BarTab.Cementing):
            if self.cxt.bar_t == BarTab.Cementing.CentralizationPlots:
                if self.cxt.bar_idx != BarTab.Cementing.CentralizationPlots.CentralizationIntervals:
                    return False
            return True
        elif isinstance(self.cxt.bar_high, BarTab.SwabSurge):
            return True
        elif isinstance(self.cxt.bar_high, BarTab.UBHydraulics):
            return True
        elif isinstance(self.cxt.bar_high, BarTab.WellControl):
            return True
        elif isinstance(self.cxt.bar_high, BarTab.BHADynamics):
            return True
        elif isinstance(self.cxt.bar_high, BarTab.StuckPipe):
            return True

        return False

    #动态变化的窗体 数值编辑
    def rheology(self, FluidItem : auto.CustomControl, rheology : FluidsEditor.RheologyTests, Density : float):
        if self.validRheologyBar() is False:
            return

        RheologyTests = FluidsEditor.RheologyTests
        RheologyGrp = FluidItem.GroupControl(searchDepth=1, ClassName='GroupBox',
                                           AutomationId='GroupBox_Rheology')
        RheologyDataCtrl = FluidItem.CustomControl(searchDepth=1, ClassName='RheologyDataControl', AutomationId='RheologyDataControl')
        checkboxFoamable = RheologyGrp.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                           AutomationId='CheckBox_6')
        helper.AutoToggleStateClick(rheology.enableFoamable, checkboxFoamable)

        RHEOLOGYMODELCOMBOBOX = RheologyGrp.ComboBoxControl(searchDepth=1, ClassName='ComboBox', AutomationId='HorizontalComboBox_RHEOLOGYMODELCOMBOBOX')
        #复原
        helper.ComboBoxCtrlRestore(RHEOLOGYMODELCOMBOBOX)
        #设置值
        helper.SetCtrlComboBoxValue(RHEOLOGYMODELCOMBOBOX, rheology.model)

        #范式
        FannRadio = None
        if rheology.IsRheology:
            FannRadio = RheologyGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton', AutomationId='RadioButton_1')
        else:
            FannRadio = RheologyGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton', AutomationId='RadioButton_2')

        helper.ClickOnce(FannRadio)

        #表格 -- 温度 & 压力
        RheologyGrid = RheologyGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                                AutomationId='RheologyDataTableGrid')
        # 首行，需要设置该行数据
        FirstRow = RheologyGrid.DataItemControl(searchDepth=1, foundIndex=1, ClassName='DataGridRow',
                                                      Name='DSWE.Core.Presentation.FluidEditor.PresentationModel.RheologyDataModel')
        item1 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=1)
        txt1 = item1.TextControl(searchDepth=1, ClassName='TextBlock')
        helper.ClickOnce(item1)
        item1.DoubleClick()
        item1.SendKeys('{CTRL}A')
        item1.SendKeys(str(rheology.Temperature))
        item2 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=2)
        txt2 = item2.TextControl(searchDepth=1, ClassName='TextBlock')
        helper.ClickOnce(item2)
        item2.DoubleClick()
        item2.SendKeys('{CTRL}A')
        item2.SendKeys(str(rheology.Pressure))

        fIdx = 3
        #当为范式且流变模型为 -- GeneralizedHerschelBulkley时此值有效
        if not rheology.IsRheology and rheology.model == RheologyTests.RheologyModel.GeneralizedHerschelBulkley:
            item3 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=fIdx)
            txt3 = item3.TextControl(searchDepth=1, ClassName='TextBlock')
            helper.ClickOnce(item3)
            item3.DoubleClick()
            item3.SendKeys('{CTRL}A')
            item3.SendKeys(str(rheology.FYSA))
            fIdx += 1
        #若开启了泡沫且流变模型为 GeneralizedHerschelBulkley时此值有效 则需要点击该选项
        if rheology.enableFoamable and rheology.model == RheologyTests.RheologyModel.GeneralizedHerschelBulkley:
            item4 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=fIdx + 1)
            radioBtn = item4.RadioButtonControl(searchDepth=1, ClassName='RadioButton')
            if bool(radioBtn.IsEnabled):
                radioBtn.Click()

        #密度
        DENSITY = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox', AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
        DENSITY.Click()
        helper.SetCtrlValue(DENSITY,str(Density))

        if rheology.HasField('details'):
            details = rheology.details

            if rheology.enableFoamable and rheology.model == RheologyTests.RheologyModel.GeneralizedHerschelBulkley:
                if details.HasField('FoamableDensity'):
                    FoamableDensity = RheologyDataCtrl.RadioButtonControl(searchDepth=1, ClassName='RadioButton', AutomationId='CheckBox_1')
                    helper.ClickOnce(FoamableDensity)
                    DENSITY = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_FLUID_TEMP_DENSITY')
                    helper.SetCtrlValue(DENSITY,str(details.FoamableDensity))
                elif details.HasField('FoamableQuality'):
                    useQuality = RheologyDataCtrl.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                          AutomationId='useQuality')
                    helper.ClickOnce(useQuality)
                    QUALITY = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_WP_FLUID_TEMP_QUALITY')
                    helper.SetCtrlValue(QUALITY,str(details.FoamableQuality))

            if rheology.IsRheology:
                # 塑性粘度
                def VISCOSITY_Handler(PlasticViscosity):
                    VISCOSITY = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_FLUID_TEMP_PLASTIC_VISCOSITY')
                    #VISCOSITY.Click()
                    helper.SetCtrlValue(VISCOSITY,str(PlasticViscosity))
                # 屈服值点/屈服值强度
                def YIELD_POINT_Handler(YieldPoint):
                    YIELD_POINT = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                               AutomationId='HorizontalTextBox_WP_FLUID_TEMP_YIELD_POINT')
                    #YIELD_POINT.Click()
                    helper.SetCtrlValue(YIELD_POINT,str(YieldPoint))
                #n'/n
                def Np_Handler(Np):
                    N_PRIME_PARAMETER = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                               AutomationId='HorizontalTextBox_WP_FLUID_TEMP_N_PRIME_PARAMETER')
                    #N_PRIME_PARAMETER.Click()
                    helper.SetCtrlValue(N_PRIME_PARAMETER,str(Np))
                #K‘/K
                def Kp_Handler(Kp):
                    K_PRIME_PARAMETER = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_FLUID_TEMP_K_PRIME_PARAMETER')
                    #K_PRIME_PARAMETER.Click()
                    helper.SetCtrlValue(K_PRIME_PARAMETER,str(Kp))
                def M_Handler(M):
                    M_PRIME_PARAMETER = RheologyDataCtrl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_FLUID_TEMP_M_PARAMETER')
                    #M_PRIME_PARAMETER.Click()
                    helper.SetCtrlValue(M_PRIME_PARAMETER,str(M))

                if details.HasField('Rheology'):
                    if rheology.model == RheologyTests.RheologyModel.BinghamPlastic:
                        rheologyMsg = RheologyTests.RheologyTestsDetails.BinghamPlasticRheologyMsg()
                        rheologyMsg.ParseFromString(details.Rheology)
                        VISCOSITY_Handler(rheologyMsg.PlasticViscosity)
                        YIELD_POINT_Handler(rheologyMsg.YieldPoint)
                    elif rheology.model == RheologyTests.RheologyModel.PowerLaw:
                        rheologyMsg = RheologyTests.RheologyTestsDetails.PowerLawRheologyMsg()
                        rheologyMsg.ParseFromString(details.Rheology)
                        Np_Handler(rheologyMsg.Np)
                        Kp_Handler(rheologyMsg.Kp)
                    elif rheology.model == RheologyTests.RheologyModel.HerschelBulkley:
                        rheologyMsg = RheologyTests.RheologyTestsDetails.HerschelBulkleyRheologyMsg()
                        rheologyMsg.ParseFromString(details.Rheology)
                        YIELD_POINT_Handler(rheologyMsg.YieldStrength)
                        Np_Handler(rheologyMsg.N)
                        Kp_Handler(rheologyMsg.K)
                    elif rheology.model == RheologyTests.RheologyModel.GeneralizedHerschelBulkley:
                        rheologyMsg = RheologyTests.RheologyTestsDetails.GeneralizedHerschelBulkleyRheologyMsg()
                        rheologyMsg.ParseFromString(details.Rheology)
                        VISCOSITY_Handler(rheologyMsg.PlasticViscosity)
                        YIELD_POINT_Handler(rheologyMsg.YieldStrength)
                        Np_Handler(rheologyMsg.N)
                        M_Handler(rheologyMsg.M)
                    elif rheology.model == RheologyTests.RheologyModel.Newtonian:
                        rheologyMsg = RheologyTests.RheologyTestsDetails.NewtonianRheologyMsg()
                        rheologyMsg.ParseFromString(details.Rheology)
                        VISCOSITY_Handler(rheologyMsg.PlasticViscosity)
            else:
                #范式数据 -- 表格
                FannDatagGridGrp = RheologyDataCtrl.GroupControl(searchDepth=1, ClassName='GroupBox', AutomationId='GroupBox_1',Name = '范式数据')
                FannDatagGrid = FannDatagGridGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                           AutomationId='FluidFannDatagGrid')
                headerFirst = FannDatagGrid.HeaderControl(searchDepth=1, ClassName='DataGridColumnHeadersPresenter',
                                            AutomationId='PART_ColumnHeadersPresenter')
                helper.ClearDataGrid(FannDatagGrid)

                tableData = ''
                for elem in details.Fanns:
                    tableData += '{}	{}\r\n'.format(elem.Speed, elem.Dial)

                if len(details.Fanns) > 0:
                   helper.WriteDataToDataGrid(FannDatagGrid, tableData)

    def mudDetails(self,
                   FluidEditorView : auto.CustomControl,
                   fluidsEditor : FluidsEditor,
                   fluidList : auto.ListControl,
                   AddFluidButton : auto.ButtonControl):
        # 选项的细节
        FluidItem = FluidEditorView.CustomControl(searchDepth=2, ClassName='FluidItem',
                                                  AutomationId='UserControl_1')
        count = 0
        for elem in fluidsEditor.mudDetails:
            count += 1

            # 名称
            if elem.HasField('Name'):
                FLUID_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_FLUID_FLUID_NAME')
                helper.SetCtrlValue(FLUID_NAME,str(elem.Name))
            # 描述
            if elem.HasField('Desc'):
                COMPANY_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_FLUID_COMPANY_NAME')
                helper.SetCtrlValue(COMPANY_NAME,str(elem.Desc))
            # 密度
            '''
            if elem.HasField('Density'):
                TEMP_BASE_DENSITY1 = FluidItem.EditControl(foundIndex=1, searchDepth=2, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
                if TEMP_BASE_DENSITY1.Exists(0, 0):
                    helper.SetCtrlValue(TEMP_BASE_DENSITY1,str(elem.Density))

                TEMP_BASE_DENSITY2 = FluidItem.EditControl(foundIndex=2, searchDepth=2, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
                if TEMP_BASE_DENSITY2.Exists(0, 0):
                    helper.SetCtrlValue(TEMP_BASE_DENSITY2,str(elem.Density))
            '''
            # 流体抗压缩性
            FluidComposition = FluidItem.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                      AutomationId='GroupBox_FluidComposition')

            # Mud 基础类型
            mudCombo = FluidComposition.ComboBoxControl(searchDepth=1, ClassName='ComboBox',
                                                        AutomationId='MudBaseTypeComboBox')
            helper.ComboBoxCtrlRestore(mudCombo)
            if elem.fluidComposition.mudBaseType > 0:
                helper.SetCtrlComboBoxValue(mudCombo, elem.fluidComposition.mudBaseType)

                # 基础流体
                if elem.fluidComposition.HasField('baseFluid'):
                    baseFluidCombo = FluidComposition.ComboBoxControl(searchDepth=1, ClassName='ComboBox',
                                                                 AutomationId='BaseFluidComboBox')
                    helper.ComboBoxCtrlRestore(baseFluidCombo)
                    helper.SetCtrlComboBoxValue(baseFluidCombo, elem.fluidComposition.baseFluid.base)

                    baseFluid = elem.fluidComposition.baseFluid
                    if baseFluid.HasField('data'):
                        if (elem.fluidComposition.mudBaseType == FluidsEditor.MudDetails.MudBaseType.Oil and
                            baseFluid.base > FluidsEditor.MudDetails.BaseFluid.BaseOil.Diesel) or \
                                elem.fluidComposition.mudBaseType == FluidsEditor.MudDetails.MudBaseType.Synthetic:
                            CompressibilityGrp = FluidComposition.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                                               AutomationId='GroupBox_Compressibility')
                            data = baseFluid.data
                            # 油含量（体积）
                            if data.HasField('OilContent_Vol'):
                                PERCENT_OIL = CompressibilityGrp.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FLUID_PERCENT_OIL')
                                helper.SetCtrlValue(PERCENT_OIL,str(data.OilContent_Vol))
                            # 水含量（体积）
                            if data.HasField('WaterContent_Vol'):
                                PERCENT_WATER = CompressibilityGrp.EditControl(searchDepth=1,
                                                                               ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_CD_FLUID_PERCENT_WATER')
                                helper.SetCtrlValue(PERCENT_WATER,str(data.WaterContent_Vol))
                            # 盐度（重量）
                            if data.HasField('SaltContext_Wt'):
                                CONC_NACL = CompressibilityGrp.EditControl(searchDepth=1,
                                                                           ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_FLUID_CONC_NACL')
                                helper.SetCtrlValue(CONC_NACL,str(data.SaltContext_Wt))
                            # 参考温度
                            if data.HasField('ReferenceTemperature'):
                                TEMP_DENSITY = CompressibilityGrp.EditControl(searchDepth=1,
                                                                              ClassName='TextBox',
                                                                              AutomationId='HorizontalTextBox_CD_FLUID_TEMP_DENSITY')
                                helper.SetCtrlValue(TEMP_DENSITY,str(data.ReferenceTemperature))
                            # 平均固体重力
                            if data.HasField('AverageSolidsGravity'):
                                SOLIDS_SG_AVG = CompressibilityGrp.EditControl(searchDepth=1,
                                                                               ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_CD_FLUID_SOLIDS_SG_AVG')
                                helper.SetCtrlValue(SOLIDS_SG_AVG,str(data.AverageSolidsGravity))

            if elem.HasField('rheology'):
                self.rheology(FluidItem, elem.rheology, elem.Density)


            if len(fluidsEditor.mudDetails) != count:
                helper.ClickOnce(AddFluidButton)
                item = fluidList.ListItemControl(foundIndex=self.rowCount, searchDepth=1, ClassName='ListBoxItem',
                                                 Name='DSWE.Core.Presentation.FluidEditor.PresentationModel.FluidModel')
                helper.ClickOnce(item)
                # 选项的细节
                FluidItem = FluidEditorView.CustomControl(searchDepth=2, ClassName='FluidItem',
                                                          AutomationId='UserControl_1')


    def spacerDetails(self,
                      FluidEditorView: auto.CustomControl,
                      fluidsEditor: FluidsEditor,
                      fluidList: auto.ListControl,
                      AddSpacerButton: auto.ButtonControl):
        for elem in fluidsEditor.spacerDetails:
            helper.ClickOnce(AddSpacerButton)
            item = fluidList.ListItemControl(foundIndex=self.rowCount, searchDepth=1, ClassName='ListBoxItem',
                                             Name='DSWE.Core.Presentation.FluidEditor.PresentationModel.FluidModel')
            helper.ClickOnce(item)
            # 选项的细节
            FluidItem = FluidEditorView.CustomControl(searchDepth=2, ClassName='FluidItem',
                                                      AutomationId='UserControl_1')
            # 名称
            if elem.HasField('Name'):
                FLUID_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_FLUID_FLUID_NAME')
                helper.SetCtrlValue(FLUID_NAME,str(elem.Name))
            # 描述
            if elem.HasField('Desc'):
                COMPANY_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_FLUID_COMPANY_NAME')
                helper.SetCtrlValue(COMPANY_NAME,str(elem.Desc))
            '''
            # 密度
            if elem.HasField('Density'):
                FluidReferenceDensity = FluidItem.CustomControl(searchDepth=1, ClassName='FluidReferenceDensity',
                                                                AutomationId='UserControl_2')
                TEMP_BASE_DENSITY1 = FluidReferenceDensity.EditControl(foundIndex=1, searchDepth=1, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
                helper.SetCtrlValue(TEMP_BASE_DENSITY1,str(elem.Density))
            #TEMP_BASE_DENSITY2 = FluidReferenceDensity.EditControl(foundIndex=2, searchDepth=1, ClassName='TextBox',
            #                                                       AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
            #helper.SetCtrlValue(TEMP_BASE_DENSITY2,str(elem.Density))
            '''
            if elem.HasField('rheology'):
                self.rheology(FluidItem, elem.rheology, elem.Density)

    def cementDetails(self,
                      FluidEditorView: auto.CustomControl,
                      fluidsEditor: FluidsEditor,
                      fluidList: auto.ListControl,
                      AddCementButton: auto.ButtonControl):
        for elem in fluidsEditor.cementDetails:
            if not isinstance(elem, FluidsEditor.CementDetails):
                return
            helper.ClickOnce(AddCementButton)
            item = fluidList.ListItemControl(foundIndex=self.rowCount, searchDepth=1, ClassName='ListBoxItem',
                                             Name='DSWE.Core.Presentation.FluidEditor.PresentationModel.FluidModel')
            helper.ClickOnce(item)
            # 选项的细节
            FluidItem = FluidEditorView.CustomControl(searchDepth=2, ClassName='FluidItem',
                                                      AutomationId='UserControl_1')
            # 名称
            if elem.HasField('Name'):
                FLUID_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_FLUID_FLUID_NAME')
                helper.SetCtrlValue(FLUID_NAME,str(elem.Name))
            # 描述
            if elem.HasField('Desc'):
                COMPANY_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_FLUID_COMPANY_NAME')
                helper.SetCtrlValue(COMPANY_NAME,str(elem.Desc))
            '''
            # 密度
            if elem.HasField('Density'):
                FluidReferenceDensity = FluidItem.CustomControl(searchDepth=1, ClassName='FluidReferenceDensity',
                                                                AutomationId='UserControl_2')
                TEMP_BASE_DENSITY1 = FluidReferenceDensity.EditControl(foundIndex=1, searchDepth=1, ClassName='TextBox',
                                                                       AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
                helper.SetCtrlValue(TEMP_BASE_DENSITY1,str(elem.Density))
            #TEMP_BASE_DENSITY2 = FluidReferenceDensity.EditControl(foundIndex=2, searchDepth=1, ClassName='TextBox',
            #                                                       AutomationId='HorizontalTextBox_WP_FLUID_TEMP_BASE_DENSITY')
            #helper.SetCtrlValue(TEMP_BASE_DENSITY2,str(elem.Density))
            '''
            # 水泥的特性
            if elem.HasField('cementProperties'):
                CementGrp = FluidItem.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                   AutomationId='GroupBox_Cement')
                CementClassComboBox = CementGrp.ComboBoxControl(searchDepth=1, ClassName='ComboBox',
                                                                AutomationId='CementClassComboBox')
                CementClassComboBox.SetFocus()

                # 级 默认为空
                if elem.cementProperties.HasField('clazz'):
                    helper.ComboBoxCtrlRestore(CementClassComboBox)
                    helper.SetCtrlComboBoxValue(CementClassComboBox, elem.cementProperties.clazz)

                # 屈服值
                if elem.cementProperties.HasField('Yield'):
                    YIELD = CementGrp.EditControl(foundIndex=1, searchDepth=1, ClassName='TextBox',
                                                              AutomationId='HorizontalTextBox_CD_FLUID_YIELD')
                    helper.SetCtrlValue(YIELD,str(elem.cementProperties.Yield))
                # 水要求
                if elem.cementProperties.HasField('WaterRequirement'):
                    WATER_REQUIREMENT = CementGrp.EditControl(foundIndex=1, searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_FLUID_WATER_REQUIREMENT')
                    helper.SetCtrlValue(WATER_REQUIREMENT,str(elem.cementProperties.WaterRequirement))
            if elem.HasField('rheology'):
                self.rheology(FluidItem, elem.rheology, elem.Density)

    def gasDetails(self,
                   FluidEditorView: auto.CustomControl,
                   fluidsEditor: FluidsEditor,
                   fluidList: auto.ListControl,
                   AddGasButton: auto.ButtonControl):
        for elem in fluidsEditor.gasDetails:
            if not isinstance(elem, FluidsEditor.GasDetails):
                return

            helper.ClickOnce(AddGasButton)

            item = fluidList.ListItemControl(foundIndex=self.rowCount, searchDepth=1, ClassName='ListBoxItem')
            helper.ClickOnce(item)
            # 选项的细节
            FluidItem = FluidEditorView.CustomControl(searchDepth=2, ClassName='FluidItem',
                                                      AutomationId='UserControl_1')
            # 名称
            if elem.HasField('Name'):
                FLUID_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_FLUID_FLUID_NAME')
                helper.SetCtrlValue(FLUID_NAME,str(elem.Name))
            # 描述
            if elem.HasField('Desc'):
                COMPANY_NAME = FluidItem.EditControl(searchDepth=1, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_FLUID_COMPANY_NAME')
                helper.SetCtrlValue(COMPANY_NAME,str(elem.Desc))
            if elem.HasField('gasProperties'):
                GasProperties = FluidItem.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                       AutomationId='GroupBox_GasProperties')
                gasProperties = elem.gasProperties
                if gasProperties.UserDefined:
                    # 气体的性质 -- 用户定义
                    UserDef = GasProperties.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                               AutomationId='RadioButton_6', Name='用户定义')
                    helper.ClickOnce(UserDef)
                    #UserDef.SendKey(auto.Keys.VK_SPACE)
                    # 摩尔重量
                    if gasProperties.HasField('MoleWeigth'):
                        MOLECULAR_WEIGHT = GasProperties.EditControl(searchDepth=1, foundIndex=2,  ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_WP_FLUID_GAS_PROPERTIES_MOLECULAR_WEIGHT')
                        helper.SetCtrlValue(MOLECULAR_WEIGHT,str(gasProperties.MoleWeigth))
                    # 比热容比
                    if gasProperties.HasField('SpecificHeatRatio'):
                        SPECIFIC_HEAT_RATIO = GasProperties.EditControl(searchDepth=1, foundIndex=2, ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_WP_FLUID_GAS_PROPERTIES_SPECIFIC_HEAT_RATIO')
                        helper.SetCtrlValue(SPECIFIC_HEAT_RATIO,str(gasProperties.SpecificHeatRatio))
                    # 粘度
                    if gasProperties.HasField('Viscosity'):
                        VISCOSITY = GasProperties.EditControl(searchDepth=1,foundIndex=2, ClassName='TextBox',
                                                          AutomationId='HorizontalTextBox_WP_FLUID_GAS_PROPERTIES_VISCOSITY')
                        helper.SetCtrlValue(VISCOSITY,str(gasProperties.Viscosity))
                    # 临界压力 kPa
                    if gasProperties.HasField('CriticalPressure'):
                        CRITICAL_PRESSURE = GasProperties.EditControl(searchDepth=1,foundIndex=2, ClassName='TextBox',
                                                                  AutomationId='HorizontalTextBox_WP_FLUID_GAS_PROPERTIES_CRITICAL_PRESSURE')
                        helper.SetCtrlValue(CRITICAL_PRESSURE,str(gasProperties.CriticalPressure))
                    # 临界压力 摄氏度
                    if gasProperties.HasField('CriticalTemperature'):
                        CRITICAL_TEMPERATURE = GasProperties.EditControl(searchDepth=1,foundIndex=2, ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_FLUID_GAS_PROPERTIES_CRITICAL_TEMPERATURE')
                        helper.SetCtrlValue(CRITICAL_TEMPERATURE,str(gasProperties.CriticalTemperature))
                    # 气体特别重力
                    if gasProperties.HasField('Gas_SpecificGravity'):
                        GAS_SPECIFIC_GRAVITY = GasProperties.EditControl(searchDepth=1,foundIndex=2, ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_FLUID_GAS_PROPERTIES_GAS_SPECIFIC_GRAVITY')
                        helper.SetCtrlValue(GAS_SPECIFIC_GRAVITY,str(gasProperties.Gas_SpecificGravity))
                else:
                    # 气体的性质 -- 从目录中选择
                    # 从目录中选择
                    ContentSel = GasProperties.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                  AutomationId='RadioButton_5', Name='从目录中选择')
                    helper.ClickOnce(ContentSel)
                    # 从目录中选取
                    #GasCatalogBtn = GasProperties.ButtonControl(searchDepth=1, ClassName='Button',
                    #                                            AutomationId='GasCatalog')
                    #GasCatalogBtn.SetFocus()
                    #GasCatalogBtn.SendKey(auto.Keys.VK_SPACE)

                    # 气体目录操作
                    GasContent = self.cxt.TopWindow.WindowControl(searchDepth=1, ClassName='Window',
                                                                  AutomationId='Window_1', Name='气体目录')
                    GasListGrid = GasContent.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                             AutomationId='GasListGrid')
                    GasEditorGrid = GasContent.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                               AutomationId='GasEditorGrid')
                    OKBtn = GasContent.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='Button_3', Name='OK')

                    gasContainer = {}
                    gasListContainer = []
                    for item in gasProperties.Components:
                        if not isinstance(item, FluidsEditor.GasDetails.GasProperties.GasComponent):
                            return
                        gasContainer[int(item.gas)] = item.MixturePercentage

                    countStep = 0
                    for item, depth in auto.WalkControl(GasListGrid, maxDepth=1):
                        if isinstance(item, auto.DataItemControl):
                            item.GetScrollItemPattern().ScrollIntoView(waitTime=0.1)
                            val = gasContainer.get(countStep, None)
                            if val is not None:
                                helper.ClickOnce(item)
                                item.DoubleClick()
                                gasListContainer.append(val)
                            countStep += 1

                    for item, depth in auto.WalkControl(GasEditorGrid):
                        if isinstance(item, auto.DataItemControl):
                            item.GetScrollItemPattern().ScrollIntoView(waitTime=0.1)
                            # item.GetSelectionItemPattern().Select(waitTime=0.1)
                            item.DoubleClick(ratioX=0.8)
                            auto.SendKeys(str(gasListContainer.pop(0)))
                    GasContent.Click()
                    helper.ClickOnce(OKBtn)

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化流体信息")

        FluidTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='FluidTab')
        helper.ClickOnce(FluidTab)
        FluidEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                    ClassName='FluidEditorView',
                                                                    AutomationId='FluidEditorView')

        FluidList_1 = FluidEditorView.CustomControl(searchDepth=2, ClassName='FluidList',
                                                    AutomationId='ThisControls:FluidList_1')
        fluidGrp = FluidList_1.GroupControl(searchDepth=1, ClassName='Expander',
                                            AutomationId='FluidListExpander')
        fluidBtn = fluidGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                          AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, fluidBtn)

        fluidList = fluidGrp.ListControl(searchDepth=1, ClassName='ListBox', AutomationId='ListBox_1')
        #尝试进行清空
        while True:
            removeBtn = None
            for item, depth in auto.WalkControl(fluidList, maxDepth=1):
                if isinstance(item, auto.ListItemControl):
                    item.GetScrollItemPattern().ScrollIntoView(waitTime=0.1)
                    removeBtn = item.ButtonControl(searchDepth=1, ClassName='Button')
                    if bool(removeBtn.IsEnabled):
                        helper.ClickOnce(removeBtn)
            if removeBtn is None:
                break
            if removeBtn and bool(removeBtn.IsEnabled) is False:
                break

        # 控件是总插入头部也就是首部
        # 选择一个Item，默认总有一个泥浆#1
        item = fluidList.ListItemControl(foundIndex=self.rowCount, searchDepth=1, ClassName='ListBoxItem')
        helper.ClickOnce(item)

        # 添加新泥浆
        AddFluidButton = fluidBtn.ButtonControl(searchDepth=1, ClassName='Button',
                                                AutomationId='HoleSectionEditorDisplayAddFluidButton')
        self.mudDetails(FluidEditorView, self.fluidsEditor, fluidList, AddFluidButton)

        # 添加新离液
        AddSpacerButton = fluidBtn.ButtonControl(searchDepth=1, ClassName='Button',
                                                 AutomationId='HoleSectionEditorDisplayAddSpacerButton')
        self.spacerDetails(FluidEditorView, self.fluidsEditor, fluidList, AddSpacerButton)

        # 添加新水泥
        AddCementButton = fluidBtn.ButtonControl(searchDepth=1, ClassName='Button',
                                                 AutomationId='HoleSectionEditorDisplayAddCementButton')
        self.cementDetails(FluidEditorView, self.fluidsEditor, fluidList, AddCementButton)

        # 添加新气体
        AddGasButton = fluidBtn.ButtonControl(searchDepth=1, ClassName='Button',
                                              AutomationId='FluidEditorDisplayAddGasButton')
        self.gasDetails(FluidEditorView, self.fluidsEditor, fluidList, AddGasButton)
        if self.isConnected():
            listener.sendStatus(self.conn, "流体信息初始化完毕")
