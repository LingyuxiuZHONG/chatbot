import logging
from logging import StreamHandler
from RasaHost.loggingDatabase import *
import datetime
from flask import request, has_request_context
import flask
import traceback
import coloredlogs
import re
import uuid

def get_request_id():
    if has_request_context():
        if getattr(flask.g, 'request_id', None):
            return flask.g.request_id
        original_request_id = flask.request.headers.get("X-Request-Id")
        request_id = original_request_id if original_request_id else str(uuid.uuid4())
        # 如果从请求头中获取到了 "X-Request-Id"，则使用该值作为请求 ID；否则，生成一个新的 UUID 作为请求 ID。
        flask.g.request_id = request_id
        return flask.g.request_id
    else:
        return None
