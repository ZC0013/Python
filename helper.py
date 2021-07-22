# -*- coding: utf-8 -*-
import time
import traceback

import pyperclip
import uiautomation as auto

import config
import network.listener as listener
from protocol import wellplan_pb2 as pb2
from loguru import logger


def CheckStatus():
    if listener.isStop():
        ExceptionHandler()


def EnumText(e: pb2.StringEditor.SectionType):
    CheckStatus()

    switch = {
        pb2.StringEditor.SectionType.Unknown: 'Unknown',
        pb2.StringEditor.SectionType.DrillPipe: 'Drill Pipe',
        pb2.StringEditor.SectionType.Accelerator: 'Accelerator',
        pb2.StringEditor.SectionType.AdjNearBitReamer: 'Adj. Near Bit Reamer',
        pb2.StringEditor.SectionType.Anchor: 'Anchor',
        pb2.StringEditor.SectionType.AnchorShoe: 'Anchor Shoe',
        pb2.StringEditor.SectionType.Bit: 'Bit',
        pb2.StringEditor.SectionType.Block: 'Block',
        pb2.StringEditor.SectionType.Casing: 'Casing',
        pb2.StringEditor.SectionType.CasingScraper: 'Casing Scraper',
        pb2.StringEditor.SectionType.CasingShoe: 'Casing Shoe',
        pb2.StringEditor.SectionType.CoiledTubing: 'Coiled Tubing',
        pb2.StringEditor.SectionType.ConventionalPump: 'Conventional Pump',
        pb2.StringEditor.SectionType.CoreBarrel: 'Core Barrel',
        pb2.StringEditor.SectionType.CuttingsBedImpeller: 'Cuttings Bed Impeller',
        pb2.StringEditor.SectionType.DragSpring: 'Drag Spring',
        pb2.StringEditor.SectionType.DrillCollar: 'Drill Collar',
        pb2.StringEditor.SectionType.ElectricalSubmersiblePump: 'Electrical Submersible Pump',
        pb2.StringEditor.SectionType.EccentricStabillzer: 'Eccentric Stabilizer',
        pb2.StringEditor.SectionType.Fish: 'Fish',
        pb2.StringEditor.SectionType.FishingTool: 'Fishing Tool',
        pb2.StringEditor.SectionType.FloatCollar: 'Float Collar',
        pb2.StringEditor.SectionType.Hangers: 'Hangers',
        pb2.StringEditor.SectionType.HeavyWeight: 'Heavy Weight',
        pb2.StringEditor.SectionType.HoleOpener: 'Hole Opener',
        pb2.StringEditor.SectionType.HydraulicLiftPump: 'Hydraulic Lift Pump',
        pb2.StringEditor.SectionType.HydraulicValve: 'Hydraulic Valve',
        pb2.StringEditor.SectionType.Instrument: 'Instrument',
        pb2.StringEditor.SectionType.IntelligentWellTool: 'Intelligent Well Tool',
        pb2.StringEditor.SectionType.Jar: 'Jar',
        pb2.StringEditor.SectionType.Mandrel: 'Mandrel',
        pb2.StringEditor.SectionType.MudMotor: 'Mud Motor',
        pb2.StringEditor.SectionType.MWD: 'MWD',
        pb2.StringEditor.SectionType.Packer: 'Packer',
        pb2.StringEditor.SectionType.PolishedBoreReceptacles: 'Polished Bore Receptacles',
        pb2.StringEditor.SectionType.PortCollar_DiverterSub_CirculatingSub: 'Port Collar/Diverter Sub/Circulating Sub',
        pb2.StringEditor.SectionType.ProgressingCavityPump: 'Progressing Cavity Pump',
        pb2.StringEditor.SectionType.PumpRod: 'Pump Rod',
        pb2.StringEditor.SectionType.Recorder: 'Recorder',
        pb2.StringEditor.SectionType.RotarySteerableSystem: 'Rotary Steerable System',
        pb2.StringEditor.SectionType.RotatingShutInTool: 'Rotating Shut in Tool',
        pb2.StringEditor.SectionType.SafetyJoint: 'Safety Joint',
        pb2.StringEditor.SectionType.Sampler: 'Sampler',
        pb2.StringEditor.SectionType.SandControlScreen: 'Sand Control Screen',
        pb2.StringEditor.SectionType.SlottedPipe: 'Slotted Pipe',
        pb2.StringEditor.SectionType.Stabilizer: 'Stabilizer',
        pb2.StringEditor.SectionType.Sub: 'Sub',
        pb2.StringEditor.SectionType.SubSurfaceSafetyValve: 'Sub-Surface Safety Valve',
        pb2.StringEditor.SectionType.Tubing: 'Tubing',
        pb2.StringEditor.SectionType.Underreamer: 'Underreamer',
        pb2.StringEditor.SectionType.WellboreEquipment: 'Wellbore Equipment',
    }
    val = switch.get(e)
    if val == None:
        logger.info('EnumText Not Found: {}'.format(e))

    return val


