"""
The flask application package.
"""

from os import environ
import os
import sys
import traceback
import logging
from flask import Flask
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)

class RasaHost:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    nlu_path = os.path.join(current_dir, "data/nlu/")
    stories_path = os.path.join(current_dir, "data/stories/")
    rules_path = os.path.join(current_dir,'data/rules/')
    domain_path = os.path.join(current_dir, "domain.yml")
    host = environ.get('SERVER_HOST', '0.0.0.0')
    port = 5555
    agent = None
    actionExecutor = None
    flask = None
    socketio = None

    try:
        port = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555

    def __init__(self):
        self.flask = Flask(__name__)
        # self.socketio = SocketIO(self.flask)

    def handle_message(self, *args, **kwargs):
        from RasaHost.services import ConversationsService
        return ConversationsService().handle_message(*args, **kwargs)

    def set_data_path(self, data_dir):
        self.nlu_path = os.path.join(data_dir, "data/nlu/")
        self.stories_path = os.path.join(data_dir, "data/stories/")
        self.domain_path = os.path.join(data_dir, "domain.yml")

    def enable_logging(self):
        from RasaHost.logging import enable
        enable()



    def run(self):
        import RasaHost.controllers
        self.enable_logging()
        self.flask.run(self.host, self.port)

host = RasaHost()
