#from rasa_core import utils
import logging
from logging import StreamHandler
from RasaHost.database import *
import datetime
from flask import request, has_request_context
import flask
import sys
import traceback
import coloredlogs
import re
import uuid
import json
from RasaHost.logging import get_request_id, set_sender_id
from RasaHost import host
import asyncio
import logging
logger = logging.getLogger(__name__)

class ConversationsService:
    def __init__(self):
        pass

    def find(self, query):#用于在数据库中查询对话
        return DbContext().conversations.find(query)

    def save(self, sender_id, request, response, response_raw):
        #用于保存对话消息到数据库
        conversation = Conversation()
        conversation.request = request
        conversation.response = response
        conversation.response_raw = response_raw
        conversation.sender_id = sender_id
        conversation.request_id = get_request_id()
        conversation.created = datetime.datetime.utcnow()
        DbContext().conversations.save(conversation)

   
    def handle_message(self, *args, **kwargs):
            message = None
            text = None
            sender_id = None

            try:
                message = next(iter(args))
                if message:
                    text = message.text
                    sender_id = message.sender_id
                    set_sender_id(sender_id)
            except:
                e = "\n". join(traceback.format_exception(*sys.exc_info()))
                logger.error(e)

            try:
                
                output = host.agent.handle_message(*args, **kwargs)
                response = [(x["text"] if "text" in x else None) for x in output]
                response_raw = [{"text":x.get("text")} for x in output]

                self.save(sender_id=sender_id, 
                          request=text, 
                          response=json.dumps(response), 
                          response_raw=json.dumps(response_raw))

                return output
            except:
                e = "\n".join(traceback.format_exception(*sys.exc_info()))
                output = ([])
                response = [(x["text"] if "text" in x else None) for x in output]
                if len(response) == 0:
                    response = e
                response_raw = {}
                response_raw["output"] = [{"text":x.get("text")} for x in output]
                response_raw["error"] = e
                logger.error(e)
                self.save(sender_id=sender_id, 
                          request=message, 
                          response=json.dumps(response), 
                          response_raw=json.dumps(response_raw))
                raise

    def handle_text(self, message, sender_id=None):
        try:
            # 使用异步函数和 await 等待协程的执行结果
            async def handle_output():
                output = await host.agent.handle_text(message, sender_id=sender_id)
                response = [(x["text"] if "text" in x else None) for x in output]
                response_raw = [{"text":x.get("text")} for x in output]
                self.save(sender_id=sender_id,
                          request=message,
                          response=json.dumps(response),
                          response_raw=json.dumps(response_raw))
                print(output)
                return output
            return asyncio.run(handle_output())
        except:
            e = "\n".join(traceback.format_exception(*sys.exc_info()))
            response_raw = {}
            response_raw["error"] = e
            logger.error(e)
            self.save(sender_id=sender_id, 
                      request=message, 
                      response=e, 
                      response_raw=json.dumps(response_raw))
            raise