def EnumInnerTrans(e: pb2.StringEditor.InnerString.SectionType):
    CheckStatus()

    switch = {
        pb2.StringEditor.InnerString.SectionType.Unknown: pb2.StringEditor.SectionType.Unknown,
        pb2.StringEditor.InnerString.SectionType.Bit: pb2.StringEditor.SectionType.Bit,
        pb2.StringEditor.InnerString.SectionType.Casing: pb2.StringEditor.SectionType.Casing,
        pb2.StringEditor.InnerString.SectionType.CasingShoe: pb2.StringEditor.SectionType.CasingShoe,
        pb2.StringEditor.InnerString.SectionType.CoiledTubing: pb2.StringEditor.SectionType.CoiledTubing,
        pb2.StringEditor.InnerString.SectionType.DrillCollar: pb2.StringEditor.SectionType.DrillCollar,
        pb2.StringEditor.InnerString.SectionType.DrillPipe: pb2.StringEditor.SectionType.DrillPipe,
        pb2.StringEditor.InnerString.SectionType.FloatCollar: pb2.StringEditor.SectionType.FloatCollar,
        pb2.StringEditor.InnerString.SectionType.HeavyWeight: pb2.StringEditor.SectionType.HeavyWeight,
        pb2.StringEditor.InnerString.SectionType.Jar: pb2.StringEditor.SectionType.Jar,
        pb2.StringEditor.InnerString.SectionType.MudMotor: pb2.StringEditor.SectionType.MudMotor,
        pb2.StringEditor.InnerString.SectionType.PortCollar_DiverterSub_CirculatingSub: pb2.StringEditor.SectionType.PortCollar_DiverterSub_CirculatingSub,
        pb2.StringEditor.InnerString.SectionType.Stabilizer: pb2.StringEditor.SectionType.Stabilizer,
        pb2.StringEditor.InnerString.SectionType.Sub: pb2.StringEditor.SectionType.Sub,
        pb2.StringEditor.InnerString.SectionType.Tubing: pb2.StringEditor.SectionType.Tubing,
    }
    val = switch.get(e)
    if val == None:
        logger.info('EnumText Not Found: {}'.format(e))

    return val


