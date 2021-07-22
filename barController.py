# -*- coding: utf-8 -*-

import helper
from protocol.wellplan_pb2 import BarTab
from launcher import *
from network import listener

class BarController:
    cxt = Context()
    conn: WebSocket = None

    def __init__(self, cxt: Context, conn: WebSocket = None):
        self.cxt = cxt
        self.conn = conn

    def isConnected(self):
        return self.conn is not None

    def Layout_Reset(self):
        MainRibbon = self.cxt.TopWindow.TabControl(searchDepth=1, ClassName='MainRibbon',
                                                   AutomationId='Ribbon:MainRibbon_1')
        # 主页
        Home = MainRibbon.TabItemControl(searchDepth=2, ClassName='RibbonHomeTab',
                                         AutomationId='Ribbon:RibbonTab_1')
        helper.ExistCtrl(Home, config.MINUTE)
        #helper.ClickOnce(Home)

        resetViewLayout = Home.ButtonControl(searchDepth=3, ClassName='Button', AutomationId='Button_6')
        helper.ClickOnce(resetViewLayout)

        wd = self.cxt.TopWindow.WindowControl(searchDepth=1, ClassName='Window', AutomationId='WindowDialog_1',
                                              Name='重置布局？')
        helper.ExistCtrl(wd, config.MINUTE)

        yesBtn = wd.ButtonControl(searchDepth=1, ClassName='Button', AutomationId='yesButton')
        helper.ClickOnce(yesBtn)

        closeStartPage = self.cxt.TopWindow.ButtonControl(searchDepth=1, ClassName='Button',
                                                          AutomationId='CloseAllInDocumentPane')
        helper.ExistCtrl(closeStartPage, config.MINUTE)
        helper.ClickOnce(closeStartPage)

    # 通用分析
    def GeneralOutputs(self, t, idx):
        MainRibbon = self.cxt.TopWindow.TabControl(searchDepth=1, ClassName='MainRibbon',
                                                   AutomationId='Ribbon:MainRibbon_1')

        GeneralTab = MainRibbon.TabItemControl(searchDepth=1, ClassName='RibbonTab',
                                               AutomationId='UserControl_123456', Name='通用分析')
        helper.ExistCtrl(GeneralTab, config.MINUTE)
        helper.ClickOnce(GeneralTab)

        if t == BarTab.GeneralOutputs.PlotsTables:
            WellpathOutputs = GeneralTab.GroupControl(searchDepth=1,
                                                      ClassName='RibbonGroup',
                                                      AutomationId='WellpathOutputs',
                                                      Name='图表')

            Btn = WellpathOutputs.ButtonControl(searchDepth=2,
                                                ClassName='RibbonButton',
                                                AutomationId='Ribbon1:RibbonButton_2',
                                                foundIndex=idx + 1)

            if not helper.CtrlRectContains(GeneralTab, Btn):
                GeneralTab.Click(ratioX=1)

            if not helper.CtrlRectContains(GeneralTab, Btn):
                helper.ExceptionHandler()

            helper.ClickOnce(Btn)

    # 扭矩&摩阻
    def TorqueDrag(self, t, idx):
        MainRibbon = self.cxt.TopWindow.TabControl(searchDepth=1, ClassName='MainRibbon',
                                                   AutomationId='Ribbon:MainRibbon_1')

        TorqueDragTab = MainRibbon.TabItemControl(searchDepth=1, ClassName='RibbonTab',
                                                  AutomationId='UserControl_123456', Name='扭矩 & 摩阻')
        helper.ExistCtrl(TorqueDragTab, config.MINUTE)
        helper.ClickOnce(TorqueDragTab)

        RibbonGroup = None
        if t == BarTab.TorqueDrag.FixedDepthPlots:
            RibbonGroup = TorqueDragTab.GroupControl(searchDepth=1,
                                                     ClassName='RibbonGroup',
                                                     AutomationId='TorqueDragFixedDepthPlots',
                                                     Name='固定深度图形')
        elif t == BarTab.TorqueDrag.StressPlots:
            RibbonGroup = TorqueDragTab.GroupControl(searchDepth=1,
                                                     ClassName='RibbonGroup',
                                                     AutomationId='TorqueDragStressPlots',
                                                     Name='应力图')
        elif t == BarTab.TorqueDrag.LoadStressData:
            RibbonGroup = TorqueDragTab.GroupControl(searchDepth=1,
                                                     ClassName='RibbonGroup',
                                                     AutomationId='TorqueDragLoadData',
                                                     Name='载荷与应力数据')
        elif t == BarTab.TorqueDrag.RoadmapPlots:
            RibbonGroup = TorqueDragTab.GroupControl(searchDepth=1,
                                                     ClassName='RibbonGroup',
                                                     AutomationId='TorqueDragRoadmapsCharts',
                                                     Name='路线图曲线')
        elif t == BarTab.TorqueDrag.Other:
            RibbonGroup = TorqueDragTab.GroupControl(searchDepth=1,
                                                     ClassName='RibbonGroup',
                                                     AutomationId='TorqueDragOther',
                                                     Name='其它')
        if RibbonGroup is None:
            helper.ExceptionHandler()

        Btn = RibbonGroup.ButtonControl(searchDepth=2,
                                        ClassName='RibbonButton',
                                        AutomationId='Ribbon1:RibbonButton_2',
                                        foundIndex=idx + 1)

        if not helper.CtrlRectContains(TorqueDragTab, Btn):
            TorqueDragTab.Click(ratioX=1)

        if not helper.CtrlRectContains(TorqueDragTab, Btn):
            helper.ExceptionHandler()

        helper.ClickOnce(Btn)

    # 正常钻进水力
    def Hydraulics(self, t, idx):
        pass

    # 固井
    def Cementing(self, t, idx):
        pass

    # 起下钻水力
    def SwabSurge(self, t, idx):
        pass

    # 欠平衡钻进水力
    def UBHydraulics(self, t, idx):
        pass

    # 井控压井
    def WellControl(self, t, idx):
        pass

    # 动态BHA
    def BHADynamics(self, t, idx):
        pass

    # 卡钻分析
    def StuckPipe(self, t, idx):
        pass

    def do(self, high, t, idx):
        if self.isConnected():
            listener.sendStatus(self.conn, "初始化指标信息")

        if isinstance(high, BarTab.GeneralOutputs):
            self.GeneralOutputs(t, idx)
        elif isinstance(high, BarTab.TorqueDrag):
            self.TorqueDrag(t, idx)
        else:
            helper.ExceptionHandler()

        if self.isConnected():
            listener.sendStatus(self.conn, "指标信息初始化完毕")
        # elif isinstance(high, BarTab.Hydraulics):
        #     self.Hydraulics(t, idx)
        # elif isinstance(high, BarTab.Cementing):
        #     self.Cementing(t, idx)
        # elif isinstance(high, BarTab.SwabSurge):
        #     self.SwabSurge(t, idx)
        # elif isinstance(high, BarTab.UBHydraulics):
        #     self.UBHydraulics(t, idx)
        # elif isinstance(high, BarTab.WellControl):
        #     self.WellControl(t, idx)
        # elif isinstance(high, BarTab.BHADynamics):
        #     self.BHADynamics(t, idx)
        # elif isinstance(high, BarTab.StuckPipe):
        #     self.StuckPipe(t, idx)


if __name__ == '__main__':
    cxt = Context()
    launch = Launcher(cxt)
    launch.do()

    bar = BarController(cxt)
    # bar.Layout_Reset()
    obj = BarTab.GeneralOutputs()
    bar.do(obj, BarTab.GeneralOutputs.PlotsTables, BarTab.GeneralOutputs.FormationTops)
    '''
    bar.TorqueDrag(1)
    bar.Hydraulics(1)
    bar.Cementing(1)
    bar.SwabSurge(1)
    bar.UBHydraulics(1)
    bar.WellControl(1)
    bar.BHADynamics(1)
    bar.StuckPipe(1)
    '''
