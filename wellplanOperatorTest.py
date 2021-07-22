# -*- coding: utf-8 -*-


import wellplan
import protocol.wellplan_pb2 as pb2
from context import *
from launcher import *
import uiautomation as auto
from barController import *

#模块操作测试，主要测试参数填入测试
def CreateCase(case : pb2.NewCase):
    case.Company = '川庆1'
    case.Project = '页岩气1'
    case.Site = '长宁1'
    case.Well = '宁216H6-11'
    case.Wellbore = '主井眼1'
    case.Design = '11'
    case.Case = '文案 #21'
    case.Datum = '#11'
    case.WellheadElevation = 0.0
    case.DatumElevation = 531.0
    case.GroundElevation = 523.5
    case.units = pb2.NewCase.Units.SI
    case.enableOffshore = False
    case.enableSubsea = False

StationData = '''
9.91	0.13	92.35
36.58	0.48	37.15
65.76	0.04	6.25
93.83	0.35	13.55
122.42	0.26	63.85
151.36	0.22	307.05
180.34	0.22	101.55
209.32	0.35	203.65
238.28	0.48	189.55
267.21	0.62	188.05
296.15	0.26	180.55
325.13	0.70	192.55
354.07	0.22	209.95
375.83	0.32	228.59
396.57	0.44	237.35
425.01	0.13	193.75
453.97	2.90	205.75
482.96	5.76	207.35
492.62	5.41	205.65
521.58	7.43	205.75
550.51	10.01	202.45
579.45	12.13	202.95
608.43	12.17	202.95
637.37	11.82	203.15
666.31	11.38	204.45
695.15	11.20	204.55
724.07	10.30	205.60
753.03	9.35	205.95
781.91	8.79	206.95
810.86	7.85	205.50
839.79	7.25	202.25
868.74	6.68	203.45
897.71	5.95	209.15
926.68	5.00	208.00
955.59	4.26	210.65
984.56	3.30	211.15
1,013.54	2.46	210.75
1,042.52	1.70	195.00
1,071.52	0.92	182.05
1,100.50	1.10	187.35
1,129.45	0.48	138.65
1,158.41	0.18	62.15
1,187.37	0.44	108.75
1,216.37	0.35	95.45
1,245.28	0.66	141.45
1,274.24	0.48	109.35
1,303.20	0.83	62.55
1,332.13	0.83	130.40
1,361.12	0.97	124.15
1,390.09	1.36	127.25
1,419.05	1.30	113.15
1,435.54	1.12	135.62
1,465.50	1.89	112.45
1,494.75	0.53	131.75
1,523.72	0.44	98.65
1,552.69	1.05	104.65
1,581.67	1.41	98.55
1,610.66	1.10	91.45
1,639.58	1.05	76.85
1,668.56	0.79	80.75
1,697.51	0.75	291.65
1,726.45	1.19	296.15
1,755.39	0.79	291.65
1,784.35	1.76	290.55
1,813.27	1.67	288.95
1,842.20	1.63	287.55
1,871.14	1.23	290.75
1,900.14	1.01	288.55
1,929.08	0.83	287.25
1,958.13	0.97	287.35
1,971.58	1.14	336.95
1,980.63	2.46	7.40
1,998.49	6.24	28.30
2,009.68	9.93	39.40
2,037.75	16.79	45.90
2,067.09	22.32	41.80
2,080.22	25.14	35.50
2,096.64	29.09	35.50
2,110.40	31.99	35.70
2,125.41	36.21	36.70
2,154.15	43.77	33.80
2,183.48	53.70	27.80
2,212.02	62.05	26.20
2,241.12	64.60	27.90
2,270.34	64.16	27.20
2,297.82	64.95	30.20
2,324.84	68.20	29.90
2,326.80	68.12	28.80
2,338.55	69.35	29.40
2,345.18	71.54	29.40
2,358.04	75.06	28.50
2,385.76	77.34	26.90
2,399.97	77.17	28.70
2,409.71	76.99	30.20
2,415.30	77.08	29.90
2,422.81	77.34	29.90
2,443.98	80.86	32.20
2,459.85	81.39	30.60
2,470.34	82.97	30.80
2,472.32	83.32	31.80
2,476.20	83.94	32.50
2,501.19	91.14	37.40
2,509.91	94.04	36.20
2,519.53	95.63	36.90
2,520.22	95.71	36.40
2,530.56	97.03	36.00
2,550.15	95.01	33.20
2,559.88	92.99	31.80
2,574.66	93.60	31.60
2,586.74	92.81	33.60
2,598.14	93.25	31.80
2,615.69	94.83	32.50
2,643.94	97.21	31.60
2,673.62	95.01	32.00
2,702.65	92.46	32.20
2,731.25	89.47	29.90
2,731.71	89.30	31.10
2,760.89	86.40	29.50
2,789.41	89.65	30.60
2,818.70	87.80	28.70
2,830.34	89.38	30.20
2,846.81	90.09	30.90
2,864.77	90.00	31.30
2,872.06	91.49	30.80
2,875.77	91.85	30.60
2,886.02	90.62	32.30
2,903.49	90.62	30.90
2,932.89	90.97	32.90
2,962.33	90.00	31.50
2,991.47	89.65	31.10
3,006.37	91.41	31.60
3,020.86	91.49	34.10
3,049.20	92.02	33.90
3,078.60	91.76	34.50
3,094.83	91.14	34.60
3,107.14	91.23	35.20
3,136.09	91.76	34.60
3,165.76	92.29	37.10
3,193.63	91.32	34.60
3,208.80	91.41	34.50
3,223.50	90.97	32.50
3,230.62	90.44	33.60
3,252.73	90.79	31.30
3,280.94	90.88	30.20
3,309.81	91.76	29.20
3,340.09	91.93	29.40
3,368.20	91.49	29.20
3,396.96	91.05	30.90
3,425.20	90.70	32.30
3,455.27	90.79	33.00
3,485.39	90.18	35.00
3,513.09	89.65	34.30
3,541.95	89.74	33.40
3,626.11	88.77	27.80
3,633.08	89.91	27.60
3,646.90	89.47	28.10
3,661.14	88.51	29.50
3,689.50	88.68	29.90
3,710.14	88.07	29.00
3,718.02	88.33	29.40
3,719.05	88.24	29.50
3,732.55	88.51	29.90
3,747.19	86.66	29.90
3,775.61	86.31	30.20
3,805.51	89.12	30.20
3,835.74	88.42	30.20
3,864.48	87.51	30.82
3,892.74	87.45	33.40
3,922.24	87.28	32.20
3,950.44	88.07	31.30
3,955.20	88.42	31.30
3,957.27	88.15	33.60
3,960.09	88.15	32.20
3,981.67	85.96	29.40
3,988.63	85.52	27.60
4,017.71	85.43	28.70
4,046.89	86.22	28.30
'''
def CreateWellpathEditor(we : pb2.WellpathEditor):
    we.Vsd.Azimuth = 0
    we.Vsd.OriginE = 0
    we.Vsd.OriginN = 0

    we.Settings.WellDepth = 4100
    we.Settings.InterpolationInterval = 9.14

    StationData.strip()

    for rowData in StationData.split('\n'):
        if len(rowData) == 0:
            continue
        md, inc, azi = rowData.split('\t')
        Survey = we.Stations.add()
        Survey.MD = float(md.replace(',',''))
        Survey.Inc = float(inc.replace(',',''))
        Survey.Azi = float(azi.replace(',',''))
    return we

