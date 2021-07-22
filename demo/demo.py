#!c:\python27-x64\python.exe
# -*- coding:utf-8 -*-
import sys
import time
import win32api
import os
import pyperclip
import uiautomation as auto
from uiautomation import Logger

WAIT_TIME = 100

WP = auto.WindowControl(searchDepth=1, AutomationId='AppFoundation', ClassName='Window')

if WP.Exists(0, 0) == False:
    win32api.ShellExecute(0, 'open', 'C:\Landmark\EDT_5000.14\WellPlan\WellPlan.exe', '', 'C:\Landmark\EDT_5000.14\WellPlan', 0)
    
    print('没有找到对应的窗口进程, 开始启动该软件.\n')
    if auto.WaitForExist(WP, WAIT_TIME):
        print('启动成功!')

print(str(WP))
WP.SetActive()
WP.Show()
# #气体目录操作
# GasContent = WP.WindowControl(searchDepth=1, ClassName='Window', AutomationId='Window_1', Name='气体目录')
# GasListGrid = GasContent.DataGridControl(searchDepth=1, ClassName='HalWPFGrid', AutomationId='GasListGrid')
# GasEditorGrid = GasContent.DataGridControl(searchDepth=1, ClassName='HalWPFGrid', AutomationId='GasEditorGrid')
# coutStep = 0
#
# for item, depth in auto.WalkControl(GasListGrid, maxDepth=1):
#     if isinstance(item, auto.DataItemControl):
#         item.GetScrollItemPattern().ScrollIntoView(waitTime=0.1)
#         if coutStep == 55:
#             item.DoubleClick()
#         coutStep += 1
#
# for item, depth in auto.WalkControl(GasEditorGrid):
#     if isinstance(item, auto.DataItemControl):
#         item.GetScrollItemPattern().ScrollIntoView(waitTime=0.1)
#         #item.GetSelectionItemPattern().Select(waitTime=0.1)
#         item.DoubleClick(ratioX= 0.8)
#         auto.SendKeys('10')