def IsGeneralEnum(e: pb2.StringEditor.SectionType):
    CheckStatus()

    switch = {
        pb2.StringEditor.SectionType.Unknown: '',
        pb2.StringEditor.SectionType.Accelerator: '',
        pb2.StringEditor.SectionType.AdjNearBitReamer: '',
        pb2.StringEditor.SectionType.Anchor: '',
        pb2.StringEditor.SectionType.AnchorShoe: '',
        pb2.StringEditor.SectionType.CasingShoe: '',
        # pb2.StringEditor.SectionType.CoiledTubing: '',
        pb2.StringEditor.SectionType.ConventionalPump: '',
        pb2.StringEditor.SectionType.CoreBarrel: '',
        pb2.StringEditor.SectionType.CuttingsBedImpeller: '',
        pb2.StringEditor.SectionType.DragSpring: '',
        # pb2.StringEditor.SectionType.FloatCollar: '',
        pb2.StringEditor.SectionType.HydraulicValve: '',
        pb2.StringEditor.SectionType.Instrument: '',
        pb2.StringEditor.SectionType.IntelligentWellTool: '',
        pb2.StringEditor.SectionType.Mandrel: '',
        pb2.StringEditor.SectionType.Recorder: '',
        pb2.StringEditor.SectionType.RotatingShutInTool: '',
        pb2.StringEditor.SectionType.SafetyJoint: '',
        pb2.StringEditor.SectionType.Sampler: '',
        pb2.StringEditor.SectionType.Block: '',
        pb2.StringEditor.SectionType.Fish: '',
        pb2.StringEditor.SectionType.FishingTool: '',
        pb2.StringEditor.SectionType.Hangers: '',
        pb2.StringEditor.SectionType.PolishedBoreReceptacles: '',
        pb2.StringEditor.SectionType.ProgressingCavityPump: '',
        pb2.StringEditor.SectionType.RotarySteerableSystem: '',
        pb2.StringEditor.SectionType.SandControlScreen: '',
        pb2.StringEditor.SectionType.SlottedPipe: '',
        pb2.StringEditor.SectionType.WellboreEquipment: '',
        pb2.StringEditor.SectionType.CoiledTubing: '',
        pb2.StringEditor.SectionType.FloatCollar: '',
        pb2.StringEditor.SectionType.PumpRod: '',
        pb2.StringEditor.SectionType.SubSurfaceSafetyValve: '',
    }
    val = switch.get(e)
    if val is not None:
        return True
    else:
        return False


def StandoffDevicesEnumText(e: pb2.StringEditor.StandoffDevices.StringStandoffItem.SectionType):
    CheckStatus()

    switch = {
        pb2.StringEditor.StandoffDevices.StringStandoffItem.SectionType.Centralizer: 'Centralizer',
        pb2.StringEditor.StandoffDevices.StringStandoffItem.SectionType.Other: 'Other',
    }
    val = switch.get(e)
    if val == None:
        logger.info('StandoffDevicesEnumText Not Found: {}'.format(e))
    return val


def BoolText(b: bool):
    CheckStatus()

    if b:
        return 'True'
    return 'False'


def SubsurfaceEnumText(e: pb2.SubsurfaceEditor.FormationTops.Lithology):
    CheckStatus()

    switch = {
        pb2.SubsurfaceEditor.FormationTops.Lithology.Anhydrite: 'Anhydrite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Basalt: 'Basalt',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Chalk: 'Chalk',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Clay: 'Clay',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Claystone: 'Claystone',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Coal: 'Coal',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Coal_Anthracite: 'Coal, Anthracite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Coal_Bituminous: 'Coal, Bituminous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Coal_Lignite: 'Coal, Lignite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Conglomerate: 'Conglomerate',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Dolomite: 'Dolomite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Empty: 'Empty',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Evaporites_Anhydrite: 'Evaporites, Anhydrite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Evaporites_Gypsum: 'Evaporites, Gypsum',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Evporites_Halite: 'Evaporites, Halite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Gneiss: 'Gneiss',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Granite: 'Granite',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Gravel: 'Gravel',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Gypsum: 'Gypsum',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Halite_Salt: 'Halite (salt)',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone: 'Limestone',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Argillaceous: 'Limestone, Argillaceous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Dolomitic: 'Limestone, Dolomitic',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Fossiliferous: 'Limestone, Fossiliferous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Micritic: 'Limestone, Micritic',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Oolitic: 'Limestone, Oolitic',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Porous: 'Limestone, Porous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Limestone_Sparitic: 'Limestone, Sparitic',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Marl: 'Marl',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Mud: 'Mud',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Mudstone: 'Mudstone',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Other: 'Other',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Permafrost_Avg: 'Permafrost, Avg.',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sand: 'Sand',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sand_Silty: 'Sand, Silty',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sandstone: 'Sandstone',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sandstone_Coarse: 'Sandstone, Coarse',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sandstone_Fine: 'Sandstone, Fine',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sandstone_Fossiliferous: 'Sandstone, Fossiliferous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sandstone_Medium: 'Sandstone, Medium',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sandstone_Shaly: 'Sandstone, Shaly',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Schist: 'Schist',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale: 'Shale',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale_Calcarous: 'Shale, Calcarous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale_Dolomitic: 'Shale, Dolomitic',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale_Oil: 'Shale, Oil',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale_Sandy: 'Shale, Sandy',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale_Siliceous: 'Shale, Siliceous',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Shale_Silty: 'Shale, Silty',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Silt: 'Silt',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Sliltstone: 'Siltstone',
        pb2.SubsurfaceEditor.FormationTops.Lithology.Tuff: 'Tuff',
    }
    val = switch.get(e)
    if val == None:
        logger.info('SubsurfaceEnumText Not Found: {}'.format(e))
    return val


