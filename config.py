# -*- coding: utf-8 -*-

import argparse
import os, sys
from configparser import *

argParser = argparse.ArgumentParser()
argParser.add_argument('-cf', '--configfile', help='配置文件路径', default='cfg.conf')
args = argParser.parse_args()

configParser = ConfigParser()
configParser.read(args.configfile)

LAUNCH_ENV = configParser.get('main', 'launchEnv', fallback=None)
LAUNCH = configParser.get('main', 'launch', fallback=None)
REMOTE_ADDR = configParser.get('main', 'remoteAddr', fallback=None)
RETRY_TIME = configParser.getint('main', 'retryInterval', fallback=None)

MINUTE = 15

TEST_MODE = True