'''
User = WP.EditControl(searchDepth=2, AutomationId='_user', ClassName='TextBox')
PWD = WP.EditControl(searchDepth=2, AutomationId='_password', ClassName='PasswordBox')
Login = WP.ButtonControl(searchDepth=3, Name=unicode('登录', 'utf-8'), ClassName='Button')

if User.Exists(0, 0) == False:
    print('USER 登陆窗口未找到, 开始等待\n')
    auto.WaitForExist(User, WAIT_TIME)

if PWD.Exists(0, 0) == False:
	print('PWD 登陆窗口未找到, 开始等待\n')
	auto.WaitForExist(PWD, WAIT_TIME)

User.SetValue('edm')
PWD.SetValue('Landmark1')
Login.Click()

### 创建新的解决方案 ###

WDialog = WP.WindowControl(searchDepth=1, AutomationId='WindowDialog_1', ClassName='Window')
if WDialog.Exists(0, 0) == False:
    auto.WaitForExist(WDialog, WAIT_TIME)

TB = WDialog.TabControl(searchDepth=1, AutomationId='TabControl_1', ClassName='TabControl')
if TB.Exists(0, 0) == False:
    auto.WaitForExist(TB, WAIT_TIME)

NewProject = TB.TabItemControl(searchDepth=1, AutomationId='TabItem_2', ClassName='TabItem', name=unicode('创建新的文案', 'utf-8'))

if NewProject.Exists(0, 0) == False:
    print('NewProject 控件寻找失败!')
    os.Exit(0)

NewProject.Click()

NewCase = NewProject.CustomControl(searchDepth=1, AutomationId='CreateNewCase:CreateNewCaseControl_1', ClassName='CreateNewCaseControl')

CompanyCombo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='CompanyCombo', ClassName='AutoCompleteBox')
CompanyCombo.SetValue(unicode("公司1", 'utf-8'))

ProjectCombo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='ProjectCombo', ClassName='AutoCompleteBox')
ProjectCombo.SetValue(unicode("项目1", 'utf-8'))

SiteCombo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='SiteCombo', ClassName='AutoCompleteBox')
SiteCombo.SetValue(unicode("油田1", 'utf-8'))

WellCombo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='WellCombo', ClassName='AutoCompleteBox')
WellCombo.SetValue(unicode("井1", 'utf-8'))

WellboreCombo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='WellboreCombo', ClassName='AutoCompleteBox')
WellboreCombo.SetValue(unicode("井眼1", 'utf-8'))

DesignCombo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='DesignCombo', ClassName='AutoCompleteBox')
DesignCombo.SetValue(unicode("设计1", 'utf-8'))

AnalysisName = NewCase.EditControl(searchDepth=2, AutomationId='AnalysisName', ClassName='TextBox')
AnalysisName.SetValue(unicode("文案1", 'utf-8'))

wpc = NewCase.ComboBoxControl(searchDepth=2, AutomationId='wpcontrols:AutoCompleteCombo_1', ClassName='AutoCompleteBox')
wpc.SetValue(unicode("坐标系1", 'utf-8'))

ValItems = [unicode("API", 'utf-8'), unicode("SI", 'utf-8'),
         unicode("Mixed API", 'utf-8'), unicode("API - US Survey Feet", 'utf-8')]

#for item in ValItems:
    #print(item)

UMS_Combo = NewCase.ComboBoxControl(searchDepth=2, AutomationId='UMS_Combo', ClassName='ComboBox')
print(str(UMS_Combo))

UMS_Combo.Click()
UMS_Combo.SendKey(auto.Keys.VK_UP)
UMS_Combo.SendKey(auto.Keys.VK_UP)
UMS_Combo.SendKey(auto.Keys.VK_UP)
UMS_Combo.SendKey(auto.Keys.VK_UP)

###选项判断

'''
#当前是API
'''
Input = unicode("API - US Survey Feet", 'utf-8')

if Input == ValItems[1]:
    UMS_Combo.SendKey(auto.Keys.VK_DOWN)
elif Input == ValItems[2]:
    UMS_Combo.SendKey(auto.Keys.VK_DOWN)
    UMS_Combo.SendKey(auto.Keys.VK_DOWN)
elif Input == ValItems[3]:
    UMS_Combo.SendKey(auto.Keys.VK_DOWN)
    UMS_Combo.SendKey(auto.Keys.VK_DOWN)
    UMS_Combo.SendKey(auto.Keys.VK_DOWN)
    
UMS_Combo.SendKey(auto.Keys.VK_ENTER)



#UMS_Combo.Select(unicode("API", 'utf-8'))
#print(UMS_Combo.GetSelectionPattern().GetSelection())


DatimCtl = NewCase.CustomControl(searchDepth=1, AutomationId='CreateNewCase:DatumControl_1', ClassName='DatumControl')
S1CheckBox = DatimCtl.CheckBoxControl(searchDepth=1, ClassName='CheckBox', Name=unicode('深海', 'utf-8'))
print(str(S1CheckBox))

if S1CheckBox.CurrentToggleState() != auto.ToggleState.On:
    S1CheckBox.Click()
    
    #if S1CheckBox.CurrentToggleState == auto.ToggleState.On:
H1CheckBox = DatimCtl.CheckBoxControl(searchDepth=1, ClassName='CheckBox', Name=unicode('海底', 'utf-8'))
if H1CheckBox.CurrentToggleState() != auto.ToggleState.On:
    H1CheckBox.Click()

if S1CheckBox.CurrentToggleState() == auto.ToggleState.On:

    below = DatimCtl.EditControl(AutomationId='TextBox_2', ClassName='TextBox')
    print(str(below))
    below.SetValue('223.33')
    
elif S1CheckBox.CurrentToggleState() == auto.ToggleState.On:
    above = DatimCtl.EditControl(AutomationId='TextBox_2', ClassName='TextBox')
    print(str(above))
    above.SetValue('223.33')

posHigh = DatimCtl.EditControl(AutomationId='Label_13', ClassName='TextBox')
print(str(posHigh))
posHigh.SetValue('223.33')

###如果深海选项被选中则会出现海水深度数值

if S1CheckBox.CurrentToggleState() == auto.ToggleState.On:
    #TextBox_1  海水深度
    seaDepthHigh = DatimCtl.EditControl(AutomationId='TextBox_1', ClassName='TextBox')
    print(str(seaDepthHigh))
    seaDepthHigh.SetValue('223.33')
else:
    #TextBox_1  大地表面标高
    earthFloorHigh = DatimCtl.EditControl(AutomationId='TextBox_1', ClassName='TextBox')
    print(str(earthFloorHigh))
    earthFloorHigh.SetValue('223.33')

WDialog.Click()

airDistance = DatimCtl.EditControl(AutomationId='TextBox_3', ClassName='TextBox')
print(str(airDistance))
print(airDistance.CurrentValue())

CreateProject = WDialog.ButtonControl(searchDepth=1, AutomationId = 'Button_3', ClassName='Button')
CreateProject.Click()

#####
'''
####### 数值输入必要条件 ######
'''
#基准面
DatumTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='DatumTab')
#点击基准面后的操作
DatumTab.Click()
DatumEditorView = WP.CustomControl(searchDepth=1, ClassName= 'DatumEditorView', AutomationId= 'UserControl_1')
#增加基准坐标系
AddDatumButton = DatumEditorView.ButtonControl(searchDepth=5, ClassName='Button', AutomationId = 'AddDatumButton')

'''
#井轨迹
WellpathTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='WellpathTab')
#点击井轨迹后的操作
WellpathTab.Click()
WellpathEditorView = WP.CustomControl(searchDepth=1, ClassName= 'WellpathEditorView', AutomationId= 'WellpathEditorView')
'''
#原点北
OriginNorth = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_VS_NORTH')
if not isinstance(OriginNorth, auto.EditControl):
    pass

helper.SetCtrlValue(OriginNorth,'3.3')
#原点东
OriginEast = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_VS_EAST')
helper.SetCtrlValue(OriginEast,'3.3')
#方位角
DirctAngle = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_PLANNED_AZIMUTH')
helper.SetCtrlValue(DirctAngle,'3.3')
#井深
BH = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_BH_MD')
helper.SetCtrlValue(BH,'12')
#插值间距
Interval = WellpathEditorView.EditControl(searchDepth=2, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_DEFINITIVE_SURVEY_HEADER_INTERPOLATION_INTERVAL')
helper.SetCtrlValue(Interval,'12')
#导入操作 暂不支持
#WellpathEditorImportButton = WellpathEditorView.ButtonControl(searchDepth=2, ClassName='Button', AutomationId='WellpathEditorImportButton')
#WellpathEditorImportButton.Click()
'''

