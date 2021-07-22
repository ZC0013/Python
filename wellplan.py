# -*- coding: utf-8 -*-

import os
import sys
import time
import helper

from network import listener

from protocol.wellplan_pb2 import BarTab
from protocol.wellplan_pb2 import TaskList

from loginManager import *
from dataController import *
from fluidsController import *
from holeController import *
from launcher import *
from projectManager import *
from rigController import *
from stringController import *
from subsurfaceController import *
from wellpathController import *
from barController import *
from workerController import *
from analyzerController import *


class WellPlanState(object):
    cxt = Context()
    taskList = TaskList()

    def reinit(self):
        self.cxt = Context()
        self.taskList = TaskList()

    def barHandler(self, t, high, idx):
        self.cxt.bar_t = t
        self.cxt.bar_high = high
        self.cxt.bar_idx = idx

    def setBarTab(self, barTab: BarTab):
        self.taskList.barTab.CopyFrom(barTab)

        if barTab.HasField('general'):
            general = barTab.general
            if general.HasField('plots'):
                self.barHandler(BarTab.GeneralOutputs.PlotsTables,
                                general,
                                general.plots)
        elif barTab.HasField('torqueDrag'):
            torqueDrag = barTab.torqueDrag
            if torqueDrag.HasField('fixeds'):
                self.barHandler(BarTab.TorqueDrag.FixedDepthPlots,
                                torqueDrag,
                                torqueDrag.fixeds)
            elif torqueDrag.HasField('stress'):
                self.barHandler(BarTab.TorqueDrag.StressPlots,
                                torqueDrag,
                                torqueDrag.stress)
            elif torqueDrag.HasField('loadStress'):
                self.barHandler(BarTab.TorqueDrag.LoadStressData,
                                torqueDrag,
                                torqueDrag.loadStress)
            elif torqueDrag.HasField('roadmaps'):
                self.barHandler(BarTab.TorqueDrag.RoadmapPlots,
                                torqueDrag,
                                torqueDrag.roadmaps)
            elif torqueDrag.HasField('others'):
                self.barHandler(BarTab.TorqueDrag.Other,
                                torqueDrag,
                                torqueDrag.others)
            elif torqueDrag.HasField('summary'):
                self.barHandler(BarTab.TorqueDrag.Summary,
                                torqueDrag,
                                torqueDrag.summary)
        elif barTab.HasField('hydraulics'):
            hydraulics = barTab.hydraulics
            if hydraulics.HasField('holeCleanings'):
                self.barHandler(BarTab.Hydraulics.HoleCleaningPlots,
                                hydraulics,
                                hydraulics.holeCleanings)
            elif hydraulics.HasField('pressures'):
                self.barHandler(BarTab.Hydraulics.Pressure_ECD_Plots,
                                hydraulics,
                                hydraulics.pressures)
            elif hydraulics.HasField('roadmaps'):
                self.barHandler(BarTab.Hydraulics.RoadmapPlots,
                                hydraulics,
                                hydraulics.roadmaps)
            elif hydraulics.HasField('steady'):
                self.barHandler(BarTab.Hydraulics.SteadyStateSwab_SurgePlots,
                                hydraulics,
                                hydraulics.steady)
            elif hydraulics.HasField('others'):
                self.barHandler(BarTab.Hydraulics.Other,
                                hydraulics,
                                hydraulics.others)
            elif hydraulics.HasField('bits'):
                self.barHandler(BarTab.Hydraulics.BitOptimizationPlots,
                                hydraulics,
                                hydraulics.bits)
        elif barTab.HasField('cements'):
            cements = barTab.cements
            if cements.HasField('ctrts'):
                self.barHandler(BarTab.Cementing.CentralizationPlots,
                                cements,
                                cements.ctrts)
            elif cements.HasField('fluids'):
                self.barHandler(BarTab.Cementing.FluidSequence,
                                cements,
                                cements.fluids)
            elif cements.HasField('times'):
                self.barHandler(BarTab.Cementing.Time_VolumePlots,
                                cements,
                                cements.times)
            elif cements.HasField('depths'):
                self.barHandler(BarTab.Cementing.DepthPlots,
                                cements,
                                cements.depths)
            elif cements.HasField('others'):
                self.barHandler(BarTab.Cementing.Other,
                                cements,
                                cements.others)
            elif cements.HasField('foamJobs'):
                self.barHandler(BarTab.Cementing.FoamJob,
                                cements,
                                cements.foamJobs)
        elif barTab.HasField('swab'):
            swab = barTab.swab
            if swab.HasField('swabs'):
                self.barHandler(BarTab.SwabSurge.SwabSurgePlots,
                                swab,
                                swab.swabs)
            elif swab.HasField('recips'):
                self.barHandler(BarTab.SwabSurge.ReciprocationPlots,
                                swab,
                                swab.recips)
        elif barTab.HasField('ubs'):
            ubs = barTab.ubs
            if ubs.HasField('unders'):
                self.barHandler(BarTab.UBHydraulics.UnderbalancePlots,
                                ubs,
                                ubs.unders)
            elif ubs.HasField('foams'):
                self.barHandler(BarTab.UBHydraulics.Foam_AirDrillingPlots,
                                ubs,
                                ubs.foams)
        elif barTab.HasField('wells'):
            wells = barTab.wells
            if wells.HasField('generals'):
                self.barHandler(BarTab.WellControl.GeneralPlots,
                                wells,
                                wells.generals)
            elif wells.HasField('kicks'):
                self.barHandler(BarTab.WellControl.KickTolerancePlots,
                                wells,
                                wells.kicks)
            elif wells.HasField('kills'):
                self.barHandler(BarTab.WellControl.KillSheetPlots_Tables,
                                wells,
                                wells.kills)
        elif barTab.HasField('bhas'):
            bhas = barTab.bhas
            if bhas.HasField('bhas'):
                self.barHandler(BarTab.BHADynamics.BHA_Plots,
                                bhas,
                                bhas.bhas)
            elif bhas.HasField('drills'):
                self.barHandler(BarTab.BHADynamics.DrillAheadPlots,
                                bhas,
                                bhas.drills)
            elif bhas.HasField('others'):
                self.barHandler(BarTab.BHADynamics.Other,
                                bhas,
                                bhas.others)
            elif bhas.HasField('vibs'):
                self.barHandler(BarTab.BHADynamics.VibrationAnaylysis,
                                bhas,
                                bhas.vibs)
        elif barTab.HasField('stucks'):
            stucks = barTab.stucks
            if stucks.HasField('outs'):
                self.barHandler(BarTab.StuckPipe.Outputs,
                                stucks,
                                stucks.outs)

    def setCast(self, caze: NewCase):
        self.taskList.case.CopyFrom(caze)

    def setWellPathEditor(self, wellpath: WellpathEditor):
        self.taskList.wellPathEditor.CopyFrom( wellpath )

    def setHoleSectionEditor(self, holeSection: HoleSectionEditor):
        self.taskList.holeSectionEditor.CopyFrom( holeSection )

    def setStringItem(self, stringItem: StringEditor):
        self.taskList.stringEditor.CopyFrom( stringItem )

    def setFluidsItem(self, fluidsItem: FluidsEditor):
        self.taskList.fluidsEditor.CopyFrom( fluidsItem )

    def setSubsurfaceItem(self, subsurfaceItem: SubsurfaceEditor):
        self.taskList.subsurfaceEditor.CopyFrom( subsurfaceItem )

    def setRigEquipmentItem(self, rigEquipmentItem: RigEquipment):
        self.taskList.rigEquipment.CopyFrom( rigEquipmentItem )

    def setOperationalItem(self, operationalItem: OperationalParameters):
        self.taskList.operational.CopyFrom( operationalItem )

    def setAnalysisItem(self, analysisItem: AnalysisSetting):
        self.taskList.analysisSetting.CopyFrom( analysisItem )

    def on_test(self):
        '''
            测试模式开启 查询已经存在的窗口
            并不影响已有逻辑
        '''
        if config.TEST_MODE:
            launcher = Launcher(self.cxt)
            launcher.update()

    def on_open(self, conn: WebSocket):
        launcher = Launcher(self.cxt, conn)
        launcher.do()

    def on_loginUser(self, conn: WebSocket):
        self.on_test()

        lg = LoginManager(self.cxt, conn)
        lg.do()

    def on_createProject(self, conn: WebSocket):
        self.on_test()

        ct = ProjectManager(self.cxt, self.taskList.case, conn)
        ct.do()

    def on_initLayout(self, conn: WebSocket):
        self.on_test()

        if conn is not None:
            listener.sendStatus(conn, "初始化布局")

        titleBar = self.cxt.TopWindow.TitleBarControl(searchDepth=1)
        maxBtn = titleBar.ButtonControl(searchDepth=1, Name='最大化')
        if helper.ExistCtrl(maxBtn, config.MINUTE):
            helper.ClickOnce(maxBtn)
        else:
            PART_MaximizeWindowButton = self.cxt.TopWindow.ButtonControl(searchDepth=1, AutomationId='PART_MaximizeWindowButton')
            if helper.ExistCtrl(PART_MaximizeWindowButton, config.MINUTE):
                helper.ClickOnce(PART_MaximizeWindowButton)


        bar = BarController(self.cxt, conn)
        bar.Layout_Reset()

        if conn is not None:
            listener.sendStatus(conn, "布局初始化完毕")

        bar.do(self.cxt.bar_high, self.cxt.bar_t, self.cxt.bar_idx)

    def wellPathItemProcess(self, conn: WebSocket):
        self.on_test()
        wellpath = WellpathController(self.cxt, self.taskList.wellPathEditor, conn)
        wellpath.do()

    def holeSectionItemProcess(self, conn: WebSocket):
        self.on_test()
        holeSection = HoleController(self.cxt, self.taskList.holeSectionEditor, conn)
        holeSection.do()

    def stringItemProcess(self, conn: WebSocket):
        self.on_test()
        string = StringController(self.cxt, self.taskList.stringEditor, conn)
        string.do()

    def fluidsItemProcess(self, conn: WebSocket):
        self.on_test()
        fluids = FluidsController(self.cxt, self.taskList.fluidsEditor, conn)
        fluids.do()

    def subsurfaceProcess(self, conn: WebSocket):
        self.on_test()
        subsurface = SubsurfaceController(self.cxt, self.taskList.subsurfaceEditor, conn)
        subsurface.do()

    def rigEquipmentProcess(self, conn: WebSocket):
        self.on_test()
        rig = RigController(self.cxt, self.taskList.rigEquipment, conn)
        rig.do()

    def analysisProcess(self, conn: WebSocket):
        self.on_test()
        analysis = AnalyzerController(self.cxt, self.taskList.analysisSetting, conn)
        analysis.do()

    def operationalProcess(self, conn: WebSocket):
        self.on_test()
        worker = WorkerController(self.cxt, self.taskList.operational, conn)
        worker.do()

    def on_outProcess(self, bar: BarTab, conn: WebSocket):
        self.on_test()
        dataCtrl = DataController(self.cxt, bar, conn)
        dataCtrl.do()

        if dataCtrl.isErr():
            return True, dataCtrl.getErrMsg()

        return False, dataCtrl.get()

    def on_resource(self, conn: WebSocket):
        self.on_test()
        #执行强制退出
        command = 'taskkill /F /IM WellPlan.exe'
        os.system(command)



