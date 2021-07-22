# -*- coding: utf-8 -*-
import threading
from config import *
from loguru import logger
from SimpleWebSocketServer import SimpleWebSocketServer
from network import listener

if __name__ == '__main__':
    logger.add("log_{time}.log", rotation="4 MB", compression='tar.gz', enqueue=True)
    logger.info('初始化日志组件')

    if LAUNCH == None:
        logger.info('读取配置文件参数失败: launch')
        sys.exit(os.EX_NOTFOUND)

    if LAUNCH_ENV == None:
        logger.info('读取配置文件参数失败: launchEnv')
        sys.exit(os.EX_NOTFOUND)

    if REMOTE_ADDR == None:
        logger.info('读取配置文件参数失败: remoteAddr')
        sys.exit(os.EX_NOTFOUND)

    if RETRY_TIME == None:
        logger.info('读取配置文件参数失败: retryInterval')
        sys.exit(os.EX_NOTFOUND)

    server = SimpleWebSocketServer('0.0.0.0', 9999, listener.WellMsgServer)
    logger.info('初始化网络组件: {}', server.listeners)
    netThread = threading.Thread(target=server.serveforever)
    netThread.start()
    listener.run()