#CreateWellpathEditor(pb2.WellpathEditor())

def CreateHoleSectionEditor(hs : pb2.HoleSectionEditor):
    '''
    hs.riser.OD = 1.1
    hs.riser.ID = 1.1
    hs.riser.FrictionFactor = 1.1
    hs.riser.LinearCapacity = 1.1
    hs.riser.Desc = 'qweqwe'
    hs.riser.manu = pb2.HoleSectionEditor.Manufacturer.mGUIBERSON
    hs.riser.Model = 'qweqwe'
    hs.riser.Pump.InjectionDepth = 111
    hs.riser.Pump.InjectionRate = 11
    hs.riser.Pump.InjectionTemperature = 30
    '''
    c = hs.casing.add()
    if not isinstance(c, pb2.HoleSectionEditor.Casing):
        return
    c.MDBase = 1360
    c.Length = 1360
    c.OD = 244.5
    c.ID = 220.52
    c.DriftId = 220.52
    c.EffectiveHoleDiameter = 311.20
    '''
    c.Weight = 15
    c.grade = pb2.HoleSectionEditor.Casing.Grade.gCT_100
    c.MinYieldStrength = 1.2
    c.BurstRating = 1.3
    c.CollapseRating = 11
    '''
    c.FrictionFactor = 0.04
    c.LinearCapacity = 38.19
    '''
    c.Desc = 'asdfasdf'
    c.ShoeMD = 22
    c.Model = 'qweqw'
    '''

    #Open Hole
    oh = hs.openHole.add()
    if not isinstance(oh, pb2.HoleSectionEditor.OpenHole):
        return

    oh.MDBase = 4100
    oh.Length = 2740
    oh.ID = 215.9
    oh.EffectiveDiameter = 215.90
    oh.FrictionFactor = 0.25
    oh.VolumeExcess = 0
    #oh.Desc = 'qweqwe'

