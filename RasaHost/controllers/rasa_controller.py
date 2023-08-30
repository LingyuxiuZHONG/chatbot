"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import logging
import sys
import traceback
import json
from RasaHost import host
app = host.flask
from RasaHost.services import ConversationsService
from RasaHost.database import *

logger = logging.getLogger(__name__)

@app.route("/conversations/<sender_id>/respond",methods = ['Post'])
def rasa_respond(sender_id):
    message = None
    try:
        message = request.json['q']
        output = ConversationsService().handle_text(message, sender_id=sender_id)
        print(output)
        response = jsonify(output)
        return response
    except:
        e = "\n". join(traceback.format_exception(*sys.exc_info()))
        logger.error(e)
        response = jsonify({"error": e})
        response.status_code = 400
        return response


@app.route("/actions", methods = ['GET', 'POST'])
def actions():
    action_call = request.json
    try:
        response = host.actionExecutor.run(action_call)
        return jsonify(response)
    except:
        e = "\n". join(traceback.format_exception(*sys.exc_info()))
        logger.error(e)
        response = jsonify({"error": e, "action_name": action_call})
        response.status_code = 400
        return response

    