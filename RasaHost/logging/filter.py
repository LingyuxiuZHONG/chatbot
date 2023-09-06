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
from RasaHost.logging.request_id import get_request_id
from RasaHost.logging.sender_id import get_sender_id

class LoggingFilter(logging.Filter):
    # 这个过滤器类的作用是为每条日志记录添加发送者 ID（sender_id）和请求 ID
    def filter(self, record):
        try:
            record.sender_id = get_sender_id(record.getMessage())
            record.request_id = get_request_id()
        except:
            return True
        return True