def CreateStringEditor(s : pb2.StringEditor):
    s.stringItem.StringName = 'Assembly'
    s.stringItem.StringDepth = 4100.0
    s.stringItem.StringSortOrder = pb2.StringEditor.SortOrder.soBottomToTop
    item = s.stringItem.Items.add()

    # 1 -- item
    item.Type = pb2.StringEditor.SectionType.Bit
    item.Details.Type = pb2.StringEditor.ItemDetails.BitDetailData.Type.tPolycrystallineDiamondBit
    item.Details.Desc = 'Polycrystalline Diamond Bit 6.786 cm²'

    bit = pb2.StringEditor.ItemDetails.BitDetailData()

    bit.bitData.manufacturer = pb2.StringEditor.ItemDetails.mHALLIBURTON
    bit.bitData.ModelNumber = 'TK56'
    bit.bitData.Length = 0.210
    bit.bitData.ApproximateWeight = 112.08
    bit.bitData.Bit_Drill_Diameter = 215.90
    bit.nozzleSize.TotalFlowArea = 6.786
    item.Details.data = bit.SerializeToString()

    # 2 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.MWD
    item.Details.Type = pb2.StringEditor.ItemDetails.MWDDetailData.Type.tLoggingWhileDrilling
    item.Details.Desc = 'TRIPLE COMBO/PWD, 6 3/4" in'

    MWD = pb2.StringEditor.ItemDetails.MWDDetailData()
    MWD.general.Length = 10.0
    MWD.general.BodyOD = 178.0
    MWD.general.ClosedEndDisplacement = 24.88
    MWD.general.BodyID = 48.77
    MWD.general.LinearCapacity = 1.87

    MWD.mechanical.ApproximateWeight = 150.0
    MWD.mechanical.grade = int(pb2.StringEditor.ItemDetails.MWDDetailData.Grade.gALLOY_25_1)
    MWD.mechanical.MinimumYieldStrength = 758423.3
    MWD.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.Material.mSS_15_15LC
    MWD.mechanical.YoungsMoudulus = 190984777.98
    MWD.mechanical.PoissonsRatio = 0.3
    MWD.mechanical.Density = 7769
    MWD.mechanical.CoeffOfThermalExp = 15.30
    MWD.mechanical.Connection = '4 1/2" IF'
    MWD.mechanical.MakeupTorque = 44742.0
    MWD.mwd.FlowRate1 = 1.7034
    MWD.mwd.PressureLoss1 = 455.05
    MWD.mwd.FlowRate2 = 4.5425
    MWD.mwd.PressureLoss2 = 2702.74
    item.Details.data = MWD.SerializeToString()

    # 3 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.Sub
    item.Details.Type = pb2.StringEditor.ItemDetails.SubDetailData.Type.FloatSub
    item.Details.Desc = '7, 7 x3 in'

    sub = pb2.StringEditor.ItemDetails.SubDetailData()
    sub.general.Length = 0.5
    sub.general.BodyOD = 172.0
    sub.general.ClosedEndDisplacement = 23.24
    sub.general.BodyID = 76.20
    sub.general.LinearCapacity = 4.56

    sub.mechanical.ApproximateWeight = 159.10
    sub.mechanical.grade = pb2.StringEditor.ItemDetails.Mechanical.Grade.g4145H_MOD
    sub.mechanical.MinimumYieldStrength = 758423.3
    sub.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.Material.mCS_API_5D_7
    sub.mechanical.YoungsMoudulus = 206842719.84
    sub.mechanical.PoissonsRatio = 0.30
    sub.mechanical.Density = 7849
    sub.mechanical.CoeffOfThermalExp = 12.42
    sub.mechanical.Connection = '5 1/2 REG'
    sub.mechanical.MakeupTorque = 45419.9

    sub.sub.ShankLength = 0.457
    sub.sub.ShankOD = 176.78

    item.Details.data = sub.SerializeToString()

    # 4 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.DrillPipe
    item.Details.Type = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Type.DrillPipe
    item.Details.Desc = 'Drill Pipe 5 in, 25.60 ppf, G, 5 1/2 FH, 1'

    drill = pb2.StringEditor.ItemDetails.DrillPipeDetailData()
    drill.general.Length = 9.430
    drill.general.BodyOD = 127.0
    drill.general.ClosedEndDisplacement = 12.67
    drill.general.BodyID = 101.60
    drill.general.LinearCapacity = 8.11

    drill.mechanical.ApproximateWeight = 72.03
    drill.mechanical.grade = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Grade.dpG
    drill.mechanical.MinimumYieldStrength = 723949.5
    drill.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.mCS_API_5D_7
    drill.mechanical.YoungsMoudulus = 206842719.84
    drill.mechanical.PoissonsRatio = 0.3
    drill.mechanical.Density = 7849
    drill.mechanical.CoeffOfThermalExp = 12.42
    drill.mechanical.Connection = '5 1/2 FH'
    drill.mechanical.MakeupTorque = 64035.3

    drill.StringItem.serviceClass =pb2.StringEditor.ItemDetails.DrillPipeDetailData.String.ServiceClass.sc1
    drill.StringItem.WallTickness = 100.0
    drill.StringItem.ConnectionOD = 184.15
    drill.StringItem.ConnectionID = 82.55
    drill.StringItem.AverageJointLength = 9.14
    drill.StringItem.TollJointLength = 0.433
    drill.StringItem.ConnectionTorsionalYield = 106725.9
    drill.StringItem.UltimateTensileStrength = 792897.1
    drill.StringItem.FatigueEnduranceLimit = 137895.1

    item.Details.data = drill.SerializeToString()

    # 5 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.Sub
    item.Details.Type = pb2.StringEditor.ItemDetails.SubDetailData.Type.FloatSub
    item.Details.Desc = '6, 6 x2 in'

    sub = pb2.StringEditor.ItemDetails.SubDetailData()
    sub.general.Length = 0.5
    sub.general.BodyOD = 165.10
    sub.general.ClosedEndDisplacement = 21.41
    sub.general.BodyID = 48.77
    sub.general.LinearCapacity = 1.87

    sub.mechanical.ApproximateWeight = 127.28
    sub.mechanical.grade = pb2.StringEditor.ItemDetails.Mechanical.Grade.g4145H_MOD
    sub.mechanical.MinimumYieldStrength = 758423.3
    sub.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.Material.mCS_API_5D_7
    sub.mechanical.YoungsMoudulus = 206842719.84
    sub.mechanical.PoissonsRatio = 0.30
    sub.mechanical.Density = 7849
    sub.mechanical.CoeffOfThermalExp = 12.42
    sub.mechanical.Connection = '4 1/2 REG'
    sub.mechanical.MakeupTorque = 31726.1

    sub.sub.ShankLength = 0.457
    sub.sub.ShankOD = 152.40

    item.Details.data = sub.SerializeToString()

    # 6 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.DrillPipe
    item.Details.Type = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Type.DrillPipe
    item.Details.Desc = 'Drill Pipe 5 in, 25.60 ppf, G, 5 1/2 FH, 1'

    drill = pb2.StringEditor.ItemDetails.DrillPipeDetailData()
    drill.general.Length = 83.310
    drill.general.BodyOD = 127.0
    drill.general.ClosedEndDisplacement = 12.67
    drill.general.BodyID = 101.60
    drill.general.LinearCapacity = 8.11

    drill.mechanical.ApproximateWeight = 43.68
    drill.mechanical.grade = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Grade.dpG
    drill.mechanical.MinimumYieldStrength = 723949.5
    drill.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.mCS_API_5D_7
    drill.mechanical.YoungsMoudulus = 206842719.84
    drill.mechanical.PoissonsRatio = 0.3
    drill.mechanical.Density = 7849
    drill.mechanical.CoeffOfThermalExp = 12.42
    drill.mechanical.Connection = '5 1/2 FH'
    drill.mechanical.MakeupTorque = 64035.3

    drill.StringItem.serviceClass = pb2.StringEditor.ItemDetails.DrillPipeDetailData.String.ServiceClass.sc1
    drill.StringItem.WallTickness = 100.0
    drill.StringItem.ConnectionOD = 184.15
    drill.StringItem.ConnectionID = 82.55
    drill.StringItem.AverageJointLength = 9.14
    drill.StringItem.TollJointLength = 0.433
    drill.StringItem.ConnectionTorsionalYield = 106725.9
    drill.StringItem.UltimateTensileStrength = 792897.1
    drill.StringItem.FatigueEnduranceLimit = 137895.1

    item.Details.data = drill.SerializeToString()

    # 7 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.Jar
    item.Details.Type = pb2.StringEditor.ItemDetails.JarDetailData.Type.MechanicalJar
    item.Details.Desc = 'Mechanical Jar, Dailey Mech., 6 1/4 in'

    jar = pb2.StringEditor.ItemDetails.JarDetailData()
    jar.general.Length = 9.870
    jar.general.BodyOD = 165.10
    jar.general.ClosedEndDisplacement = 21.41
    jar.general.BodyID = 57.15
    jar.general.LinearCapacity = 2.57

    jar.mechanical.ApproximateWeight = 147.16
    jar.mechanical.grade = pb2.StringEditor.ItemDetails.Mechanical.Grade.g4145H_MOD
    jar.mechanical.MinimumYieldStrength = 758423.3
    jar.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.mCS_API_5D_7
    jar.mechanical.YoungsMoudulus = 206842719.84
    jar.mechanical.PoissonsRatio = 0.3
    jar.mechanical.Density = 7849
    jar.mechanical.CoeffOfThermalExp = 12.42
    jar.mechanical.Connection = '4 1/2 IF'
    jar.mechanical.MakeupTorque = 29150.1

    jar.jar.DownSetForce = 0.0
    jar.jar.UpTripForce = 0.0
    jar.jar.DownTripForce = 0.0
    jar.jar.PumpOpenForce = 0.0
    jar.jar.SealFrictionForce = 0.0

    item.Details.data = jar.SerializeToString()

    # 8 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.DrillPipe
    item.Details.Type = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Type.DrillPipe
    item.Details.Desc = 'Drill Pipe 5 in, 25.60 ppf, G, 5 1/2 FH, 1'

    drill = pb2.StringEditor.ItemDetails.DrillPipeDetailData()
    drill.general.Length = 55.520
    drill.general.BodyOD = 127.0
    drill.general.ClosedEndDisplacement = 12.67
    drill.general.BodyID = 76.20
    drill.general.LinearCapacity = 4.56

    drill.mechanical.ApproximateWeight = 72.03
    drill.mechanical.grade = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Grade.dpG
    drill.mechanical.MinimumYieldStrength = 723949.5
    drill.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.mCS_API_5D_7
    drill.mechanical.YoungsMoudulus = 206842719.84
    drill.mechanical.PoissonsRatio = 0.3
    drill.mechanical.Density = 7849
    drill.mechanical.CoeffOfThermalExp = 12.42
    drill.mechanical.Connection = '5 1/2 FH'
    drill.mechanical.MakeupTorque = 58964.5

    drill.StringItem.serviceClass = pb2.StringEditor.ItemDetails.DrillPipeDetailData.String.ServiceClass.sc1
    drill.StringItem.WallTickness = 100.0
    drill.StringItem.ConnectionOD = 184.15
    drill.StringItem.ConnectionID = 88.90
    drill.StringItem.AverageJointLength = 9.14
    drill.StringItem.TollJointLength = 0.433
    drill.StringItem.ConnectionTorsionalYield = 98273.8
    drill.StringItem.UltimateTensileStrength = 792897.1
    drill.StringItem.FatigueEnduranceLimit = 137895.1

    item.Details.data = drill.SerializeToString()

    # 9 -- item
    item = s.stringItem.Items.add()
    item.Type = pb2.StringEditor.SectionType.DrillPipe
    item.Details.Type = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Type.DrillPipe
    item.Details.Desc = 'Drill Pipe 5 in, 25.60 ppf, G, 5 1/2 FH, 1'

    drill = pb2.StringEditor.ItemDetails.DrillPipeDetailData()
    drill.general.Length = 55.520
    drill.general.BodyOD = 127.0
    drill.general.ClosedEndDisplacement = 12.67
    drill.general.BodyID = 108.61
    drill.general.LinearCapacity = 9.26

    drill.mechanical.ApproximateWeight = 29.01
    drill.mechanical.grade = pb2.StringEditor.ItemDetails.DrillPipeDetailData.Grade.dpG
    drill.mechanical.MinimumYieldStrength = 723949.5
    drill.mechanical.material = pb2.StringEditor.ItemDetails.Mechanical.mCS_API_5D_7
    drill.mechanical.YoungsMoudulus = 206842719.84
    drill.mechanical.PoissonsRatio = 0.3
    drill.mechanical.Density = 7849
    drill.mechanical.CoeffOfThermalExp = 12.42
    drill.mechanical.Connection = 'NC50(XH)'
    drill.mechanical.MakeupTorque = 42064.3

    drill.StringItem.serviceClass = pb2.StringEditor.ItemDetails.DrillPipeDetailData.String.ServiceClass.sc1
    drill.StringItem.WallTickness = 100.0
    drill.StringItem.ConnectionOD = 168.28
    drill.StringItem.ConnectionID = 82.55
    drill.StringItem.AverageJointLength = 9.14
    drill.StringItem.TollJointLength = 0.433
    drill.StringItem.ConnectionTorsionalYield = 70106.6
    drill.StringItem.UltimateTensileStrength = 792897.1
    drill.StringItem.FatigueEnduranceLimit = 137895.1

    item.Details.data = drill.SerializeToString()

