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


def get_sender_id(message=None):
    if has_request_context():  # 检查是否存在请求上下文，即是否在 Flask 应用的请求处理过程中。
        if getattr(flask.g, 'sender_id', None):  # 如果 sender_id 已经存在于全局上下文中，则直接返回该值。
            return flask.g.sender_id
        sender_id = request.view_args[
            'sender_id'] if request and request.view_args and 'sender_id' in request.view_args else None
        # 尝试从 Flask 请求对象 request 中获取发送者的 ID。
        if sender_id:
            return sender_id
        sender_id = request.json['sender_id'] if request and request.json and 'sender_id' in request.json else None
        return sender_id
    else:
        if message:
            return next(iter(re.findall("/conversations/(.*)/[a-zA-Z]", message)), None)
        # /conversations/：这部分直接匹配字符 "/conversations/"。
        # (.*)：这部分使用括号将 .* 包裹起来，表示匹配任意数量的字符（除了换行符）。括号表示捕获组，可以将匹配到的内容提取出来。
        # [a-zA-Z]：这部分表示匹配一个字母，大小写不限
        # next(iter(...), None)：这部分代码将正则表达式匹配结果转换为迭代器
        # 并使用 next() 函数从迭代器中获取第一个匹配项。如果没有匹配项，返回 None。
        else:
            return None


def set_sender_id(sender_id):
    if has_request_context():
        flask.g.sender_id = sender_id
