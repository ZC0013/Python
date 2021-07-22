# -*- coding: utf-8 -*-
import base64
import json

METHOD = "method"
REQ_ID = "reqID"
CODE = "code"
MESSAGE = "message"
DATA = "data"


def initMessage(method, reqId='', data='', code=0) -> dict:
    obj = dict()
    obj[METHOD] = method
    obj[REQ_ID] = str(reqId)
    obj[DATA] = data
    obj[CODE] = code
    return obj


def serialized(obj: dict) -> bytes:
    jsonText = json.dumps(obj)
    return base64.b64encode(bytes(jsonText, encoding='utf-8'))