def CreateMudDetails(m : pb2.FluidsEditor.MudDetails):
    m.Name = '泥浆#1'
    #m.Desc = ''
    m.Density = 1890

    m.fluidComposition.mudBaseType = pb2.FluidsEditor.MudDetails.MudBaseType.Oil
    m.fluidComposition.baseFluid.base = pb2.FluidsEditor.MudDetails.BaseFluid.BaseOil.Diesel

    '''
    m.fluidComposition.baseFluid.data.OilContent_Vol = 2.2
    m.fluidComposition.baseFluid.data.WaterContent_Vol = 3.3
    m.fluidComposition.baseFluid.data.SaltContext_Wt = 4.4
    m.fluidComposition.baseFluid.data.ReferenceTemperature = 5.5
    m.fluidComposition.baseFluid.data.AverageSolidsGravity = 6.6
    '''
    rly = pb2.FluidsEditor.RheologyTests.RheologyTestsDetails.BinghamPlasticRheologyMsg()
    rly.PlasticViscosity = 24.00
    rly.YieldPoint = 5.746

    m.rheology.Temperature = 21.111
    m.rheology.Pressure = 101.35
    m.rheology.details.Rheology = rly.SerializeToString()

def CreateSpacerDetails(s : pb2.FluidsEditor.SpacerDetails):
    s.Name = 'ertret'
    s.Desc = 'dfghdfg'
    s.Density = 3.3