SurveyStationsGrid = WellpathEditorView.DataGridControl(searchDepth=1, ClassName='HalWPFGrid', AutomationId='SurveyStationsGrid')
#得到表头
PART_ColumnHeadersPresenter = SurveyStationsGrid.HeaderControl(searchDepth=1, ClassName='DataGridColumnHeadersPresenter', AutomationId='PART_ColumnHeadersPresenter')
PART_FillerColumnHeader = PART_ColumnHeadersPresenter.HeaderItemControl(searchDepth=1, ClassName='DataGridColumnHeader', AutomationId='PART_FillerColumnHeader')
PART_FillerColumnHeader.RightClick()

#菜单
menu = auto.MenuControl(searchDepth= 3, ClassName = 'ContextMenu', AutomationId='ContextMenu_1')

menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='插入行')
print(menuItem.IsEnabled)

menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='选择所有')
menuItem.Click()
PART_FillerColumnHeader.RightClick()
#删除
menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='删除选择')
menuItem.Click()

#添加新的时所需的Item
NewItemPlaceholder = SurveyStationsGrid.DataItemControl(searchDepth=1, ClassName='DataGridRow', Name='{NewItemPlaceholder}')
#首行，需要设置该行数据
FirstRow = SurveyStationsGrid.DataItemControl(searchDepth=1, foundIndex=1, ClassName='DataGridRow', Name='Hal.Core.Presentation.Infrastructure.DomainModelAdapters.AutoNotifyPropertyChangedAdapter')

item1 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=2)
txt1 = item1.TextControl(searchDepth=1, ClassName='TextBlock')
item1.DoubleClick()
item1.SendKeys('{0}{ENTER}')
item2 = FirstRow.CustomControl(searchDepth=1, ClassName='DataGridCell', foundIndex=3)
txt2 = item2.TextControl(searchDepth=1, ClassName='TextBlock')
item2.DoubleClick()
item2.SendKeys('{0}{ENTER}')

tableData='24,40.0	12.00	12.00\r\n'
tableData += '24,404.0	12.00	12.00\r\n'
pyperclip.copy(tableData)
print(tableData)

NewItemPlaceholder.RightClick()
#菜单
menu = auto.MenuControl(searchDepth= 3, ClassName = 'ContextMenu', AutomationId='ContextMenu_1')
#追加
menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='追加（粘贴行到表格末尾）')
menuItem.Click()

