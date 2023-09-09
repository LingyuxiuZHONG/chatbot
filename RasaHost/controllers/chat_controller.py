"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
from rasa import train
from RasaHost import host
import os
from rasa.core.agent import Agent
from rasa.utils import endpoints
app = host.flask

@app.route('/chat')
def chat():
    return render_template(
        'chat/index.html',
        title='Chat'
    )
@app.route('/api/train',methods=['POST'])
def trainModel():
    current_dir = '/Users/zhonglingyuxiu/Desktop/chatbot/chatbot/'
    models_path = os.path.join(current_dir,'database')

    config_file = os.path.join(current_dir, "config.yml")
    training_data_dir = os.path.join(current_dir, "data")
    domain_file = os.path.join(current_dir, "domain.yml")
    train(
        domain=domain_file,
        config=config_file,
        training_files=training_data_dir,
        output=models_path
    )

    endpoints_path = os.path.join(current_dir,"endpoints.yml")
    action_endpoint_conf = endpoints.read_endpoint_config(endpoints_path, endpoint_type="action_endpoint")

    # 获取文件夹中所有文件的列表
    file_list = os.listdir(models_path)
    # 根据文件的创建时间进行排序
    sorted_files = sorted(file_list, key=lambda x: os.path.getctime(os.path.join(models_path, x)))
    # 返回最新创建的文件路径
    newest_file = sorted_files[-1]
    newest_model_path = os.path.join(models_path, newest_file)
    host.agent = Agent.load(newest_model_path,action_endpoint=action_endpoint_conf)
    print('Success!')
    return jsonify({'message': 'Train successfully'})