def CreateCementDetails(c : pb2.FluidsEditor.CementDetails):
    c.Name = 'sdfgsdf'
    c.Desc = 'wertwert'
    c.Density = 4.4

    c.cementProperties.clazz = pb2.FluidsEditor.CementDetails.CementProperties.Class.ClassH
    c.cementProperties.Yield = 3.3
    c.cementProperties.WaterRequirement = 5.5

def CreateGasDetails(g : pb2.FluidsEditor.GasDetails):
    g.Name = 'retwer'
    g.Desc = 'ewrtwer'
    g.gasProperties.UserDefined = True
    g.gasProperties.MoleWeigth = 3.3
    g.gasProperties.SpecificHeatRatio = 3.3
    g.gasProperties.Viscosity = 4.4
    g.gasProperties.CriticalPressure = 5.5
    g.gasProperties.CriticalTemperature = 6.6
    g.gasProperties.Gas_SpecificGravity = 7.7

    c = g.gasProperties.Components.add()
    c.gas = pb2.FluidsEditor.GasDetails.GasProperties.Gas._nHexane_C6H14
    c.MixturePercentage = 20
    c = g.gasProperties.Components.add()
    c.gas = pb2.FluidsEditor.GasDetails.GasProperties.Gas._2_2_DiMethylPentane_C7H16
    c.MixturePercentage = 20
    c = g.gasProperties.Components.add()
    c.gas = pb2.FluidsEditor.GasDetails.GasProperties.Gas._TriPtane_C8H18
    c.MixturePercentage = 20
    c = g.gasProperties.Components.add()
    c.gas = pb2.FluidsEditor.GasDetails.GasProperties.Gas._Benzene_C6H6
    c.MixturePercentage = 20
    c = g.gasProperties.Components.add()
    c.gas = pb2.FluidsEditor.GasDetails.GasProperties.Gas._Air_N2O2
    c.MixturePercentage = 20