'''
#井身
HoleSectionTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='HoleSectionTab')
HoleSectionTab.Click()
#点击井身后的操作
HoleSectionEditorView = WP.CustomControl(searchDepth=1, ClassName= 'HoleSectionEditorView', AutomationId= 'HoleSectionEditorView')
#隔水管添加按钮
HoleSectionEditorDisplayAddRiserButton = HoleSectionEditorView.ButtonControl(searchDepth=2, ClassName='Button', AutomationId= 'HoleSectionEditorDisplayAddRiserButton')
HoleSectionEditorDisplayAddRiserButton.SetFocus()
HoleSectionEditorDisplayAddRiserButton.SendKey(auto.Keys.VK_ENTER)
#设置隔水数值
RiserContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='RiserContainer', AutomationId = 'UserControl_1')
#外径
OuterDIA = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_OD_CASING')
OuterDIA.SetValue('123')
#内径
InnerDIA = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_HOLE_SIZE')
InnerDIA.SetValue('1')
#摩擦系数
Friction = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_COF')
Friction.SetValue('0.25')
#线性容积
Capacity = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_LINEAR_CAPACITY')
Capacity.SetValue('3')
#描述
Desc = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_CATALOG_KEY_DESC')
Desc.SetValue('qweqwe')
#生产商
########暂未设置
#模式
Model = RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_RISER_CD_HOLE_SECT_MODEL')
Model.SetValue('qweqwe')
#增压泵
Pump = RiserContainer.CheckBoxControl(searchDepth=4, ClassName='CheckBox', AutomationId='BoosterPumpIsEnabledCheckbox')
if Pump.CurrentToggleState() != auto.ToggleState.On:
    Pump.SetFocus()
    Pump.SendKey(auto.Keys.VK_SPACE)
#注入深度
InjectDepth=RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_WP_CASE_BOOSTER_PUMP_INJECTION_DEPTH')
InjectDepth.SetValue('1211')
#注入温度
InjectTemper=RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_WP_CASE_BOOSTER_PUMP_INJECTION_TEMPERATURE')
InjectTemper.SetValue('17.7')
#注入率
InjectRate=RiserContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_WP_CASE_BOOSTER_PUMP_INJECTION_RATE')
InjectRate.SetValue('1')

RiserContainer.Click()

#套管添加按钮
HoleSectionEditorDisplayAddCasingButton = HoleSectionEditorView.ButtonControl(searchDepth=2, ClassName='Button', AutomationId='HoleSectionEditorDisplayAddCasingButton')
HoleSectionEditorDisplayAddCasingButton.SetFocus()
HoleSectionEditorDisplayAddCasingButton.SendKey(auto.Keys.VK_ENTER)
#套管
CasingContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='CasingContainer', AutomationId = 'UserControl_1')
#长度
Length = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_LENGTH')
Length.SetValue('1122')
#变径
Tapered = CasingContainer.CheckBoxControl(searchDepth=4, ClassName='CheckBox', AutomationId='CasingItem_Tapered')
if Tapered.IsEnabled:
    print('开启了变径选项')
#套管鞋测深MD
MDShoe = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_MD_SHOE')
#外径
OuterDIA = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_OD_CASING')
OuterDIA.SetValue('111')
#内径
InnerDIA = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_HOLE_SIZE')
InnerDIA.SetValue('12')
#内通径
Drift = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_ID_DRIFT')
Drift.SetValue('12')
#有效井眼直径
DIAMETER = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_EFFECTIVE_DIAMETER')
DIAMETER.SetValue('11111')
#重量
WEIGHT = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_WEIGHT')
WEIGHT.SetValue('1000')
#级  combox未实现
Lvl = CasingContainer.ComboBoxControl(searchDepth=4, ClassName='ComboBox', AutomationId='ComboBox_1')
#最小屈服强度
MinYieleStress = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_MIN_YIELD_STRESS')
MinYieleStress.SetValue('241316.5')
#物质密度
MinYieleStress = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_MIN_YIELD_STRESS')
MinYieleStress.SetValue('241316.5')
#抗内压度
BURST = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_PRESSURE_BURST')
BURST.SetValue('111')
#抗挤强度率
COLLAPSE = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_ASSEMBLY_COMP_PRESSURE_COLLAPSE')
COLLAPSE.SetValue('111')
#摩擦系数
COF = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_COF')
COF.SetValue('1')
#摩擦系数2
COF2 = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_COF2')
COF2.SetValue('1')
#线性容积
CAPACITY = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_LINEAR_CAPACITY')
CAPACITY.SetValue('3')
#描述
DESC = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_CATALOG_KEY_DESC')
DESC.SetValue('qweqwe')
#生产商 combox未实现
Manu = CasingContainer.ComboBoxControl(searchDepth=4, ClassName='ComboBox', AutomationId='ComboBox_2')
#模式
Model = CasingContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CASINGITEM_CD_HOLE_SECT_MODEL')
Model.SetValue('qweqwe')

#祼眼
HoleSectionEditorDisplayAddOpenHoleButton = HoleSectionEditorView.ButtonControl(searchDepth=2, ClassName='Button', AutomationId='HoleSectionEditorDisplayAddOpenHoleButton')
HoleSectionEditorDisplayAddOpenHoleButton.SetFocus()
HoleSectionEditorDisplayAddOpenHoleButton.SendKey(auto.Keys.VK_ENTER)

#裸眼容器
OpenHoleContainer = HoleSectionEditorView.CustomControl(searchDepth=2, ClassName='OpenHoleContainer', AutomationId = 'UserControl_1')
OpenHoleContainer.SetFocus()
#长度
Length = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_LENGTH')
Length.SetValue('12')
#内径
Inner = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_HOLE_SIZE')
Inner.SetValue('10')
#有效直径
DIAMETER = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_EFFECTIVE_DIAMETER')
DIAMETER.SetValue('10')
#摩擦系数
COF = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_COF')
COF.SetValue('0.3')
#摩擦系数2
COF2 = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_COF2')
COF2.SetValue('0.3')
#线性容积
CAPACITY = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_LINEAR_CAPACITY')
if CAPACITY.IsEnabled:
    print('裸眼--线性容积可修改')
#体积超量
#VOLUME = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_VOLUME_EXCESS')
#VOLUME.SetValue('12')
#描述
DESC = OpenHoleContainer.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_OPENHOLE_CD_HOLE_SECT_CATALOG_KEY_DESC')
DESC.SetValue('qweqwe')

#分析设置
SchematicTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='SchematicTab')
SchematicTab.Click()
#点击分析设置后的操作
SchematicWindow = WP.CustomControl(searchDepth=1, ClassName='SchematicView', AutomationId='SchematicWindow')
FlowRate = SchematicWindow.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_MD_ASSEMBLY_BASE')
FlowRate.SetValue('11')
'''
'''
#管柱
StringTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='StringTab')
StringTab.Click()

MainStringEditorView = WP.CustomControl(searchDepth=1, ClassName='MainStringEditorView', AutomationId='MainStringEditorTabControl')
MainStringEditorTabControl = MainStringEditorView.TabControl(searchDepth=1, ClassName='TabControl', AutomationId='MainStringEditorTabControl')
#管柱
WorkStringTab = MainStringEditorTabControl.TabItemControl(searchDepth=1, ClassName='TabItem', AutomationId='WorkStringTab')

#管柱名称
WorkName = WorkStringTab.EditControl(searchDepth=3, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_ASSEMBLY_NAME')
helper.SetCtrlValue(WorkName,'asdasd')
#管柱深度
ASSEMBLY = WorkStringTab.EditControl(searchDepth=3, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_MD_ASSEMBLY_BASE')
helper.SetCtrlValue(ASSEMBLY,'12312')
WorkName.Click()

AdjDlg = auto.WindowControl(searchDepth=1, ClassName='Window', AutomationId='Window_1', Name='可调的深度')
if AdjDlg.Exists(0, 0):
    adjBtn = AdjDlg.ButtonControl(searchDepth=1, ClassName='Button', AutomationId = 'Button_1')
    adjBtn.SendKey(auto.Keys.VK_ENTER)

#排列顺序 combobox
order = WorkStringTab.ComboBoxControl(searchDepth=3, ClassName='ComboBox')
order.Click()
order.SendKey(auto.Keys.VK_DOWN)
order.SendKey(auto.Keys.VK_ENTER)
#管柱表格
StringsGrid = WorkStringTab.DataGridControl(searchDepth=3, ClassName='HalWPFGrid', AutomationId='StringsGrid')
DataRow = WorkStringTab.DataItemControl(searchDepth=3, ClassName='DataGridRow', Name='{NewItemPlaceholder}')
StringsGrid.WheelDown()
DataRow.RightClick()
#右击添加管柱
#菜单
menu = auto.MenuControl(searchDepth= 3, ClassName = 'ContextMenu', AutomationId='ContextMenu_1')
#追加
menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', AutomationId='MenuItem_5')
menuItem.Click()
print(StringsGrid.GetGridPattern().RowCount)
rowCount = StringsGrid.GetGridPattern().RowCount - 1
#选择一个Item
item = StringsGrid.DataItemControl(foundIndex=rowCount, searchDepth=1, ClassName='DataGridRow', Name='DSWE.Core.Presentation.StringEditor.PresentationModel.StringComponentModel')
item.GetSelectionItemPattern().Select()
'''
'''
#选项Unknown的细节
SingleCategoryPropertyPageControl = WorkStringTab.CustomControl(searchDepth=2, ClassName='SingleCategoryPropertyPageControl', AutomationId='Controls:SingleCategoryPropertyPageControl_1')
combDetailsType = SingleCategoryPropertyPageControl.ComboBoxControl(searchDepth=1, ClassName='ComboBox')
combDetailsType.Click()
for idx in range(0, 40):
    combDetailsType.SendKey(auto.Keys.VK_UP, waitTime = 0.1)
combDetailsType.SendKey(auto.Keys.VK_ENTER)

Desc=SingleCategoryPropertyPageControl.EditControl(searchDepth=1, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CATALOG_KEY_DESC')
helper.SetCtrlValue(Desc,'基本原则')

#展开通用
UnGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1', Name='通用')
print(str(UnGrp))

UnBtn = UnGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite', Name='通用')
if UnBtn.GetTogglePattern().ToggleState != auto.ToggleState.On:
    UnBtn.Click()
#生产商
PART_EditableTextBox = UnGrp.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='PART_EditableTextBox')
helper.SetCtrlValue(PART_EditableTextBox,'ARMCO')
#型号
ASSEMBLY_COMP_MODEL = UnGrp.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MODEL')
helper.SetCtrlValue(ASSEMBLY_COMP_MODEL,'111')
#长度
ASSEMBLY_COMP_LENGTH = UnGrp.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_LENGTH')
if not ASSEMBLY_COMP_LENGTH.GetValuePattern().IsReadOnly:
    helper.SetCtrlValue(ASSEMBLY_COMP_LENGTH,'1')
#内径
ASSEMBLY_COMP_OD_BODY = UnGrp.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_OD_BODY')
helper.SetCtrlValue(ASSEMBLY_COMP_OD_BODY,'0.1')
#封闭终端排代量
DISPLACEMENT = UnGrp.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CLOSED_END_DISPLACEMENT')
helper.SetCtrlValue(DISPLACEMENT,'0.3')
#体内径
ASSEMBLY_COMP_ID_BODY = UnGrp.EditControl(searchDepth=4, ClassName='TextBox', AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_ID_BODY')
helper.SetCtrlValue(ASSEMBLY_COMP_ID_BODY,'0.01')

#展开机械
machineGrp = WorkStringTab.GroupControl(searchDepth=4, ClassName='Expander', AutomationId='Expander1',
                                                Name='机械')
machineBtn = machineGrp.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='HeaderSite',
                                      Name='机械')
if machineBtn.GetTogglePattern().ToggleState != auto.ToggleState.On:
    machineBtn.WheelDown()
    machineBtn.Click()
# 毛量
APPROXIMATE_WEIGHT = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                            AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_APPROXIMATE_WEIGHT')
helper.SetCtrlValue(APPROXIMATE_WEIGHT,str(123))
# 级
Lvl = machineGrp.ComboBoxControl(searchDepth=4, ClassName='ComboBox', foundIndex=1)
Lvl.SetFocus()
for idx in range(0, 3):
    Lvl.SendKey(auto.Keys.VK_DOWN)
Lvl.SendKey(auto.Keys.VK_ENTER)

#最小屈服强度
MIN_YIELD_STRESS = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                           AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MIN_YIELD_STRESS')
helper.SetCtrlValue(MIN_YIELD_STRESS,str(68947.7))

#材质
texture = machineGrp.ComboBoxControl(searchDepth=4, ClassName='ComboBox', foundIndex=2)
texture.SetFocus()
for idx in range(0, 3):
    texture.SendKey(auto.Keys.VK_DOWN)
texture.SendKey(auto.Keys.VK_ENTER)

# 抗外挤强度
PRESSURE_COLLAPSE = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                           AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_PRESSURE_COLLAPSE')
helper.SetCtrlValue(PRESSURE_COLLAPSE,str(4354))

#杨氏模型
YOUNGS_MODULUS = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                           AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_YOUNGS_MODULUS')
helper.SetCtrlValue(YOUNGS_MODULUS,str(123))

#泊松比
POISSONS_RATIO = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                        AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_POISSONS_RATIO')
helper.SetCtrlValue(POISSONS_RATIO,str(0.4))
#密度
DENSITY = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                        AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_DENSITY')
helper.SetCtrlValue(DENSITY,str(1111))
#热膨胀系数
THERMAL_EXPANSION_COEF = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                 AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_THERMAL_EXPANSION_COEF')
helper.SetCtrlValue(THERMAL_EXPANSION_COEF,str(232))
#连接
CONNECTION_NAME = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                                AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_CONNECTION_NAME')
helper.SetCtrlValue(CONNECTION_NAME,str(232))
#补充扭矩
MAKEUP_TORQUE = machineGrp.EditControl(searchDepth=4, ClassName='TextBox',
                                         AutomationId='HorizontalTextBox_CD_ASSEMBLY_COMP_MAKEUP_TORQUE')
helper.SetCtrlValue(MAKEUP_TORQUE,str(222))

#偏移间隙装置
StandoffDevicesTab = MainStringEditorTabControl.TabItemControl(searchDepth=1, ClassName='TabItem', AutomationId='StandoffDevicesTab')
#内管柱
InnerStringTab = MainStringEditorTabControl.TabItemControl(searchDepth=1, ClassName='TabItem', AutomationId='InnerStringTab')
'''
'''
#流体
FluidTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='FluidTab')

#地层
SubsurfaceTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='SubsurfaceTab')

#钻井平台
RigEquipmentTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='RigEquipmentTab')

#作业
OperationalDataTab = WP.TextControl(searchDepth=1, ClassName='TextBlock', AutomationId='OperationalDataTab')

OperationalDataTab.Click()
'''
'''
RibbonTab = WP.TabControl(searchDepth=1, ClassName='MainRibbon', AutomationId='Ribbon:MainRibbon_1')
#主页
Home = RibbonTab.TabItemControl(searchDepth=2, ClassName='RibbonHomeTab', AutomationId='Ribbon:RibbonTab_1')
Home.SetFocus()
resetViewLayout = Home.ButtonControl(searchDepth=3, ClassName='Button', AutomationId='Button_6')
resetViewLayout.SendKey(auto.Keys.VK_ENTER)
wd = WP.WindowControl(searchDepth=1, ClassName='Window', AutomationId='WindowDialog_1', Name='重置布局？')
yesBtn = wd.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='yesButton')
yesBtn.SendKey(auto.Keys.VK_ENTER)

closeStartPage = WP.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='CloseAllInDocumentPane')
closeStartPage.SendKey(auto.Keys.VK_ENTER)

#通用分析
UnAn = RibbonTab.TabItemControl(searchDepth=2, ClassName='RibbonTab', AutomationId='UserControl_123456', Name='通用分析')
UnAn.Click()
#垂直井段
btn1 = UnAn.ButtonControl(searchDepth=3, ClassName='RibbonButton', AutomationId='Ribbon1:RibbonButton_2', foundIndex=1)
btn1.Click()
time.sleep(2)

#垂直并段
Grid_1 = WP.CustomControl(searchDepth=1, ClassName='WellpathVerticalSectionPlotView', AutomationId='Grid_1')
EDKResultVisualiser_1 = Grid_1.CustomControl(searchDepth=1, ClassName='EDKResultVisualizer', AutomationId='Controls1:EDKResultVisualiser_1')
#复制按钮
copy = EDKResultVisualiser_1.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='Button_1')
#点击复制按钮，复制图像
copy.Click()
#转换为数据
transfor = EDKResultVisualiser_1.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='FlipController')
#点击转换为表格
transfor.Click()

#点击复制表格数据
copy.Click()
#复制单元格
wd = WP.WindowControl(searchDepth=1, ClassName='Window', AutomationId='WindowDialog_1', Name='复制单元格')
Yes = wd.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='yesButton', Name='是')
Yes.Click()

time.sleep(5)

print(pyperclip.paste())
'''