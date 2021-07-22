# -*- coding: utf-8 -*-

import config
import pyperclip
import helper

from protocol.wellplan_pb2 import WellpathEditor
from launcher import *
from network import listener

class WellpathController:
    cxt = Context()
    wellPathEditor = WellpathEditor()
    conn: WebSocket = None

    def __init__(self, cxt: Context, wellPathEditor: WellpathEditor, conn: WebSocket = None):
        self.cxt = cxt
        self.wellPathEditor = wellPathEditor
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def vsd(self, wellPathEditor: WellpathEditor, WellpathEditorView: auto.CustomControl):
        # 原点北
        OriginNorth = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox',
                                                     AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_VS_NORTH')
        helper.ClearCtrlValue(OriginNorth)

        # 原点东
        OriginEast = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_VS_EAST')
        helper.ClearCtrlValue(OriginEast)

        # 方位角
        DirctAngle = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox',
                                                    AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_PLANNED_AZIMUTH')
        helper.ClearCtrlValue(DirctAngle)

        if wellPathEditor.HasField('Vsd'):
            if wellPathEditor.Vsd.HasField('OriginN'):
                helper.SetCtrlValue(OriginNorth, str(wellPathEditor.Vsd.OriginN))
            if wellPathEditor.Vsd.HasField('OriginE'):
                helper.SetCtrlValue(OriginEast, str(wellPathEditor.Vsd.OriginE))
            if wellPathEditor.Vsd.HasField('Azimuth'):
                helper.SetCtrlValue(DirctAngle, str(wellPathEditor.Vsd.Azimuth))

    def settings(self, wellPathEditor: WellpathEditor, WellpathEditorView: auto.CustomControl):
        # 井深
        BH = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox',
                                            AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_BH_MD')
        helper.ClearCtrlValue(BH)
        # 插值间距
        Interval = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox',
                                                  AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_INTERPOLATION_INTERVAL')
        helper.ClearCtrlValue(Interval)

        if wellPathEditor.HasField('Settings'):
            if wellPathEditor.Settings.HasField('WellDepth'):
                helper.SetCtrlValue(BH, str(wellPathEditor.Settings.WellDepth))
            if wellPathEditor.Settings.HasField('InterpolationInterval'):
                helper.SetCtrlValue(Interval, str(wellPathEditor.Settings.InterpolationInterval))

    def stations(self, wellPathEditor: WellpathEditor, WellpathEditorView: auto.CustomControl):
        SurveyStationsGrid = WellpathEditorView.DataGridControl(searchDepth=1, ClassName='HalWPFGrid',
                                                                AutomationId='SurveyStationsGrid')
        helper.ClearDataGrid(SurveyStationsGrid)

        if len(wellPathEditor.Stations) != 0:
            # 首行，需要设置该行数据
            FirstRow = SurveyStationsGrid.DataItemControl(searchDepth=1, foundIndex=1, ClassName='DataGridRow',
                                                          Name='Hal.Core.Presentation.Infrastructure.DomainModelAdapters.AutoNotifyPropertyChangedAdapter')
            item1 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=2)
            txt1 = item1.TextControl(searchDepth=1, ClassName='TextBlock')
            helper.ClickOnce(item1)
            item1.DoubleClick()
            item1.MiddleClick()
            item1.SendKeys('{0}{0}{0}')
            item2 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=3)
            txt2 = item2.TextControl(searchDepth=1, ClassName='TextBlock')
            helper.ClickOnce(item2)
            item2.DoubleClick()
            item2.MiddleClick()
            item2.SendKeys('{0}{0}{0}')
            '''
                tableData='24,40.0	12.00	12.00\r\n24,404.0	12.00	ß12.00\r\n'
            '''
            tableData = ''
            if len(wellPathEditor.Stations) > 0:
                for elem in wellPathEditor.Stations:
                    if isinstance(elem, WellpathEditor.SurveyStations):
                        row = '{}	{}	{}\r\n'.format(elem.MD, elem.Inc, elem.Azi)
                        tableData += row
                helper.WriteDataToDataGrid(SurveyStationsGrid, tableData)

    def do(self):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化井轨迹信息")

        WellpathTab = self.cxt.TopWindow.TextControl(searchDepth=1, ClassName='TextBlock',
                                                     AutomationId='WellpathTab')
        # 点击井轨迹后的操作
        helper.ClickOnce(WellpathTab)

        WellpathEditorView = self.cxt.TopWindow.CustomControl(searchDepth=1,
                                                              ClassName='WellpathEditorView',
                                                              AutomationId='WellpathEditorView')
        helper.ExistCtrl(WellpathEditorView, config.MINUTE)

        helper.ClickOnce(WellpathEditorView)
        wellPathEditor = self.wellPathEditor

        if wellPathEditor:
            self.vsd(wellPathEditor, WellpathEditorView)
            self.settings(wellPathEditor, WellpathEditorView)
            self.stations(wellPathEditor, WellpathEditorView)

        if self.isConnected():
            listener.sendStatus(self.conn, "井轨迹信息初始化完毕")