def CreateFluidsEditor(f : pb2.FluidsEditor):
    CreateMudDetails(f.mudDetails.add())
    #CreateSpacerDetails(f.spacerDetails.add())
    #CreateCementDetails(f.cementDetails.add())
    #CreateGasDetails(f.gasDetails.add())

def CreateSubsurfaceEditor(s : pb2.SubsurfaceEditor):
    s.poreFirstEMW = 998
    s.geothermalGradient.standardProfile.SurfaceAmbient = 25.0
    s.geothermalGradient.standardProfile.AtWellTVD = -17.778



def CreateRigEquipment(re : pb2.RigEquipment):
    #re.mechanicalLimits.EnableBlockRating = True
    #re.mechanicalLimits.EnableTorqueRating = True

    #1 mud pumps
    item = re.circulatingSystem.mudPumps.add()
    item.enable = True
    item.pumpName = 'Continental Emsco - FB-1600 - TR'
    item.VolumePerStroke = 0.014016
    item.MaximumSpeed = 130.0
    item.MaxDischargePressure = 34473.79
    item.HorsepowerRating = 1193.60
    item.VolumePerStroke = 100

    # 2 mud pumps
    item = re.circulatingSystem.mudPumps.add()
    item.enable = True
    item.pumpName = 'National - FD-1600 - TRIPLEX'
    item.VolumePerStroke = 0.014016
    item.MaximumSpeed = 130.0
    item.MaxDischargePressure = 34473.79
    item.HorsepowerRating = 1193.60
    item.VolumePerStroke = 100

