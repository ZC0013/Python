# -*- coding: utf-8 -*-
import pyperclip

from protocol.wellplan_pb2 import SubsurfaceEditor
from launcher import *
from network import listener
import helper

class SubsurfaceController:
    cxt = Context()
    subsurfaceEditor = SubsurfaceEditor()
    conn: WebSocket = None

    def __init__(self, cxt : Context, subsurfaceEditor : SubsurfaceEditor, conn: WebSocket = None):
        self.cxt = cxt
        self.subsurfaceEditor = subsurfaceEditor
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def porePressure(self, SubsurfaceEditorView : auto.CustomControl, subsurfaceEditor : SubsurfaceEditor):
        # 孔隙压力
        PorePressureGrp = SubsurfaceEditorView.GroupControl(searchDepth=2, ClassName='Expander',
                                                            AutomationId='Expander_3')
        PorePressureBtn = PorePressureGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, PorePressureBtn)

        DataGrid = PorePressureGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                   AutomationId='WPGridInfra:HalWPFGrid_3')
        helper.ClearDataGrid(DataGrid)

        for item, depth in auto.WalkControl(DataGrid, maxDepth=1):
            if isinstance(item, auto.DataItemControl):
                Cell = item.CustomControl(searchDepth=1, foundIndex=3, ClassName='DataGridCell')
                txt = Cell.TextControl(searchDepth=1, ClassName='TextBlock')
                helper.ClickOnce(txt)
                txt.DoubleClick()
                auto.SendKeys(str(subsurfaceEditor.poreFirstEMW))
                break

        # 表格项
        if len(subsurfaceEditor.porePressure) > 0:
            tableData = ''
            for elem in subsurfaceEditor.porePressure:
                row = '{}	{}	{}\r\n'.format(elem.TVD, elem.Pressure, elem.EMW)
                tableData += row
            helper.WriteDataToDataGrid(DataGrid, tableData)

    def fractureGradient(self, SubsurfaceEditorView : auto.CustomControl, subsurfaceEditor : SubsurfaceEditor):
        # 破裂压力梯度
        FractureGradientGrp = SubsurfaceEditorView.GroupControl(searchDepth=2, ClassName='Expander',
                                                                AutomationId='Expander_1')
        FractureGradientBtn = FractureGradientGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, FractureGradientBtn)

        DataGrid = FractureGradientGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                       AutomationId='FractureGradientGrid')
        helper.ClearDataGrid(DataGrid)

        for item, depth in auto.WalkControl(DataGrid, maxDepth=1):
            if isinstance(item, auto.DataItemControl):
                Cell = item.CustomControl(searchDepth=1, foundIndex=3, ClassName='DataGridCell')
                txt = Cell.TextControl(searchDepth=1, ClassName='TextBlock')
                helper.ClickOnce(txt)
                txt.DoubleClick()
                auto.SendKeys(str(subsurfaceEditor.fractureFirstEMW))
                break

        # 表格项
        if len(subsurfaceEditor.fractureGradient) > 0:
            tableData = ''
            for elem in subsurfaceEditor.fractureGradient:
                row = '{}	{}	{}\r\n'.format(elem.TVD, elem.Pressure, elem.EMW)
                tableData += row
            helper.WriteDataToDataGrid(DataGrid, tableData)

    def formationTop(self, SubsurfaceEditorView : auto.CustomControl, subsurfaceEditor : SubsurfaceEditor):
        # 地层
        FormationTopGrp = SubsurfaceEditorView.GroupControl(searchDepth=2, ClassName='Expander',
                                                            AutomationId='FormationTopExpander')
        FormationTopBtn = FormationTopGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                        AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, FormationTopBtn)

        DataGrid = FormationTopGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                   AutomationId='FormationTopGrid')
        helper.ClearDataGrid(DataGrid)
        # 表格项
        if len(subsurfaceEditor.formationTops) > 0:
            tableData = ''
            for elem in subsurfaceEditor.formationTops:
                row = '{}	{}	{}	{}\r\n'.format(elem.TVD, elem.MD, elem.Name,
                                                        helper.SubsurfaceEnumText(elem.lithology))
                tableData += row

            helper.WriteDataToDataGrid(DataGrid, tableData)

    def geothermalGradient(self, SubsurfaceEditorView : auto.CustomControl, subsurfaceEditor : SubsurfaceEditor):
        if subsurfaceEditor.HasField('geothermalGradient'):
            geothermalGradient = subsurfaceEditor.geothermalGradient
            # 地热
            GeothermalGradientGrp = SubsurfaceEditorView.GroupControl(searchDepth=2, ClassName='Expander',
                                                                      AutomationId='Expander_2')
            GeothermalGradientBtn = GeothermalGradientGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                                        AutomationId='HeaderSite')
            helper.AutoToggleStateClick(True, GeothermalGradientBtn)

            # 标准的概括
            if geothermalGradient.HasField('standardProfile'):
                StandardProfile = geothermalGradient.standardProfile
                StandardProfileGrp = GeothermalGradientGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                                        AutomationId='GroupBox_1')
                # 地表周围
                if StandardProfile.HasField('SurfaceAmbient'):
                    SURFACE_AMBIENT_TEMP = StandardProfileGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_TEMP_GRADIENT_GROUP_SURFACE_AMBIENT_TEMP')
                    helper.SetCtrlValue(SURFACE_AMBIENT_TEMP,str(StandardProfile.SurfaceAmbient))
                #泥线位置
                if StandardProfile.HasField('AtMudline'):
                    MUDLINE_TEMP = StandardProfileGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                          AutomationId='HorizontalTextBox_CD_TEMP_GRADIENT_GROUP_MUDLINE_TEMP')
                    helper.SetCtrlValue(MUDLINE_TEMP,str(StandardProfile.AtMudline))

                #在井的垂深处
                if StandardProfile.IsAtWellTVD:
                    AtWellTVDBtn = StandardProfileGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                         AutomationId='RadioButton_1')
                    helper.ClickOnce(AtWellTVDBtn)
                    if StandardProfile.HasField('AtWellTVD'):
                        TEMP_TVD = StandardProfileGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                  AutomationId='HorizontalTextBox_CD_TEMP_GRADIENT_GROUP_TEMP_TVD')
                        helper.SetCtrlValue(TEMP_TVD,str(StandardProfile.AtWellTVD))
                else:
                    GradientBtn = StandardProfileGrp.RadioButtonControl(searchDepth=1, ClassName='RadioButton',
                                                                        AutomationId='RadioButton_2')
                    helper.ClickOnce(GradientBtn)
                    if StandardProfile.HasField('Gradient'):
                        GRAD_TVD = StandardProfileGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                  AutomationId='HorizontalTextBox_CD_TEMP_GRADIENT_GROUP_GRAD_TVD')
                        helper.SetCtrlValue(GRAD_TVD,str(StandardProfile.Gradient))

            # 额外的温度点
            StandardProfileGrp = GeothermalGradientGrp.GroupControl(searchDepth=1, ClassName='GroupBox',
                                                                    AutomationId='GroupBox_2')
            DataGrid = StandardProfileGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                          AutomationId='TemperaturePointsGrid')
            helper.ClearDataGrid(DataGrid)
            # 表格项
            if len(geothermalGradient.additionalTemperaturePoints) > 0:
                tableData = ''
                for elem in geothermalGradient.additionalTemperaturePoints:
                    row = '{}	{}\r\n'.format(elem.TVD, elem.Temperature)
                    tableData += row
                helper.WriteDataToDataGrid(DataGrid, tableData)

    def formationInflux(self, SubsurfaceEditorView : auto.CustomControl, subsurfaceEditor : SubsurfaceEditor):
        # 地层流入
        formationInfluxGrp = SubsurfaceEditorView.GroupControl(searchDepth=2, ClassName='Expander',
                                                               AutomationId='Expander_4')
        formationInfluxBtn = formationInfluxGrp.ButtonControl(searchDepth=1, ClassName='Button',
                                                              AutomationId='HeaderSite')
        helper.AutoToggleStateClick(True, formationInfluxBtn)

        UseCheckbox = formationInfluxBtn.CheckBoxControl(searchDepth=1, ClassName='CheckBox',
                                                         AutomationId='FormationInfluxUseCheckbox')
        helper.AutoToggleStateClick(subsurfaceEditor.UseFormationInfluxData, UseCheckbox)
        if subsurfaceEditor.UseFormationInfluxData:
            DataGrid = formationInfluxGrp.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                          AutomationId='FormationInfluxGrid')
            DataGrid.WheelDown()
            helper.ClearDataGrid(DataGrid)
            # 表格项
            if len(subsurfaceEditor.formationInflux) > 0:
                for elem in subsurfaceEditor.formationInflux:
                    assert isinstance(elem, SubsurfaceEditor.FormationInflux)
                    DataGrid.WheelDown()
                    rowData = '{}	{}	{}	{}	{}\r\n'.format(elem.TVD, elem.MD, elem.Gas, elem.Oil, elem.Water)
                    helper.WriteDataToDataGrid(DataGrid, rowData)

                    rowCount = DataGrid.GetGridPattern().RowCount - 1
                    # 选择一个Item
                    item = DataGrid.DataItemControl(foundIndex=rowCount, searchDepth=1, ClassName='DataGridRow',
                                                       Name='DSWE.Core.Presentation.Subsurface.PresentationModel.FormationInfluxPresentationModel.FormationInfluxAutoNotifyPropertyChangedAdapter')

                    item.GetSelectionItemPattern().Select()

                    if elem.HasField('Details'):
                        # 选项的细节
                        detailsGrp = formationInfluxGrp.GroupControl(searchDepth=1, ClassName='GroupBox', AutomationId='GroupBox_1')
                        #气体摩尔重量
                        GAS_MOLE_WEIGHT = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_GAS_MOLE_WEIGHT')
                        helper.SetCtrlValue(GAS_MOLE_WEIGHT, str(elem.Details.GasMoleWeight))
                        #气体比热比
                        GAS_SPECIFIC_HEAT_RATIO = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_GAS_SPECIFIC_HEAT_RATIO')
                        helper.SetCtrlValue(GAS_SPECIFIC_HEAT_RATIO, str(elem.Details.GasSpecificHeatRatio))
                        #气体粘度
                        GAS_VISCOSITY = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_GAS_VISCOSITY')
                        helper.SetCtrlValue(GAS_VISCOSITY, str(elem.Details.GasViscosity))
                        #气体的临界压力
                        GAS_CRITICAL_PRESSURE = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_GAS_CRITICAL_PRESSURE')
                        helper.SetCtrlValue(GAS_CRITICAL_PRESSURE, str(elem.Details.GasCriticalPressure))
                        #气体的临界温度
                        GAS_CRITICAL_TEMPERATURE = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_GAS_CRITICAL_TEMPERATURE')
                        helper.SetCtrlValue(GAS_CRITICAL_TEMPERATURE, str(elem.Details.GasCriticalTemperature))
                        #油粘度
                        OIL_VISCOSITY = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_OIL_VISCOSITY')
                        helper.SetCtrlValue(OIL_VISCOSITY, str(elem.Details.OilViscosity))
                        #油密度
                        OIL_DENSITY = detailsGrp.EditControl(searchDepth=1, ClassName='TextBox',
                                                                             AutomationId='HorizontalTextBox_CD_FORMATION_INFLUX_OIL_DENSITY')
                        helper.SetCtrlValue(OIL_DENSITY, str(elem.Details.OilDensity))

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化地层信息")
        SubsurfaceTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock',
                                                       AutomationId='SubsurfaceTab')
        helper.ClickOnce(SubsurfaceTab)

        SubsurfaceEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                                         ClassName='SubsurfaceEditorView',
                                                                         AutomationId='SubsurfaceEditorView')
        self.porePressure(SubsurfaceEditorView, self.subsurfaceEditor)
        self.fractureGradient(SubsurfaceEditorView, self.subsurfaceEditor)
        self.formationTop(SubsurfaceEditorView, self.subsurfaceEditor)
        self.geothermalGradient(SubsurfaceEditorView, self.subsurfaceEditor)
        self.formationInflux(SubsurfaceEditorView, self.subsurfaceEditor)
        if self.isConnected():
            listener.sendStatus(self.conn, "地层信息初始化完毕")