def CtrlRectContains(ctrl: auto.Control, other):
    CheckStatus()

    ctrl.SetFocus()

    rt = other.BoundingRectangle
    return ctrl.BoundingRectangle.contains(rt.left, rt.top)


def ComboBoxCtrlRestore(cbCtrl: auto.Control):
    CheckStatus()

    # 归为最顶
    cbCtrl.SetFocus()
    cbCtrl.SendKey(auto.Keys.VK_DOWN)
    for idx in range(0, 20):
        cbCtrl.SendKey(auto.Keys.VK_UP, waitTime=0.1)


# 根据 bState 和 控件状态 不匹配则点击
# bState true = 1
# false = 0
def AutoToggleStateClick(bState: bool, checkBox: auto.Control):
    CheckStatus()

    if not ExistCtrl(checkBox):
        return

    if bState:
        checkBox.SetFocus()
        checkBox.SendKey(auto.Keys.VK_SPACE)

    if checkBox.GetTogglePattern().ToggleState != int(bState):
        checkBox.SetFocus()
        checkBox.SendKey(auto.Keys.VK_SPACE)

    #assert checkBox.GetTogglePattern().ToggleState == int(bState)


# 点击一次
def ClickOnce(ctrl: auto.Control):
    CheckStatus()

    ctrl.SetFocus()
    if bool(ctrl.IsEnabled):
        if isinstance(ctrl, auto.RadioButtonControl):
            ctrl.SendKey(auto.Keys.VK_SPACE)
        else:
            ctrl.Click()


# 判断控件是否存在
# waitTime 为等待时间
def ExistCtrl(ctrl: auto.Control, waitTime=0) -> bool:
    CheckStatus()
    if ctrl.Exists(0, 0):
        return True
    if waitTime > 0 and auto.WaitForExist(ctrl, waitTime):
        return True
    return False


# 清空控件数值
def ClearCtrlValue(ctrl: auto.Control):
    CheckStatus()

    ctrl.SetFocus()
    ctrl.SendKeys('{CTRL}A')
    ctrl.SendKey(auto.Keys.VK_BACK)


# 设置一般控件的文本值
def SetCtrlValue(ctrl: auto.Control, text: str):
    CheckStatus()

    ctrl.SetFocus()
    ctrl.GetValuePattern().SetValue(text)
    ctrl.SendKey(auto.Keys.VK_RIGHT)
    ctrl.SetFocus()


# 设置 ComboBox 控件数值
def SetCtrlComboBoxValue(ctrl: auto.ComboBoxControl, idx: int):
    CheckStatus()

    ctrl.SetFocus()
    for idx in range(0, idx):
        ctrl.SendKey(auto.Keys.VK_DOWN, 0.1)