def CreateOperations(op : pb2.OperationalParameters):
    op.tdNormalAnalysis.trippingOut.Speed = 18.29
    op.tdNormalAnalysis.trippingIn.Speed = 18.29
    op.tdHybridModel.UnknownParameter = False

def CreateAnalysis(an : pb2.AnalysisSetting):
    an.common.PumpRate = 1.920
    an.torqueDrag.hookload.BlockWeight = 320.0
    an.torqueDrag.stringAnalysis.UseStiffString = True
    an.torqueDrag.stringAnalysis.BucklingLimitFactor = 1.0
    an.torqueDrag.overpull.UsingOfYield = 90.0

def CreateTaskList():
    taskList = pb2.TaskList()
    CreateCase(taskList.case)

    CreateWellpathEditor(taskList.wellPathEditor)

    CreateHoleSectionEditor(taskList.holeSectionEditor)

    CreateStringEditor(taskList.stringEditor)

    CreateFluidsEditor(taskList.fluidsEditor)

    CreateSubsurfaceEditor(taskList.subsurfaceEditor)

    CreateRigEquipment(taskList.rigEquipment)
    #taskList.barTab.general.plots.append(0)

    CreateOperations(taskList.operational)

    CreateAnalysis(taskList.analysisSetting)

    return taskList
