# -*- coding: utf-8 -*-
import helper
import pyperclip
from protocol.wellplan_pb2 import StringEditor
from launcher import *
from network import listener

class StringController:
    cxt = Context()
    stringEditor = StringEditor()
    conn: WebSocket = None

    def __init__(self, cxt: Context, stringEditor: StringEditor, conn: WebSocket = None):
        self.cxt = cxt
        self.stringEditor = stringEditor
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化管柱信息")

        stringTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='StringTab')
        helper.ClickOnce(stringTab)

        MainStringEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                ClassName='MainStringEditorView',
                                                                AutomationId='MainStringEditorTabControl')
        MainStringEditorTabControl = MainStringEditorView.TabControl(searchDepth=1, ClassName='TabControl',
                                                                     AutomationId='MainStringEditorTabControl')

        self.workString(MainStringEditorTabControl, self.stringEditor)
        self.standoffDevices(MainStringEditorTabControl, self.stringEditor)
        self.innerString(MainStringEditorTabControl, self.stringEditor)

        if self.isConnected():
            listener.sendStatus(self.conn, "管柱信息初始化完毕")

    def stringGeneralHelper(self, WorkStringTab, general: StringEditor.ItemDetails.General):
        # 展开通用
        UnGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1', Name='通用')
        UnGrp.SetFocus()
        UnBtn = UnGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite', Name='通用')
        helper.AutoToggleStateClick(True, UnBtn)

        if general.HasField('manufacturer'):
            # 生产商
            PART_EditableTextBox = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                     AutomationId='PART_EditableTextBox')
            helper.ComboBoxCtrlRestore(PART_EditableTextBox)
            helper.SetCtrlComboBoxValue(PART_EditableTextBox, general.manufacturer)
        # 型号
        if general.HasField('ModelNumber'):
            ASSEMBLY_COMP_MODEL = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MODEL')
            helper.SetCtrlValue(ASSEMBLY_COMP_MODEL, general.ModelNumber)
        # 长度
        if general.HasField('Length'):
            ASSEMBLY_COMP_LENGTH = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH')
            if not ASSEMBLY_COMP_LENGTH.GetValuePattern().IsReadOnly:
                helper.SetCtrlValue(ASSEMBLY_COMP_LENGTH, str(general.Length))
        # 内径
        if general.HasField('BodyOD'):
            ASSEMBLY_COMP_OD_BODY = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_OD_BODY')
            helper.SetCtrlValue(ASSEMBLY_COMP_OD_BODY, str(general.BodyOD))
        # 封闭终端排代量
        if general.HasField('ClosedEndDisplacement'):
            DISPLACEMENT = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CLOSED_END_DISPLACEMENT')
            helper.SetCtrlValue(DISPLACEMENT, str(general.ClosedEndDisplacement))
        # 体内径
        if general.HasField('BodyID'):
            ASSEMBLY_COMP_ID_BODY = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ID_BODY')
            helper.SetCtrlValue(ASSEMBLY_COMP_ID_BODY, str(general.BodyID))
        # 线性容积
        if general.HasField('LinearCapacity'):
            LINEAR_CAPACITY = UnGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LINEAR_CAPACITY')
            helper.SetCtrlValue(LINEAR_CAPACITY, str(general.LinearCapacity))

    def stringMechanicalHelper(self, WorkStringTab, mechanical: StringEditor.ItemDetails.Mechanical):
        # 展开机械
        machineGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                                Name='机械')
        machineGrp.SetFocus()
        machineBtn = machineGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                              Name='机械')
        helper.AutoToggleStateClick(True, machineBtn)

        # 毛量
        if mechanical.HasField('ApproximateWeight'):
            APPROXIMATE_WEIGHT = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_APPROXIMATE_WEIGHT')
            helper.SetCtrlValue(APPROXIMATE_WEIGHT, str(mechanical.ApproximateWeight))
        # 级
        if mechanical.HasField('grade'):
            Lvl = machineGrp.ComboBoxControl(searchDepth=4, ClassName='ComboBox', foundIndex=1)
            helper.ComboBoxCtrlRestore(Lvl)
            helper.SetCtrlComboBoxValue(Lvl, mechanical.grade)

        # 最小屈服强度
        if mechanical.HasField('MinimumYieldStrength'):
            MIN_YIELD_STRESS = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MIN_YIELD_STRESS')
            helper.SetCtrlValue(MIN_YIELD_STRESS, str(mechanical.MinimumYieldStrength))

        # 材质
        if mechanical.HasField('material'):
            texture = machineGrp.ComboBoxControl(searchDepth=4, ClassName='ComboBox', foundIndex=2)
            helper.ComboBoxCtrlRestore(texture)
            helper.SetCtrlComboBoxValue(texture, mechanical.material)

        # 抗外挤强度
        if mechanical.HasField('CollapseResistance'):
            PRESSURE_COLLAPSE = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PRESSURE_COLLAPSE')
            helper.SetCtrlValue(PRESSURE_COLLAPSE, str(mechanical.CollapseResistance))

        # 杨氏模型
        if mechanical.HasField('YoungsMoudulus'):
            YOUNGS_MODULUS = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_YOUNGS_MODULUS')
            helper.SetCtrlValue(YOUNGS_MODULUS, str(mechanical.YoungsMoudulus))

        # 泊松比
        if mechanical.HasField('PoissonsRatio'):
            POISSONS_RATIO = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_POISSONS_RATIO')
            helper.SetCtrlValue(POISSONS_RATIO, str(mechanical.PoissonsRatio))
        # 密度
        if mechanical.HasField('Density'):
            DENSITY = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_DENSITY')
            helper.SetCtrlValue(DENSITY, str(mechanical.Density))
        # 热膨胀系数
        if mechanical.HasField('CoeffOfThermalExp'):
            THERMAL_EXPANSION_COEF = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_THERMAL_EXPANSION_COEF')
            helper.SetCtrlValue(THERMAL_EXPANSION_COEF, str(mechanical.CoeffOfThermalExp))
        # 连接
        if mechanical.HasField('Connection'):
            CONNECTION_NAME = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CONNECTION_NAME')
            helper.SetCtrlValue(CONNECTION_NAME, str(mechanical.Connection))
        # 补充扭矩
        if mechanical.HasField('MakeupTorque'):
            MAKEUP_TORQUE = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MAKEUP_TORQUE')
            helper.SetCtrlValue(MAKEUP_TORQUE, str(mechanical.MakeupTorque))

    def stringBitDataHelper(self, WorkStringTab, bitData: StringEditor.ItemDetails.BitDetailData.BitData):
        BitGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1', Name='钻头数据')
        BitBtn = BitGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite', Name='钻头数据')
        helper.AutoToggleStateClick(True, BitBtn)
        # 生产商
        if bitData.HasField('manufacturer'):
            PART_EditableTextBox = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='PART_EditableTextBox')
            # 生产商归为最顶
            helper.ComboBoxCtrlRestore(PART_EditableTextBox)
            helper.SetCtrlComboBoxValue(PART_EditableTextBox, bitData.manufacturer)

        # 型号
        if bitData.HasField('ModelNumber'):
            ASSEMBLY_COMP_MODEL = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MODEL')
            helper.SetCtrlValue(ASSEMBLY_COMP_MODEL, bitData.ModelNumber)
        # 长度
        if bitData.HasField('Length'):
            ASSEMBLY_COMP_LENGTH = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH')
            if not ASSEMBLY_COMP_LENGTH.GetValuePattern().IsReadOnly:
                helper.SetCtrlValue(ASSEMBLY_COMP_LENGTH, str(bitData.Length))
        # 毛重
        if bitData.HasField('ApproximateWeight'):
            APPROXIMATE_WEIGHT = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_APPROXIMATE_WEIGHT')
            helper.SetCtrlValue(APPROXIMATE_WEIGHT, str(bitData.ApproximateWeight))
        # 钻头尺寸
        if bitData.HasField('Bit_Drill_Diameter'):
            OD_BODY = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                         AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_OD_BODY')
            helper.SetCtrlValue(OD_BODY, str(bitData.Bit_Drill_Diameter))
        # 柄长度
        if bitData.HasField('ShankLength'):
            FISHNECK_LENGTH = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(bitData.ShankLength))
        # 柄外径
        if bitData.HasField('ShankOD'):
            FISHNECK_OD = BitGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_OD')
            helper.SetCtrlValue(FISHNECK_OD, str(bitData.ShankOD))

    def stringNozzleSizesHelper(self, WorkStringTab,
                                nozzleSize: StringEditor.ItemDetails.BitDetailData.NozzleSizes):
        nozzleSizeGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                                   Name='喷嘴的尺寸')
        nozzleSizeBtn = nozzleSizeGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                                    Name='喷嘴的尺寸')
        helper.AutoToggleStateClick(True, nozzleSizeBtn)

        # % 喷嘴塞面积
        if nozzleSize.HasField('NozzleAreaPlugged'):
            PERCENT_PLUGGED = nozzleSizeGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                        AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PERCENT_PLUGGED')
            helper.SetCtrlValue(PERCENT_PLUGGED, str(nozzleSize.NozzleAreaPlugged))
        # 总流面积
        if nozzleSize.HasField('TotalFlowArea'):
            TFA = nozzleSizeGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_TFA')
            helper.SetCtrlValue(TFA, str(nozzleSize.TotalFlowArea))
        # 表格项
        DataGrid = nozzleSizeGrp.DataGridControl(searchDepth=2, ClassName='HalWPFGrid',
                                                 AutomationId='dg:DataGrid_1')
        helper.ClearDataGrid(DataGrid)
        if len(nozzleSize.items) > 0:
            tableData = ''
            for elem in nozzleSize.items:
                row = '{}	{}\r\n'.format(elem.Count, elem.Size)
                tableData += row
            helper.WriteDataToDataGrid(DataGrid, tableData)

    def stringCasingHelper(self, WorkStringTab, casing: StringEditor.ItemDetails.CasingDetailData.Casing):
        casingGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                               Name='套管')
        casingBtn = casingGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                            Name='套管')
        helper.AutoToggleStateClick(True, casingBtn)

        # 耦合外径
        if casing.HasField('CouplingOD'):
            OD_CONNECTION = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                  AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_OD_CONNECTION')
            helper.SetCtrlValue(OD_CONNECTION, str(casing.CouplingOD))
        # 大于耦合长度
        if casing.HasField('OutsideCouplingLength'):
            LENGTH_OUTSIDE_COUPLING = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH_OUTSIDE_COUPLING')
            helper.SetCtrlValue(LENGTH_OUTSIDE_COUPLING, str(casing.OutsideCouplingLength))
        # 耦合内径
        if casing.HasField('CouplingID'):
            ID_CONNECTION = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                  AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ID_CONNECTION')
            helper.SetCtrlValue(ID_CONNECTION, str(casing.CouplingID))
        # 在耦合长度内
        if casing.HasField('InsideCouplingLength'):
            LENGTH_INSIDE_COUPLING = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                           AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH_INSIDE_COUPLING')
            helper.SetCtrlValue(LENGTH_INSIDE_COUPLING, str(casing.InsideCouplingLength))
        # 平均接头长度
        if casing.HasField('AverageJointLength'):
            AVERAGE_JOINT_LENGTH = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                         AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_AVERAGE_JOINT_LENGTH')
            helper.SetCtrlValue(AVERAGE_JOINT_LENGTH, str(casing.AverageJointLength))
        # 体屈服强度
        if casing.HasField('BodyYieldStrength'):
            YIELD_WEIGHT_BODY = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_YIELD_WEIGHT_BODY')
            helper.SetCtrlValue(YIELD_WEIGHT_BODY, str(casing.BodyYieldStrength))
        # 接口强度
        if casing.HasField('JointStrength'):
            JOINT_STRENGTH = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_JOINT_STRENGTH')
            helper.SetCtrlValue(JOINT_STRENGTH, str(casing.JointStrength))
        # 内屈服压力
        if casing.HasField('InternalYieldPressure'):
            PRESSURE_BURST = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PRESSURE_BURST')
            helper.SetCtrlValue(PRESSURE_BURST, str(casing.InternalYieldPressure))
        # 漂移内径
        if casing.HasField('DriftID'):
            ID_DRIFT = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ID_DRIFT')
            helper.SetCtrlValue(ID_DRIFT, str(casing.DriftID))
        # 公称重量
        if casing.HasField('NominalWeight'):
            NOMINAL_WEIGHT = casingGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                   AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_NOMINAL_WEIGHT')
            helper.SetCtrlValue(NOMINAL_WEIGHT, str(casing.NominalWeight))

    def stringCasingShoeFloatOptionHelper(self, WorkStringTab,
                                          floatOption: StringEditor.ItemDetails.CasingShoeDetailData.FloatOption):
        casingShoeGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                                   Name='浮动选项（下钻）')
        casingShoeBtn = casingShoeGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                                    Name='浮动选项（下钻）')
        helper.AutoToggleStateClick(True, casingShoeBtn)

        # 流体流动模块
        if floatOption.HasField('mode'):
            FlowModeCombo = casingShoeGrp.ComboBoxControl(searchDepth=4, ClassName='ComboBox', foundIndex=1)
            helper.ComboBoxCtrlRestore(FlowModeCombo)
            helper.SetCtrlComboBoxValue(FlowModeCombo, floatOption.mode)

        # 打开的横截面百分比
        if floatOption.HasField('PercentAreaOpen'):
            PERC_AREA_OPEN = casingShoeGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                       AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PERC_AREA_OPEN')
            helper.SetCtrlValue(PERC_AREA_OPEN, str(floatOption.PercentAreaOpen))
        # 浮动内径
        if floatOption.HasField('FloatID'):
            FLOAT_ID = casingShoeGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FLOAT_ID')
            helper.SetCtrlValue(FLOAT_ID, str(floatOption.FloatID))
        # 总流体面积
        if floatOption.HasField('TotalFlowArea'):
            TFA = casingShoeGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_TFA')
            helper.SetCtrlValue(TFA, str(floatOption.TotalFlowArea))

    def stringDrillCollarHelper(self, WorkStringTab,
                                drillCollar: StringEditor.ItemDetails.DrillCollarDetailData.DrillCollar):
        drillCollarGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                                    Name='钻铤')
        drillCollarBtn = drillCollarGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                                      Name='钻铤')
        helper.AutoToggleStateClick(True, drillCollarBtn)

        # 平均接头长度
        if drillCollar.HasField('AverageJointLength'):
            AVERAGE_JOINT_LENGTH = drillCollarGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                              AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_AVERAGE_JOINT_LENGTH')
            helper.SetCtrlValue(AVERAGE_JOINT_LENGTH, str(drillCollar.AverageJointLength))

    def stringDrillPipeStringHelper(self, WorkStringTab,
                                    drillPipeString: StringEditor.ItemDetails.DrillPipeDetailData.String):
        drillPipeGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                                  Name='管柱')
        drillPipeBtn = drillPipeGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                                  Name='管柱')
        helper.AutoToggleStateClick(True, drillPipeBtn)

        SingleCategoryPropertyPageControl = drillPipeGrp.CustomControl(searchDepth=1,
                                                                       ClassName='SingleCategoryPropertyPageControl',
                                                                       AutomationId='UserControl_1')
        # 服务等级
        if drillPipeString.HasField('serviceClass'):
            serviceLvl = SingleCategoryPropertyPageControl.ComboBoxControl(searchDepth=1, ClassName='ComboBox')
            helper.ComboBoxCtrlRestore(serviceLvl)
            helper.SetCtrlComboBoxValue(serviceLvl, drillPipeString.serviceClass)
        # 壁厚
        if drillPipeString.HasField('WallTickness'):
            WALL_THICKNESS_PERCENT = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                   AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_WALL_THICKNESS_PERCENT')
            helper.SetCtrlValue(WALL_THICKNESS_PERCENT, str(drillPipeString.WallTickness))
        # 接口外径
        if drillPipeString.HasField('ConnectionOD'):
            OD_CONNECTION = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_OD_CONNECTION')
            helper.SetCtrlValue(OD_CONNECTION, str(drillPipeString.ConnectionOD))
        # 连接内径
        if drillPipeString.HasField('ConnectionID'):
            ID_CONNECTION = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ID_CONNECTION')
            helper.SetCtrlValue(ID_CONNECTION, str(drillPipeString.ConnectionID))
        # 平均接头长度
        if drillPipeString.HasField('AverageJointLength'):
            AVERAGE_JOINT_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_AVERAGE_JOINT_LENGTH')
            helper.SetCtrlValue(AVERAGE_JOINT_LENGTH, str(drillPipeString.AverageJointLength))
        # 钻柱接口长度
        if drillPipeString.HasField('TollJointLength'):
            LENGTH_TOOL_JOINT = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                              AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH_TOOL_JOINT')
            helper.SetCtrlValue(LENGTH_TOOL_JOINT, str(drillPipeString.TollJointLength))
        # 接口扭转阻尼
        if drillPipeString.HasField('ConnectionTorsionalYield'):
            CONNECTION_TORSIONAL_YIELD = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                       ClassName='TextBox',
                                                                                       AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CONNECTION_TORSIONAL_YIELD')
            helper.SetCtrlValue(CONNECTION_TORSIONAL_YIELD, str(drillPipeString.ConnectionTorsionalYield))
        # 拉伸极限
        if drillPipeString.HasField('UltimateTensileStrength'):
            ULTIMATE_TENSILE_STRENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                      ClassName='TextBox',
                                                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ULTIMATE_TENSILE_STRENGTH')
            helper.SetCtrlValue(ULTIMATE_TENSILE_STRENGTH, str(drillPipeString.UltimateTensileStrength))
        # 搞疲劳极限
        if drillPipeString.HasField('FatigueEnduranceLimit'):
            FATIGUE_ENDURANCE_LIMIT = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FATIGUE_ENDURANCE_LIMIT')
            helper.SetCtrlValue(FATIGUE_ENDURANCE_LIMIT, str(drillPipeString.FatigueEnduranceLimit))

    def stringEccentricStabilizerHelper(self, WorkStringTab,
                                        eccentricStabilizer: StringEditor.ItemDetails.EccentricStabilizerDetailData.EccemtrocStabilizer):
        eccentricStabilizerGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                                            AutomationId='Expander1',
                                                            Name='偏心扶正器')
        eccentricStabilizerBtn = eccentricStabilizerGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                      AutomationId='HeaderSite',
                                                                      Name='偏心扶正器')
        helper.AutoToggleStateClick(True, eccentricStabilizerBtn)
        SingleCategoryPropertyPageControl = eccentricStabilizerGrp.CustomControl(searchDepth=1,
                                                                                 ClassName='SingleCategoryPropertyPageControl',
                                                                                 AutomationId='UserControl_1')
        # 扶正器的长度
        if eccentricStabilizer.HasField('BladeLength'):
            ECCSTAB_STAB_BLADE_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                      ClassName='TextBox',
                                                                                      AutomationId='HorizontalTextBox_CD_BHA_COMP_ECCSTAB_STAB_BLADE_LENGTH')
            helper.SetCtrlValue(ECCSTAB_STAB_BLADE_LENGTH, str(eccentricStabilizer.BladeLength))
        # 打捞颈长度
        if eccentricStabilizer.HasField('FishneckLength'):
            FISHNECK_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(eccentricStabilizer.FishneckLength))
        # 稳定器叶片外径1
        if eccentricStabilizer.HasField('BladeOD1'):
            ECCSTAB_STAB_BLADE_OD_1 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                    AutomationId='HorizontalTextBox_CD_BHA_COMP_ECCSTAB_STAB_BLADE_OD_1')
            helper.SetCtrlValue(ECCSTAB_STAB_BLADE_OD_1, str(eccentricStabilizer.BladeOD1))
        # 稳定器叶片外径2
        if eccentricStabilizer.HasField('BladeOD2'):
            ECCSTAB_STAB_BLADE_OD_2 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                    AutomationId='HorizontalTextBox_CD_BHA_COMP_ECCSTAB_STAB_BLADE_OD_2')
            helper.SetCtrlValue(ECCSTAB_STAB_BLADE_OD_2, str(eccentricStabilizer.BladeOD2))
        # 稳定器叶片外径3
        if eccentricStabilizer.HasField('BladeOD3'):
            ECCSTAB_STAB_BLADE_OD_3 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                    AutomationId='HorizontalTextBox_CD_BHA_COMP_ECCSTAB_STAB_BLADE_OD_3')
            helper.SetCtrlValue(ECCSTAB_STAB_BLADE_OD_3, str(eccentricStabilizer.BladeOD3))
        # 稳定器叶片外径4
        if eccentricStabilizer.HasField('BladeOD4'):
            ECCSTAB_STAB_BLADE_OD_3 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                    AutomationId='HorizontalTextBox_CD_BHA_COMP_ECCSTAB_STAB_BLADE_OD_4')
            helper.SetCtrlValue(ECCSTAB_STAB_BLADE_OD_3, str(eccentricStabilizer.BladeOD4))

    def stringHeavyWeightHelper(self, WorkStringTab,
                                heavyWeight: StringEditor.ItemDetails.HeavyWeightDetailData.HeavyWeight):
        heavyWeighGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                                   AutomationId='Expander1',
                                                   Name='重质')
        heavyWeighBtn = heavyWeighGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                    AutomationId='HeaderSite',
                                                    Name='重质')
        helper.AutoToggleStateClick(True, heavyWeighBtn)

        SingleCategoryPropertyPageControl = heavyWeighGrp.CustomControl(searchDepth=1,
                                                                        ClassName='SingleCategoryPropertyPageControl',
                                                                        AutomationId='UserControl_1')
        # 接口外径
        if heavyWeight.HasField('ConnectionOD'):
            OD_CONNECTION = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_OD_CONNECTION')
            helper.SetCtrlValue(OD_CONNECTION, str(heavyWeight.ConnectionOD))
        # 连接内径
        if heavyWeight.HasField('ConnectionID'):
            ID_CONNECTION = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ID_CONNECTION')
            helper.SetCtrlValue(ID_CONNECTION, str(heavyWeight.ConnectionID))
        # 平均接头长度
        if heavyWeight.HasField('AverageJointLength'):
            AVERAGE_JOINT_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_AVERAGE_JOINT_LENGTH')
            helper.SetCtrlValue(AVERAGE_JOINT_LENGTH, str(heavyWeight.AverageJointLength))
        # 钻柱接口长度
        if heavyWeight.HasField('ToolJointLength'):
            LENGTH_TOOL_JOINT = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                              AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH_TOOL_JOINT')
            helper.SetCtrlValue(LENGTH_TOOL_JOINT, str(heavyWeight.ToolJointLength))
        # 拉伸极限
        if heavyWeight.HasField('UltimateTensileStrength'):
            ULTIMATE_TENSILE_STRENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                      ClassName='TextBox',
                                                                                      AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ULTIMATE_TENSILE_STRENGTH')
            helper.SetCtrlValue(ULTIMATE_TENSILE_STRENGTH, str(heavyWeight.UltimateTensileStrength))
        # 抗疲劳极限
        if heavyWeight.HasField('FatigueEnduranceLimit'):
            FATIGUE_ENDURANCE_LIMIT = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FATIGUE_ENDURANCE_LIMIT')
            helper.SetCtrlValue(FATIGUE_ENDURANCE_LIMIT, str(heavyWeight.FatigueEnduranceLimit))

    def stringHoleOpenerHelper(self, WorkStringTab,
                               holeOpener: StringEditor.ItemDetails.HoleOpenerDetailData.HoleOpener):
        holeOpenerGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                                   AutomationId='Expander1',
                                                   Name='扩井眼')
        holeOpenerBtn = holeOpenerGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                    AutomationId='HeaderSite',
                                                    Name='扩井眼')
        helper.AutoToggleStateClick(True, holeOpenerBtn)

        SingleCategoryPropertyPageControl = holeOpenerGrp.CustomControl(searchDepth=1,
                                                                        ClassName='SingleCategoryPropertyPageControl',
                                                                        AutomationId='UserControl_1')
        # 最大扩井眼
        if holeOpener.HasField('HoleOpenerMax'):
            MAX_HOLE_SIZE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MAX_HOLE_SIZE')
            helper.SetCtrlValue(MAX_HOLE_SIZE, str(holeOpener.HoleOpenerMax))
        # 接触长度
        if holeOpener.HasField('ContactLength'):
            CONTACT_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CONTACT_LENGTH')
            helper.SetCtrlValue(CONTACT_LENGTH, str(holeOpener.ContactLength))
        # 打捞颈长度
        if holeOpener.HasField('FishneckLength'):
            FISHNECK_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(holeOpener.FishneckLength))

        # 默认为勾住
        # 为False时
        S1CheckBox = SingleCategoryPropertyPageControl.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                       Name='从部件中偏移')
        helper.AutoToggleStateClick(holeOpener.DivertedThroughComponent, S1CheckBox)
        if not holeOpener.DivertedThroughComponent:
            DataGrid = SingleCategoryPropertyPageControl.DataGridControl(searchDepth=2, ClassName='HalWPFGrid',
                                                      AutomationId='dg:DataGrid_1')
            helper.ClearDataGrid(DataGrid)

            if len(holeOpener.Items) > 0:
                # 表格
                tableData = ''
                for elem in holeOpener.Items:
                    rowData = '{}	{}\r\n'.format(elem.Count, elem.Size)
                    tableData += rowData
                helper.WriteDataToDataGrid(DataGrid, tableData)

            # % 喷嘴塞面积
            if holeOpener.HasField('NozzleAreaPlugged'):
                PERCENT_PLUGGED = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PERCENT_PLUGGED')
                helper.SetCtrlValue(PERCENT_PLUGGED, str(holeOpener.NozzleAreaPlugged))
            # 总流面积
            if holeOpener.HasField('TotalFlowArea'):
                TFA = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_TFA')
                helper.SetCtrlValue(TFA, str(holeOpener.TotalFlowArea))
        else:
            # 余量
            if holeOpener.HasField('AmountDiverted'):
                BITFLOW_RATE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_BITFLOW_RATE')
                helper.SetCtrlValue(BITFLOW_RATE, str(holeOpener.AmountDiverted))

    def stringJarHelper(self, WorkStringTab, jar: StringEditor.ItemDetails.JarDetailData.Jar):
        jarGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                            AutomationId='Expander1',
                                            Name='震击器')
        jarBtn = jarGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                      AutomationId='HeaderSite',
                                      Name='震击器')
        helper.AutoToggleStateClick(True, jarBtn)
        SingleCategoryPropertyPageControl = jarGrp.CustomControl(searchDepth=1,
                                                                 ClassName='SingleCategoryPropertyPageControl',
                                                                 AutomationId='UserControl_1')
        # 向上设定力
        if jar.HasField('UpSetForce'):
            UP_SET_FORCE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                         AutomationId='HorizontalTextBox_CD_BHA_COMP_JAR_UP_SET_FORCE')
            helper.SetCtrlValue(UP_SET_FORCE, str(jar.UpSetForce))
        # 向下设定力
        if jar.HasField('DownSetForce'):
            DOWN_SET_FORCE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_BHA_COMP_JAR_DOWN_SET_FORCE')
            helper.SetCtrlValue(DOWN_SET_FORCE, str(jar.DownSetForce))
        # 起钻力
        if jar.HasField('UpTripForce'):
            UP_TRIP_FORCE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_BHA_COMP_JAR_UP_TRIP_FORCE')
            helper.SetCtrlValue(UP_TRIP_FORCE, str(jar.UpTripForce))
        # 下钻力
        if jar.HasField('DownTripForce'):
            DOWN_TRIP_FORCE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_BHA_COMP_JAR_DOWN_TRIP_FORCE')
            helper.SetCtrlValue(DOWN_TRIP_FORCE, str(jar.DownTripForce))
        # 泵开放力
        if jar.HasField('PumpOpenForce'):
            PUMP_OPEN_FORCE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_BHA_COMP_JAR_PUMP_OPEN_FORCE')
            helper.SetCtrlValue(PUMP_OPEN_FORCE, str(jar.PumpOpenForce))
        # 摩擦力
        if jar.HasField('SealFrictionForce'):
            FRICTION_SEAL_FORCE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                                AutomationId='HorizontalTextBox_CD_BHA_COMP_JAR_FRICTION_SEAL_FORCE')
            helper.SetCtrlValue(FRICTION_SEAL_FORCE, str(jar.SealFrictionForce))

    def stringMudMotorHelper(self, WorkStringTab, mudMotor: StringEditor.ItemDetails.MudMotorDetailData.MudMotor):
        mudMotorGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                                 AutomationId='Expander1',
                                                 Name='泥浆泵')
        mudMotorBtn = mudMotorGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                AutomationId='HeaderSite',
                                                Name='泥浆泵')
        helper.AutoToggleStateClick(True, mudMotorBtn)

        SingleCategoryPropertyPageControl = mudMotorGrp.CustomControl(searchDepth=1,
                                                                      ClassName='SingleCategoryPropertyPageControl',
                                                                      AutomationId='UserControl_1')
        # 导航仪的弯角
        if mudMotor.HasField('SteeringToolBendAngle'):
            MOTOR_STEERING_TOOL_BEND_ANGLE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                           ClassName='TextBox',
                                                                                           AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_STEERING_TOOL_BEND_ANGLE')
            helper.SetCtrlValue(MOTOR_STEERING_TOOL_BEND_ANGLE, str(mudMotor.SteeringToolBendAngle))
        # 溢流垫长度
        if mudMotor.HasField('KickPadLength'):
            MOTOR_KICK_PAD_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                  ClassName='TextBox',
                                                                                  AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_KICK_PAD_LENGTH')
            helper.SetCtrlValue(MOTOR_KICK_PAD_LENGTH, str(mudMotor.KickPadLength))
        # 导向工具参考角
        if mudMotor.HasField('StreeringToolRefAngle'):
            MOTOR_STEERING_TOOL_REF_ANGLE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                          ClassName='TextBox',
                                                                                          AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_STEERING_TOOL_REF_ANGLE')
            helper.SetCtrlValue(MOTOR_STEERING_TOOL_REF_ANGLE, str(mudMotor.StreeringToolRefAngle))
        # 溢流垫外径
        if mudMotor.HasField('KickPadOD'):
            MOTOR_KICK_PAD_OD = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                              ClassName='TextBox',
                                                                              AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_KICK_PAD_OD')
            helper.SetCtrlValue(MOTOR_KICK_PAD_OD, str(mudMotor.KickPadOD))
        # 导向工具
        if mudMotor.HasField('SteeringToolOffset'):
            MOTOR_STEERING_TOOL_OFFSET = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                       ClassName='TextBox',
                                                                                       AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_STEERING_TOOL_OFFSET')
            helper.SetCtrlValue(MOTOR_STEERING_TOOL_OFFSET, str(mudMotor.SteeringToolOffset))
        # 溢流垫偏移
        if mudMotor.HasField('KickPadOffset'):
            MOTOR_KICK_PAD_OFFSET = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                  ClassName='TextBox',
                                                                                  AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_KICK_PAD_OFFSET')
            helper.SetCtrlValue(MOTOR_KICK_PAD_OFFSET, str(mudMotor.KickPadOffset))
        # 排量1
        if mudMotor.HasField('FlowRate1'):
            MOTOR_FLOWRATE_1 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_FLOWRATE_1')
            helper.SetCtrlValue(MOTOR_FLOWRATE_1, str(mudMotor.FlowRate1))
        # 压力损失1
        if mudMotor.HasField('PressureLoss1'):
            MOTOR_PRESS_LOSS_1 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                               ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_PRESS_LOSS_1')
            helper.SetCtrlValue(MOTOR_PRESS_LOSS_1, str(mudMotor.PressureLoss1))
        # 排量2
        if mudMotor.HasField('FlowRate2'):
            MOTOR_FLOWRATE_2 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_FLOWRATE_2')
            helper.SetCtrlValue(MOTOR_FLOWRATE_2, str(mudMotor.FlowRate2))
        # 压力损失2
        if mudMotor.HasField('PressureLoss2'):
            MOTOR_PRESS_LOSS_2 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                               ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_PRESS_LOSS_2')
            helper.SetCtrlValue(MOTOR_PRESS_LOSS_2, str(mudMotor.PressureLoss2))
        # 排量3
        if mudMotor.HasField('FlowRate3'):
            MOTOR_FLOWRATE_3 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_FLOWRATE_3')
            helper.SetCtrlValue(MOTOR_FLOWRATE_3, str(mudMotor.FlowRate3))
        # 压力损失3
        if mudMotor.HasField('PressureLoss3'):
            MOTOR_PRESS_LOSS_3 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                               ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_PRESS_LOSS_3')
            helper.SetCtrlValue(MOTOR_PRESS_LOSS_3, str(mudMotor.PressureLoss3))
        # 排量4
        if mudMotor.HasField('FlowRate4'):
            MOTOR_FLOWRATE_4 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_FLOWRATE_4')
            helper.SetCtrlValue(MOTOR_FLOWRATE_4, str(mudMotor.FlowRate4))
        # 压力损失4
        if mudMotor.HasField('PressureLoss4'):
            MOTOR_PRESS_LOSS_4 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                               ClassName='TextBox',
                                                                               AutomationId='HorizontalTextBox_CD_BHA_COMP_MOTOR_PRESS_LOSS_4')
            helper.SetCtrlValue(MOTOR_PRESS_LOSS_4, str(mudMotor.PressureLoss4))

    def stringMDWHelper(self, WorkStringTab, mwd: StringEditor.ItemDetails.MWDDetailData.MWD):
        mdwGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                            AutomationId='Expander1',
                                            Name='MWD')
        mdwBtn = mdwGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                      AutomationId='HeaderSite',
                                      Name='MWD')
        helper.AutoToggleStateClick(True, mdwBtn)
        SingleCategoryPropertyPageControl = mdwGrp.CustomControl(searchDepth=1,
                                                                 ClassName='SingleCategoryPropertyPageControl',
                                                                 AutomationId='UserControl_1')
        # 排量1
        if mwd.HasField('FlowRate1'):
            MWD_FLOWRATE_1 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                           ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_FLOWRATE_1')
            helper.SetCtrlValue(MWD_FLOWRATE_1, str(mwd.FlowRate1))
        # 压力损失1
        if mwd.HasField('PressureLoss1'):
            MWD_PRESS_LOSS_1 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_PRESS_LOSS_1')
            helper.SetCtrlValue(MWD_PRESS_LOSS_1, str(mwd.PressureLoss1))
        # 排量2
        if mwd.HasField('FlowRate2'):
            MWD_FLOWRATE_2 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                           ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_FLOWRATE_2')
            helper.SetCtrlValue(MWD_FLOWRATE_2, str(mwd.FlowRate2))
        # 压力损失2
        if mwd.HasField('PressureLoss2'):
            MWD_PRESS_LOSS_2 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_PRESS_LOSS_2')
            helper.SetCtrlValue(MWD_PRESS_LOSS_2, str(mwd.PressureLoss2))
        # 排量3
        if mwd.HasField('FlowRate3'):
            MWD_FLOWRATE_3 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                           ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_FLOWRATE_3')
            helper.SetCtrlValue(MWD_FLOWRATE_3, str(mwd.FlowRate3))
        # 压力损失3
        if mwd.HasField('PressureLoss3'):
            MWD_PRESS_LOSS_3 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_PRESS_LOSS_3')
            helper.SetCtrlValue(MWD_PRESS_LOSS_3, str(mwd.PressureLoss3))
        # 排量4
        if mwd.HasField('FlowRate4'):
            MWD_FLOWRATE_4 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                           ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_FLOWRATE_4')
            helper.SetCtrlValue(MWD_FLOWRATE_4, str(mwd.FlowRate4))
        # 压力损失4
        if mwd.HasField('PressureLoss4'):
            MWD_PRESS_LOSS_4 = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_PRESS_LOSS_4')
            helper.SetCtrlValue(MWD_PRESS_LOSS_4, str(mwd.PressureLoss4))
        # 传感器距接头底的距离
        if mwd.HasField('SensorDistanceToBottomJoint'):
            MWD_LENGTH_TO_SENSOR = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                 ClassName='TextBox',
                                                                                 AutomationId='HorizontalTextBox_CD_BHA_COMP_MWD_LENGTH_TO_SENSOR')
            helper.SetCtrlValue(MWD_LENGTH_TO_SENSOR, str(mwd.SensorDistanceToBottomJoint))

    def stringP_D_CHelper(self, WorkStringTab,
                          pdc: StringEditor.ItemDetails.PortCollar_DiverterSub_CirculatingSubDetailData.PortCollar_DiverterSub_CirculatingSub):
        pdcGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                            AutomationId='Expander1',
                                            Name='钻铤/分流接头/循环接头')
        pdcBtn = pdcGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                      AutomationId='HeaderSite',
                                      Name='钻铤/分流接头/循环接头')
        helper.AutoToggleStateClick(True, pdcBtn)

        SingleCategoryPropertyPageControl = pdcGrp.CustomControl(searchDepth=1,
                                                                 ClassName='SingleCategoryPropertyPageControl',
                                                                 AutomationId='UserControl_1')
        # 柄长度
        if pdc.HasField('ShankLength'):
            FISHNECK_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                            ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(pdc.ShankLength))
        # 柄外径
        if pdc.HasField('ShankOD'):
            FISHNECK_OD = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                        ClassName='TextBox',
                                                                        AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_OD')
            helper.SetCtrlValue(FISHNECK_OD, str(pdc.ShankOD))

        # 默认: `端口开放`为未勾选状态
        H1CheckBox = SingleCategoryPropertyPageControl.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                       Name='端口开放')
        helper.AutoToggleStateClick(pdc.PortOpen, H1CheckBox)
        if pdc.PortOpen:
            # % 喷嘴塞面积
            if pdc.HasField('NozzleAreaPlugged'):
                PERCENT_PLUGGED = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                ClassName='TextBox',
                                                                                AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PERCENT_PLUGGED')
                helper.SetCtrlValue(PERCENT_PLUGGED, str(pdc.NozzleAreaPlugged))
            # 总流面积
            if pdc.HasField('TotalFlowArea'):
                TFA = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                    ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_TFA')
                helper.SetCtrlValue(TFA, str(pdc.TotalFlowArea))

            # 表格项
            DataGrid = pdcGrp.DataGridControl(searchDepth=2, ClassName='HalWPFGrid',
                                                  AutomationId='dg:DataGrid_1')
            helper.ClearDataGrid(DataGrid)
            if len(pdc.items) > 0:
                tableData = ''
                for elem in pdc.items:
                    row = '{}	{}\r\n'.format(elem.Count, elem.Size)
                    tableData += row
                helper.WriteDataToDataGrid(DataGrid, tableData)

    def stringStabilizerHelper(self, WorkStringTab,
                               stab: StringEditor.ItemDetails.StabilizerDetailData.Stabilizer):
        stabGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                             AutomationId='Expander1',
                                             Name='稳定器')
        stabBtn = stabGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                        AutomationId='HeaderSite',
                                        Name='稳定器')
        helper.AutoToggleStateClick(True, stabBtn)
        SingleCategoryPropertyPageControl = stabGrp.CustomControl(searchDepth=1,
                                                                  ClassName='SingleCategoryPropertyPageControl',
                                                                  AutomationId='UserControl_1')
        # 扶正器的长度
        if stab.HasField('BladeLength'):
            STAB_BLADE_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                              ClassName='TextBox',
                                                                              AutomationId='HorizontalTextBox_CD_BHA_COMP_STAB_STAB_BLADE_LENGTH')
            helper.SetCtrlValue(STAB_BLADE_LENGTH, str(stab.BladeLength))
        # 打捞颈长度
        if stab.HasField('FishneckLength'):
            FISHNECK_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                            ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(stab.FishneckLength))
        # 叶片外径
        if stab.HasField('BladeOD'):
            STAB_BLADE_OD = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                          ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_BHA_COMP_STAB_STAB_BLADE_OD')
            helper.SetCtrlValue(STAB_BLADE_OD, str(stab.BladeOD))

    def stringSubHelper(self, WorkStringTab, sub: StringEditor.ItemDetails.SubDetailData.Sub):
        subGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                            AutomationId='Expander1',
                                            Name='子类')
        subBtn = subGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                      AutomationId='HeaderSite',
                                      Name='子类')
        helper.AutoToggleStateClick(True, subBtn)

        SingleCategoryPropertyPageControl = subGrp.CustomControl(searchDepth=1,
                                                                 ClassName='SingleCategoryPropertyPageControl',
                                                                 AutomationId='UserControl_1')
        # 柄长度
        if sub.HasField('ShankLength'):
            FISHNECK_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                            ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(sub.ShankLength))
        # 柄外径
        if sub.HasField('ShankOD'):
            FISHNECK_OD = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                        ClassName='TextBox',
                                                                        AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_OD')
            helper.SetCtrlValue(FISHNECK_OD, str(sub.ShankOD))

    def stringUnderreamerHelper(self, WorkStringTab,
                                underreamer: StringEditor.ItemDetails.UnderreamerDetailData.Underreamer):
        underreamerGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander',
                                                    AutomationId='Expander1',
                                                    Name='后扩眼')
        underreamerBtn = underreamerGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                      AutomationId='HeaderSite',
                                                      Name='后扩眼')
        helper.AutoToggleStateClick(True, underreamerBtn)

        SingleCategoryPropertyPageControl = underreamerGrp.CustomControl(searchDepth=1,
                                                                         ClassName='SingleCategoryPropertyPageControl',
                                                                         AutomationId='UserControl_1')
        # 最大井眼尺寸
        if underreamer.HasField('MaxHoleSize'):
            MAX_HOLE_SIZE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                          ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MAX_HOLE_SIZE')
            helper.SetCtrlValue(MAX_HOLE_SIZE, str(underreamer.MaxHoleSize))
        # 接触长度
        if underreamer.HasField('ContactLength'):
            CONTACT_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                           ClassName='TextBox',
                                                                           AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CONTACT_LENGTH')
            helper.SetCtrlValue(CONTACT_LENGTH, str(underreamer.ContactLength))
        # 试探井眼尺寸
        if underreamer.HasField('PilotHoleSize'):
            PILOT_HOLE_SIZE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                            ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PILOT_HOLE_SIZE')
            helper.SetCtrlValue(PILOT_HOLE_SIZE, str(underreamer.PilotHoleSize))
        # 打捞颈长度
        if underreamer.HasField('FishneckLength'):
            FISHNECK_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                            ClassName='TextBox',
                                                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_FISHNECK_LENGTH')
            helper.SetCtrlValue(FISHNECK_LENGTH, str(underreamer.FishneckLength))
        # 从部件中偏移， 默认是被勾选主的

        S1CheckBox = SingleCategoryPropertyPageControl.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                                       Name='从部件中偏移')
        helper.AutoToggleStateClick(underreamer.DivertedThroughComponent, S1CheckBox)
        if not underreamer.DivertedThroughComponent:
            # %喷嘴塞面积
            if underreamer.HasField('NozzleAreaPlugged'):
                PERCENT_PLUGGED = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                                ClassName='TextBox',
                                                                                AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PERCENT_PLUGGED')
                helper.SetCtrlValue(PERCENT_PLUGGED, str(underreamer.NozzleAreaPlugged))
            # 总流面积
            if underreamer.HasField('TotalFlowArea'):
                TFA = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                    ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_TFA')
                helper.SetCtrlValue(TFA, str(underreamer.TotalFlowArea))

            # 表格项
            DataGrid = underreamerGrp.DataGridControl(searchDepth=2, ClassName='HalWPFGrid',
                                                      AutomationId='dg:DataGrid_1')
            helper.ClearDataGrid(DataGrid)
            if len(underreamer.Items) > 0:
                tableData = ''
                for elem in underreamer.Items:
                    row = '{}	{}\r\n'.format(elem.Count, elem.Size)
                    tableData += row

                helper.WriteDataToDataGrid(DataGrid, tableData)
        else:
            # 余量
            if underreamer.HasField('AmountDiverted'):
                BITFLOW_RATE = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                             ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_BITFLOW_RATE')
                helper.SetCtrlValue(BITFLOW_RATE, str(underreamer.AmountDiverted))

    def stringStandoffItem(self, WorkStringTab,
                           standoff: StringEditor.StandoffDevices.StringStandoffItem.Mechanical, type):
        MultiCategoryPropertyPageControl_1 = WorkStringTab.CustomControl(searchDepth=3,
                                                                         ClassName='MultiCategoryPropertyPageControl',
                                                                         AutomationId='Controls:MultiCategoryPropertyPageControl_1')
        # 展开机械
        mechanicalGrp = MultiCategoryPropertyPageControl_1.GroupControl(searchDepth=1, ClassName='Expander',
                                                                        AutomationId='Expander1')
        mechanicalBtn = mechanicalGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                                    Name='机械')
        helper.AutoToggleStateClick(True, mechanicalBtn)

        SingleCategoryPropertyPageControl = mechanicalGrp.CustomControl(searchDepth=1,
                                                                        ClassName='SingleCategoryPropertyPageControl',
                                                                        AutomationId='UserControl_1')
        # 描述
        Desc = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                             ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_WP_TDA_FRD_ALL_DESCRIPTION')
        helper.ClearCtrlValue(Desc)
        if standoff.HasField('Desc'):
            helper.SetCtrlValue(Desc, str(standoff.Desc))
        # 当前外径
        ACT_DIAMETER = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                     ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_TDA_FRD_ALL_ACT_DIAMETER')
        helper.ClearCtrlValue(ACT_DIAMETER)
        if standoff.HasField('ActualOutsideDiameter'):
            helper.SetCtrlValue(ACT_DIAMETER, str(standoff.ActualOutsideDiameter))
        # 有效外径
        EFF_DIAMETER = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                     ClassName='TextBox',
                                                                     AutomationId='HorizontalTextBox_WP_TDA_FRD_ALL_EFF_DIAMETER')
        helper.ClearCtrlValue(EFF_DIAMETER)
        if standoff.HasField('EffectiveOutsideDiameter'):
            helper.SetCtrlValue(EFF_DIAMETER, str(standoff.EffectiveOutsideDiameter))
        # 单位重量
        ITEM_WEIGHT = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                    ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_WP_TDA_FRD_ALL_ITEM_WEIGHT')
        helper.ClearCtrlValue(ITEM_WEIGHT)
        if standoff.HasField('UnitWeigth'):
            helper.SetCtrlValue(ITEM_WEIGHT, str(standoff.UnitWeigth))
        # 单位长度
        ITEM_LENGTH = SingleCategoryPropertyPageControl.EditControl(searchDepth=1,
                                                                    ClassName='TextBox',
                                                                    AutomationId='HorizontalTextBox_WP_TDA_FRD_ALL_ITEM_LENGTH')
        helper.ClearCtrlValue(ITEM_LENGTH)
        if standoff.HasField('UnitLength'):
            helper.SetCtrlValue(ITEM_LENGTH, str(standoff.UnitLength))

        DataGrid = SingleCategoryPropertyPageControl.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                                     AutomationId='dg:DataGrid_1')
        helper.ClearDataGrid(DataGrid)

        # 表格项
        if len(standoff.Items) > 0 and type != StringEditor.StandoffDevices.StringStandoffItem.SectionType.Centralizer:
            tableData = ''
            for elem in standoff.Items:
                row = '{}	{}	{}	{}\r\n'.format(elem.HoleDiameter, elem.StartingForce, elem.RunningForce,
                                                        elem.RestoringForce)
                tableData += row
            helper.WriteDataToDataGrid(DataGrid, tableData)

    def TransSectionType(self, type: int) -> int:
        switch = {
            StringEditor.InnerString.SectionType.Unknown: StringEditor.SectionType.Unknown,
            StringEditor.InnerString.SectionType.Bit: StringEditor.SectionType.Bit,
            StringEditor.InnerString.SectionType.Casing: StringEditor.SectionType.Casing,
            StringEditor.InnerString.SectionType.CasingShoe: StringEditor.SectionType.CasingShoe,
            StringEditor.InnerString.SectionType.CoiledTubing: StringEditor.SectionType.CoiledTubing,
            StringEditor.InnerString.SectionType.DrillCollar: StringEditor.SectionType.DrillCollar,
            StringEditor.InnerString.SectionType.DrillPipe: StringEditor.SectionType.DrillPipe,
            StringEditor.InnerString.SectionType.FloatCollar: StringEditor.SectionType.FloatCollar,
            StringEditor.InnerString.SectionType.HeavyWeight: StringEditor.SectionType.HeavyWeight,
            StringEditor.InnerString.SectionType.Jar: StringEditor.SectionType.Jar,
            StringEditor.InnerString.SectionType.MudMotor: StringEditor.SectionType.MudMotor,
            StringEditor.InnerString.SectionType.PortCollar_DiverterSub_CirculatingSub: StringEditor.SectionType.PortCollar_DiverterSub_CirculatingSub,
            StringEditor.InnerString.SectionType.Stabilizer: StringEditor.SectionType.Stabilizer,
            StringEditor.InnerString.SectionType.Sub: StringEditor.SectionType.Sub,
            StringEditor.InnerString.SectionType.Tubing: StringEditor.SectionType.Tubing,
        }
        val = switch.get(type)
        if val is not None:
            return val
        else:
            helper.ExceptionHandler()

    def workStringProcess(self, elem: StringEditor.DataGridItem, WorkStringTab: auto.TabItemControl, bIsInner: bool = False):
        if bIsInner:
            elem.Type = self.TransSectionType(elem.Type)

        if helper.IsGeneralEnum(elem.Type):
            detail = StringEditor.ItemDetails.UnknownDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
        elif elem.Type == StringEditor.SectionType.ElectricalSubmersiblePump:
            detail = StringEditor.ItemDetails.ElectricalSubmersiblePumpDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
        elif elem.Type == StringEditor.SectionType.HydraulicLiftPump:
            detail = StringEditor.ItemDetails.HydraulicLiftPumpDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
        elif elem.Type == StringEditor.SectionType.Bit:
            detail = StringEditor.ItemDetails.BitDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringBitDataHelper(WorkStringTab, detail.bitData)
            self.stringNozzleSizesHelper(WorkStringTab, detail.nozzleSize)
        elif elem.Type == StringEditor.SectionType.Casing:
            detail = StringEditor.ItemDetails.CasingDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringCasingHelper(WorkStringTab, detail.casing)
        elif elem.Type == StringEditor.SectionType.CasingShoe:
            detail = StringEditor.ItemDetails.CasingShoeDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringCasingShoeFloatOptionHelper(WorkStringTab, detail.floatOption)
        elif elem.Type == StringEditor.SectionType.DrillCollar:
            detail = StringEditor.ItemDetails.DrillCollarDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringDrillCollarHelper(WorkStringTab, detail.drillCollar)
        elif elem.Type == StringEditor.SectionType.DrillPipe:
            detail = StringEditor.ItemDetails.DrillPipeDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringDrillPipeStringHelper(WorkStringTab, detail.StringItem)
        elif elem.Type == StringEditor.SectionType.EccentricStabillzer:
            detail = StringEditor.ItemDetails.EccentricStabilizerDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringEccentricStabilizerHelper(WorkStringTab, detail.eccemtrocStabilizer)
        elif elem.Type == StringEditor.SectionType.HeavyWeight:
            detail = StringEditor.ItemDetails.HeavyWeightDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringHeavyWeightHelper(WorkStringTab, detail.heavyWeight)
        elif elem.Type == StringEditor.SectionType.HoleOpener:
            detail = StringEditor.ItemDetails.HoleOpenerDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringHoleOpenerHelper(WorkStringTab, detail.holeOpener)
        elif elem.Type == StringEditor.SectionType.Jar:
            detail = StringEditor.ItemDetails.JarDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringJarHelper(WorkStringTab, detail.jar)
        elif elem.Type == StringEditor.SectionType.MudMotor:
            detail = StringEditor.ItemDetails.MudMotorDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringMudMotorHelper(WorkStringTab, detail.mudmotor)
        elif elem.Type == StringEditor.SectionType.MWD:
            detail = StringEditor.ItemDetails.MWDDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringMDWHelper(WorkStringTab, detail.mwd)
        elif elem.Type == StringEditor.SectionType.PortCollar_DiverterSub_CirculatingSub:
            detail = StringEditor.ItemDetails.PortCollar_DiverterSub_CirculatingSubDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringP_D_CHelper(WorkStringTab, detail.portCollar_DiverterSub_CirculatingSub)
        elif elem.Type == StringEditor.SectionType.Stabilizer:
            detail = StringEditor.ItemDetails.StabilizerDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringStabilizerHelper(WorkStringTab, detail.stabilizer)
        elif elem.Type == StringEditor.SectionType.Sub:
            detail = StringEditor.ItemDetails.SubDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringSubHelper(WorkStringTab, detail.sub)
        elif elem.Type == StringEditor.SectionType.Underreamer:
            detail = StringEditor.ItemDetails.UnderreamerDetailData()
            detail.ParseFromString(elem.Details.data)
            self.stringGeneralHelper(WorkStringTab, detail.general)
            self.stringMechanicalHelper(WorkStringTab, detail.mechanical)
            self.stringUnderreamerHelper(WorkStringTab, detail.underreamer)

    # 管柱
    def workString(self, MainStringEditorTabControl: auto.TabControl, stringEditor: StringEditor):
        # 管柱
        WorkStringTab = MainStringEditorTabControl.TabItemControl(searchDepth=1, ClassName='TabItem',
                                                                  AutomationId='WorkStringTab')
        helper.ClickOnce(WorkStringTab)
        # 管柱名称
        WorkName = WorkStringTab.EditControl(searchDepth=3, ClassName='TextBox',
                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_ASSEMBLY_NAME')
        # 管柱深度
        ASSEMBLY = WorkStringTab.EditControl(searchDepth=3, ClassName='TextBox',
                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_MD_ASSEMBLY_BASE')

        StringsGrid = WorkStringTab.DataGridControl(searchDepth=3, ClassName='HalWPFGrid', AutomationId='StringsGrid')

        # 尝试进行清空
        if not stringEditor.HasField('stringItem'):
            helper.ClearCtrlValue(WorkName)
            helper.ClearCtrlValue(ASSEMBLY)
            helper.ClearDataGrid(StringsGrid)
            return

        if stringEditor.stringItem.HasField('StringName'):
            helper.SetCtrlValue(WorkName, stringEditor.stringItem.StringName)
        if stringEditor.stringItem.HasField('StringDepth'):
            helper.SetCtrlValue(ASSEMBLY, str(stringEditor.stringItem.StringDepth))

        AdjDlg = auto.WindowControl(searchDepth=2, ClassName='Window', AutomationId='Window_1', Name='可调的深度')
        if helper.ExistCtrl(AdjDlg, 5):
            adjBtn = AdjDlg.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='Button_1')
            helper.ClickOnce(adjBtn)

        # 排列顺序 combobox
        order = WorkStringTab.ComboBoxControl(searchDepth=3, ClassName='ComboBox')
        helper.ComboBoxCtrlRestore(order)
        helper.SetCtrlComboBoxValue(order, stringEditor.stringItem.StringSortOrder)

        helper.ClearDataGrid(StringsGrid)
        preItem = None
        preElem = None
        for elem in stringEditor.stringItem.Items:
            StringsGrid.WheelDown()
            rowData = '{}					\r\n'.format(helper.EnumText(elem.Type))
            helper.WriteDataToDataGrid(StringsGrid, rowData)

            rowCount = StringsGrid.GetGridPattern().RowCount - 1
            # 选择一个Item
            item = StringsGrid.DataItemControl(foundIndex=rowCount, searchDepth=1, ClassName='DataGridRow',
                                               Name='DSWE.Core.Presentation.StringEditor.PresentationModel.StringComponentModel')

            if stringEditor.stringItem.StringSortOrder == StringEditor.SortOrder.soBottomToTop:
                if preItem == None:
                    preItem = item
                    preElem = elem
                    continue
                else:
                    preItem, item = item, preItem
                    preElem, elem = elem, preElem

            item.GetSelectionItemPattern().Select()

            # 选项的细节
            SingleCategoryPropertyPageControl = WorkStringTab.CustomControl(searchDepth=2,
                                                                            ClassName='SingleCategoryPropertyPageControl',
                                                                            AutomationId='Controls:SingleCategoryPropertyPageControl_1')
            combDetailsType = SingleCategoryPropertyPageControl.ComboBoxControl(searchDepth=1, ClassName='ComboBox')
            helper.ComboBoxCtrlRestore(combDetailsType)
            # 选择数值相对应的
            helper.SetCtrlComboBoxValue(combDetailsType, elem.Details.Type)

            Desc = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CATALOG_KEY_DESC')
            helper.SetCtrlValue(Desc, elem.Details.Desc)
            self.workStringProcess(elem, WorkStringTab)

        # 当为从下向上时会触发
        if preItem != None:
            item = preItem
            elem = preElem
            item.GetSelectionItemPattern().Select()

            # 选项的细节
            SingleCategoryPropertyPageControl = WorkStringTab.CustomControl(searchDepth=2,
                                                                            ClassName='SingleCategoryPropertyPageControl',
                                                                            AutomationId='Controls:SingleCategoryPropertyPageControl_1')
            combDetailsType = SingleCategoryPropertyPageControl.ComboBoxControl(searchDepth=1, ClassName='ComboBox')
            helper.ComboBoxCtrlRestore(combDetailsType)
            # 选择数值相对应的
            helper.SetCtrlComboBoxValue(combDetailsType, elem.Details.Type)

            Desc = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CATALOG_KEY_DESC')
            helper.SetCtrlValue(Desc, elem.Details.Desc)
            self.workStringProcess(elem, WorkStringTab)

    # 偏移间隙装置
    def standoffDevices(self, MainStringEditorTabControl: auto.TabControl, stringEditor: StringEditor):
        # 偏移间隙装置
        StandoffDevicesTab = MainStringEditorTabControl.TabItemControl(searchDepth=1, ClassName='TabItem',
                                                                       AutomationId='StandoffDevicesTab')
        helper.ClickOnce(StandoffDevicesTab)

        # 清空
        UseCbox = StandoffDevicesTab.CheckBoxControl(searchDepth=2, ClassName='CheckBox', AutomationId='CheckBox_1')
        helper.AutoToggleStateClick(False, UseCbox)

        # 展开 使用间隔器
        sdGrp = StandoffDevicesTab.GroupControl(searchDepth=2, ClassName='Expander', AutomationId='Expander1')
        sdBtn = sdGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite')

        if stringEditor.HasField('standoffDevices'):
            helper.AutoToggleStateClick(stringEditor.standoffDevices.UseStandoffDevices, UseCbox)
            if stringEditor.standoffDevices.UseStandoffDevices:
                helper.AutoToggleStateClick(True, sdBtn)
                # 表格
                DataGrid = sdGrp.DataGridControl(searchDepth=2, ClassName='HalWPFGrid',
                                                 AutomationId='StandoffDevicesGrid')
                helper.ClearDataGrid(DataGrid)

                # 表格项
                if len(stringEditor.standoffDevices.items) > 0:
                    for elem in stringEditor.standoffDevices.items:
                        row = '{}		{}	{}	{}	{}	{}\r\n'.format(elem.type, helper.BoolText(elem.Rigid),
                                                                                elem.disk_fromBottom.Start,
                                                                                elem.disk_fromBottom.End,
                                                                                elem.Units,
                                                                                elem.Joints)
                        helper.WriteDataToDataGrid(DataGrid, row)

                        rowCount = DataGrid.GetGridPattern().RowCount - 1
                        # 选择一个Item
                        item = DataGrid.DataItemControl(foundIndex=rowCount, searchDepth=1, ClassName='DataGridRow',
                                                        Name='DSWE.Core.Presentation.StandoffDevicesEditor.PresentationModel.StandoffDeviceModel')
                        item.GetSelectionItemPattern().Select()

                        self.stringStandoffItem(StandoffDevicesTab, elem.mechanical, elem.type)



    def innerString(self, MainStringEditorTabControl: auto.TabControl, stringEditor: StringEditor):
        # 内管柱
        InnerStringTab = MainStringEditorTabControl.TabItemControl(searchDepth=1, ClassName='TabItem',
                                                                   AutomationId='InnerStringTab')
        helper.ClickOnce(InnerStringTab)
        # 默认为未勾起
        UseCbox = InnerStringTab.CheckBoxControl(searchDepth=2, ClassName='CheckBox', AutomationId='CheckBox_1',
                                                 Name='使用内管柱')
        helper.AutoToggleStateClick(False, UseCbox)

        if stringEditor.HasField('innerString'):
            helper.AutoToggleStateClick(stringEditor.innerString.UseInnerString, UseCbox)
            if stringEditor.innerString.UseInnerString:
                # 内管柱名
                InnerStringName = InnerStringTab.EditControl(searchDepth=2,
                                                             ClassName='TextBox',
                                                             AutomationId='HorizontalTextBox_')
                helper.SetCtrlValue(InnerStringName, str(stringEditor.innerString.InnerStringName))
                # 内管柱深度
                InnerStringDepth = InnerStringTab.EditControl(searchDepth=2,
                                                              ClassName='TextBox',
                                                              AutomationId='HorizontalTextBox_CD_ASSEMBLY_MD_ASSEMBLY_BASE')
                helper.SetCtrlValue(InnerStringDepth, str(stringEditor.innerString.InnerStringDepth))

                StringsGrid = InnerStringTab.DataGridControl(searchDepth=3, ClassName='HalWPFGrid',
                                                             AutomationId='StringsGrid')
                helper.ClearDataGrid(StringsGrid)

                for elem in stringEditor.innerString.Items:
                    rowData = '{}					\r\n'.format(helper.EnumText(helper.EnumInnerTrans(elem.Type)))
                    helper.WriteDataToDataGrid(StringsGrid, rowData)

                    rowCount = StringsGrid.GetGridPattern().RowCount - 1
                    # 选择一个Item
                    item = StringsGrid.DataItemControl(foundIndex=rowCount, searchDepth=1, ClassName='DataGridRow',
                                                       Name='DSWE.Core.Presentation.StringEditor.PresentationModel.StringComponentModel')
                    item.GetSelectionItemPattern().Select()
                    # 选项的细节
                    SingleCategoryPropertyPageControl = InnerStringTab.CustomControl(searchDepth=2,
                                                                                     ClassName='SingleCategoryPropertyPageControl',
                                                                                     AutomationId='Controls:SingleCategoryPropertyPageControl_1')
                    combDetailsType = SingleCategoryPropertyPageControl.ComboBoxControl(searchDepth=1,
                                                                                        ClassName='ComboBox')
                    helper.ComboBoxCtrlRestore(combDetailsType)
                    # 选择数值相对应的
                    helper.SetCtrlComboBoxValue(combDetailsType, elem.Details.Type)

                    if elem.Details.HasField('Desc'):
                        Desc = SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CATALOG_KEY_DESC')
                        helper.SetCtrlValue(Desc, elem.Details.Desc)

                    self.workStringProcess(elem, InnerStringTab, True)
