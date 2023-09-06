from logging import StreamHandler
import logging
from RasaHost.loggingDatabase import *
import datetime
from flask import request, has_request_context
import flask
import traceback
import coloredlogs
import re
import uuid

__all__ = ['LoggingDbHandler', 'LoggingFilter', 'LoggingSocketioHandler', 'get_request_id', 'get_sender_id',
           'set_sender_id']

from RasaHost.logging.db_handler import LoggingDbHandler
from RasaHost.logging.filter import LoggingFilter
from RasaHost.logging.socketio_handler import LoggingSocketioHandler
from RasaHost.logging.request_id import get_request_id
from RasaHost.logging.sender_id import get_sender_id, set_sender_id

log_level = 'DEBUG'


def enable():
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
    field_styles['asctime'] = {}
    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
    level_styles['debug'] = {}  # level：DEBUG、INFO、WARNING、ERROR 和 CRITICAL
    coloredlogs.install(  # 用于设置日志输出的格式和样式
        level=log_level,
        use_chroot=False,  # chroot--"Change Root"（改变根目录）
        # 它是一种操作系统的功能，允许在一个进程内部创建一个独立的文件系统环境，将指定的目录作为新的根目录，以此来限制进程的访问范围。
        fmt='%(asctime)s %(levelname)-8s %(name)s  - %(message)s',
        # %(asctime)s、%(levelname)-8s、%(name)s 和 %(message)s 中的 s 表示相应的占位符将会被字符串类型的值替换。
        level_styles=level_styles,
        field_styles=field_styles)

    dbHandler = LoggingDbHandler()
    dbHandler.setLevel(log_level)
    logging.getLogger().addHandler(dbHandler)
    logging.getLogger().addHandler(logging.FileHandler("logs.txt"))
    # logging.getLogger() 返回一个根日志记录器对象，你可以通过它来管理和配置整个日志系统。
    # 为日志系统添加了两个处理器，一个用于将日志记录存储到数据库，另一个用于将日志记录输出到文本文件。
    # logging.getLogger('werkzeug').addHandler(dbHandler)
    # socketio logging
    # logging.getLogger().addHandler(LoggingSocketioHandler())
    # file logging

    for handler in logging.getLogger().handlers:
        handler.setLevel(log_level)
        handler.addFilter(LoggingFilter())  # 过滤器可以用于对日志消息进行额外的过滤操作，从而控制哪些消息会被处理器处理。
        # handler.setFormatter(logging.Formatter("[%(sender_id)s] [%(asctime)s] [%(name)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    import requests.api
    def my_get(url, **kwargs):
        print('Hello World!')
        kwargs.setdefault('allow_redirects', True)  # 设置请求的默认选项 allow_redirects 为 True，以允许重定向。
        # kwargs 表示关键字参数字典。setdefault 是 Python 字典的方法，用于在字典中查找指定的键
        # 如果键存在则返回对应的值，如果键不存在则将键值对添加到字典中，并返回默认值。
        return requests.api.request('get', url, **kwargs)  # 调用 requests.api.request('get', url, **kwargs) 来实际发起 GET 请求。

    requests.api.get = my_get

    def my_post(url, **kwargs):
        print('Hello World!')
        kwargs.setdefault('allow_redirects', True)
        return requests.api.request('post', url, **kwargs)

    requests.api.post = my_post
    # logging.getLogger('socketio').setLevel(logging.INFO)
    # logging.getLogger('engineio').setLevel(logging.INFO)
    # logging.getLogger('werkzeug').setLevel(logging.INFO)


def set_log_level(self, log_level):
    self.log_level = log_level
    for handler in logging.getLogger().handlers:
        handler.setLevel(log_level)
