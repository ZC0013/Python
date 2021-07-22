# -*- coding: utf-8 -*-
import base64
import json
import time

import protocol.wellplan_pb2 as pb2
import queue
import threading

from loguru import logger
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from network import handler
from wellplan import WellPlanState

state = WellPlanState()
callback = dict()

stop = False
lock = threading.Lock()

que = queue.Queue()
que_lock = threading.Lock()


def isStop() -> bool:
    with lock:
        return stop


def processBinary(conn: WebSocket, dataBinary: bytearray) -> bool:
    reqInfo = json.loads(dataBinary)
    if reqInfo is None:
        logger.info('解析失败: 请求数据不能被解析为json对象')
        return False

    method = reqInfo.get(handler.METHOD)
    reqId = reqInfo.get(handler.REQ_ID)
    data = reqInfo.get(handler.DATA)

    if method is None or \
            reqId is None or \
            data is None:
        return False

    if not isinstance(method, str):
        logger.info('请求字段 {} 不为字符串.', handler.METHOD)
        return False

    if not isinstance(reqId, str):
        logger.info('请求字段 {} 不为字符串.', handler.REQ_ID)
        return False

    if not isinstance(data, str):
        logger.info('请求字段 {} 不为字符串.', handler.DATA)
        return False

    func = callback.get(method)
    if func is None:
        logger.info('未找到 {} 请求方法对应的响应处理.', method)
        return False

    rawData = base64.b64decode(data)

    return func(conn, reqId, rawData)


def put(conn, data):
    with que_lock:
        sz = que.qsize()
        que.put((conn, data))
        if conn is not None:
            sendStatus(conn, str(sz), 1)


def run():
    global stop
    while True:
        conn = None
        data = None
        sz = 0
        with que_lock:
            if que.empty() is False:
                conn, data = que.get(timeout=1)
                sz = que.qsize()

        if data and conn:
            sendStatus(conn, str(sz), 1)

            result = False
            try:
                result = processBinary(conn, data)
            except Exception as e:
                logger.exception(e)
            finally:
                if not result:
                    logger.info('断开远程连接: 不正确的处理结果')
                    conn.close()
                    cleanUpCmd()
        with lock:
            if stop:
                cleanUpCmd()
                stop = False

        time.sleep(1)


class WellMsgServer(WebSocket):
    def processText(self, dataText: str) -> bool:
        return False

    def handleMessage(self):
        put(self, self.data)

    def handleConnected(self):
        request = handler.initMessage('/syncData')
        encryptData = handler.serialized(request)
        # 发送 同步数据 指令
        self.sendMessage(encryptData)

    def handleClose(self):
        global stop
        global que
        with lock, que_lock:
            stop = True
            que = queue.Queue()


# 启动软件
# 登陆软件
def launchCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 launchCmd 指令')

    logger.info('开始启动处理软件')
    state.on_open(conn)
    logger.info('启动处理软件完毕')
    logger.info('开始登陆处理软件')
    state.on_loginUser(conn)
    logger.info('登陆处理软件完毕')

    logger.info('launchCmd 指令处理完毕')
    return True


# 填写信息
def projectInfoCmd(conn: WellMsgServer, reqId: str, data) -> bool:
    logger.info('开始处理 projectInfoCmd 指令')
    c = pb2.NewCase()
    logger.info('开始解析项目信息')
    c.ParseFromString(data)
    logger.info('开始解析项目信息完毕')

    state.setCast(c)

    logger.info('开始填写项目信息')
    state.on_createProject(conn)
    logger.info('填写项目信息完毕')
    logger.info('projectInfoCmd 指令处理完毕')
    return True


# 选择指标
def indicatorCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 indicatorCmd 指令')
    bar = pb2.BarTab()
    logger.info('开始解析指标信息')
    bar.ParseFromString(data)
    logger.info('解析指标完毕')

    state.setBarTab(bar)

    logger.info('开始初始化界面布局')
    state.on_initLayout(conn)
    logger.info('初始化界面布局完毕')
    logger.info('indicatorCmd 指令处理完毕')
    return True


# 填写【井轨迹】
def wellPathItemCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 wellPathItemCmd 指令')
    wellpath = pb2.WellpathEditor()
    logger.info('开始解析 井轨迹 信息')
    wellpath.ParseFromString(data)
    logger.info('解析 井轨迹 完毕')

    state.setWellPathEditor(wellpath)
    logger.info('开始填写 井轨迹')
    state.wellPathItemProcess(conn)
    logger.info('填写 井轨迹 完毕')
    logger.info('wellPathItemCmd 指令处理完毕')
    return True


# 填写【井身】
def holeSectionItemCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 holeSectionItemCmd 指令')
    holeSection = pb2.HoleSectionEditor()
    logger.info('开始解析 井身 信息')
    holeSection.ParseFromString(data)
    logger.info('解析 井身 完毕')

    state.setHoleSectionEditor(holeSection)
    logger.info('开始填写 井身')
    state.holeSectionItemProcess(conn)
    logger.info('填写 井身 完毕')
    logger.info('holeSectionItemCmd 指令处理完毕')
    return True


# 填写【管柱】
def stringItemCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 stringItemCmd 指令')
    stringItem = pb2.StringEditor()
    logger.info('开始解析 管柱 信息')
    stringItem.ParseFromString(data)
    logger.info('解析 管柱 完毕')

    state.setStringItem(stringItem)
    logger.info('开始填写 管柱')
    state.stringItemProcess(conn)
    logger.info('填写 管柱 完毕')
    logger.info('stringItemCmd 指令处理完毕')
    return True