# 清空表格
def ClearDataGrid(ctrl: auto.DataGridControl):
    CheckStatus()
    # 全选进行删除
    # 得到表头
    PART_ColumnHeadersPresenter = ctrl.HeaderControl(searchDepth=1,
                                                     ClassName='DataGridColumnHeadersPresenter',
                                                     AutomationId='PART_ColumnHeadersPresenter')
    PART_FillerColumnHeader = PART_ColumnHeadersPresenter.HeaderItemControl(searchDepth=1,
                                                                            ClassName='DataGridColumnHeader',
                                                                            AutomationId='PART_FillerColumnHeader')
    PART_FillerColumnHeader.SetFocus()
    # 选择全部
    PART_FillerColumnHeader.RightClick()

    menu = auto.MenuControl(searchDepth=3, ClassName='ContextMenu', AutomationId='ContextMenu_1')
    ExistCtrl(menu, config.MINUTE)

    menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='选择所有')
    if ExistCtrl(menuItem) is False:
        menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='全选')
    if bool(menuItem.IsEnabled):
        menuItem.Click()
    # 删除全部
    PART_FillerColumnHeader.RightClick()
    menu = auto.MenuControl(searchDepth=3, ClassName='ContextMenu', AutomationId='ContextMenu_1')
    ExistCtrl(menu, config.MINUTE)
    menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='删除选择')
    if bool(menuItem.IsEnabled):
        menuItem.Click()
    
    time.sleep(3)


# 复制格表
def CopyDataGrid(ctrl: auto.DataGridControl) -> bool:
    CheckStatus()

    # 全选进行删除
    # 得到表头
    PART_ColumnHeadersPresenter = ctrl.HeaderControl(searchDepth=1,
                                                     ClassName='DataGridColumnHeadersPresenter',
                                                     AutomationId='PART_ColumnHeadersPresenter')
    PART_FillerColumnHeader = PART_ColumnHeadersPresenter.HeaderItemControl(searchDepth=1,
                                                                            ClassName='DataGridColumnHeader',
                                                                            foundIndex=2)
    PART_FillerColumnHeader.SetFocus()
    # 选择全部
    PART_FillerColumnHeader.RightClick()

    menu = auto.MenuControl(searchDepth=3, ClassName='ContextMenu', AutomationId='ContextMenu_1')
    ExistCtrl(menu, config.MINUTE)

    menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='选择所有')
    if ExistCtrl(menuItem) is False:
        menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='全选')
    if bool(menuItem.IsEnabled):
        menuItem.Click()
    # 复制
    PART_FillerColumnHeader.RightClick()
    menu = auto.MenuControl(searchDepth=3, ClassName='ContextMenu', AutomationId='ContextMenu_1')
    ExistCtrl(menu, config.MINUTE)
    menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='复制')
    if bool(menuItem.IsEnabled):
        menuItem.Click()
        return True

    return False


# 将数据追加置表格控件中
def WriteDataToDataGrid(ctrl: auto.Control, tableData: str):
    CheckStatus()

    if len(tableData) <= 0:
        return
    NewItemPlaceholder = ctrl.DataItemControl(searchDepth=1, ClassName='DataGridRow',
                                              Name='{NewItemPlaceholder}')
    NewItemPlaceholder.SetFocus()
    # 写入粘贴板
    pyperclip.copy(tableData)
    NewItemPlaceholder.RightClick()
    # 菜单
    menu = auto.MenuControl(searchDepth=3, ClassName='ContextMenu', AutomationId='ContextMenu_1')
    ExistCtrl(menu, config.MINUTE)
    # 追加
    menuItem = menu.MenuItemControl(searchDepth=2, ClassName='MenuItem', Name='追加（粘贴行到表格末尾）')
    if ExistCtrl(menuItem):
        menuItem.Click()



def ExceptionHandler(txt: str = ''):
    raise Exception(txt)