# 填写【流体】
def fluidsItemCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 fluidsItemCmd 指令')
    fluidsItem = pb2.FluidsEditor()
    logger.info('开始解析 流体 信息')
    fluidsItem.ParseFromString(data)
    logger.info('解析 流体 完毕')
    state.setFluidsItem(fluidsItem)
    logger.info('开始填写 流体')
    state.fluidsItemProcess(conn)
    logger.info('填写 流体 完毕')
    logger.info('fluidsItemCmd 指令处理完毕')
    return True


# 填写【地层】
def subsurfaceCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 subsurfaceCmd 指令')
    subsurfaceItem = pb2.SubsurfaceEditor()
    logger.info('开始解析 地层 信息')
    subsurfaceItem.ParseFromString(data)
    logger.info('解析 地层 完毕')

    state.setSubsurfaceItem(subsurfaceItem)
    logger.info('开始填写 地层')
    state.subsurfaceProcess(conn)
    logger.info('填写 地层 完毕')
    logger.info('subsurfaceCmd 指令处理完毕')
    return True


# 填写【钻井平台】
def rigEquipmentCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 rigEquipmentCmd 指令')
    rigEquipmentItem = pb2.RigEquipment()
    logger.info('开始解析 钻井平台 信息')
    rigEquipmentItem.ParseFromString(data)
    logger.info('解析 钻井平台 完毕')
    state.setRigEquipmentItem(rigEquipmentItem)
    logger.info('开始填写 钻井平台')
    state.rigEquipmentProcess(conn)
    logger.info('填写 钻井平台 完毕')
    logger.info('rigEquipmentCmd 指令处理完毕')
    return True


# 填写【作业】
def operationalCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 operationalCmd 指令')
    operationalItem = pb2.OperationalParameters()
    logger.info('开始解析 作业 信息')
    operationalItem.ParseFromString(data)
    logger.info('解析 作业 完毕')
    state.setOperationalItem(operationalItem)
    logger.info('开始填写 作业')
    state.operationalProcess(conn)
    logger.info('填写 作业 完毕')
    logger.info('operationalCmd 指令处理完毕')
    return True


# 填写【分析设置】
def analysisCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 analysisCmd 指令')
    analysisItem = pb2.AnalysisSetting()
    logger.info('开始解析 分析设置 信息')
    analysisItem.ParseFromString(data)
    logger.info('解析 分析设置 完毕')
    state.setAnalysisItem(analysisItem)
    logger.info('开始填写 分析设置')
    state.analysisProcess(conn)
    logger.info('填写 分析设置 完毕')
    logger.info('analysisCmd 指令处理完毕')
    return True


# 主动处理 表格数据发送 和 清理资源

'''
METHOD = "method"
REQ_ID = "reqID"
CODE = "code"
MESSAGE = "message"
DATA = "data"
'''


# 获取表格数据
def getDataCmd(conn: WellMsgServer, reqId: str, data: str) -> bool:
    logger.info('开始处理 getDataCmd 指令')
    bar = None
    if len(data) > 0:
        bar = pb2.BarTab()
        bar.ParseFromString(data)

    isErr, data = state.on_outProcess(bar, conn)
    resp = None
    if isErr:
        assert isinstance(data, list)
        errText = '\r\n'
        errText = errText.join(data)

        # 错误代码设置为 1, 默认为 0
        resp = handler.initMessage('/gridsdata', reqId, errText, 1)
    else:
        resp = handler.initMessage('/gridsdata', reqId, data)

    encryptData = handler.serialized(resp)
    conn.sendMessage(encryptData)
    logger.info('getDataCmd 指令处理完毕')
    return True


# 清理资源
def cleanUpCmd(conn: WellMsgServer = None, reqId: str = '', data: str = '') -> bool:
    logger.info('开始处理 cleanUpCmd 指令')
    try:
        state.on_resource(conn)
    except:
        pass
    state.reinit()
    logger.info('cleanUpCmd 指令处理完毕')
    return True


# 发送当前状态
def sendStatus(conn: WebSocket, text: str, code=0):
    resp = handler.initMessage('/status', '0', text, code)
    encryptData = handler.serialized(resp)
    conn.sendMessage(encryptData)
    logger.info('status: {}, {}'.format(text, code))


# 启动软件
# 登陆软件
callback["launchCmd"] = launchCmd
# 创建项目
callback["projectInfoCmd"] = projectInfoCmd
# 选择指标
callback["indicatorCmd"] = indicatorCmd
# 填写【井轨迹】
callback["wellPathItemCmd"] = wellPathItemCmd
# 填写【井身】
callback["holeSectionItemCmd"] = holeSectionItemCmd
# 填写【管柱】
callback["stringItemCmd"] = stringItemCmd
# 填写【流体】
callback["fluidsItemCmd"] = fluidsItemCmd
# 填写【地层】
callback["subsurfaceCmd"] = subsurfaceCmd
# 填写【钻井平台】
callback["rigEquipmentCmd"] = rigEquipmentCmd
# 填写【作业】
callback["operationalCmd"] = operationalCmd
# 填写【分析设置】
callback["analysisCmd"] = analysisCmd

# # 获取表格数据
callback["getDataCmd"] = getDataCmd
# # 清理资源
callback["cleanUpCmd"] = cleanUpCmd
