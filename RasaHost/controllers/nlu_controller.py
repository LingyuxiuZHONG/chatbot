"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import os;

from RasaHost import host
app = host.flask
from RasaHost.services import NluService


@app.route('/nlu')
def nlu_list():
    return render_template(
        'nlu/index.html',
        title='Nlu',
    )

@app.route('/api/nlu', methods=['GET'])
def api_nlu_list():
    q = request.args.get('q')
    #Flask中用于从URL查询字符串中获取特定参数值的方法。
    intents = NluService().find_all(q)
    return jsonify(intents)

@app.route('/api/nlu/file', methods=['GET'])
def api_nlu_get():
    path = request.args.get('path')
    intent = NluService().get_by_path(path)

    # domain_path = "/Users/zhonglingyuxiu/Desktop/docDemo/domain.yml"
    # name = request.json["name"]
    # str = "\n  - " + name
    # print(name)
    # file = open(domain_path, "r")
    # content = file.read()
    # pos = content.find("intents:") + len("intents:")
    # if pos != -1:
    #     content = content[:pos] + str + content[pos:]
    #     file = open(domain_path, "w")
    #     file.write(content)
    #     file.close()

    return jsonify(intent)

@app.route('/api/nlu/file', methods=['POST'])
def api_nlu_post():
    path = request.args.get('path')
    if not request.json["name"]:
        return jsonify({'error': 'Name is required'})
    
    newPath = os.path.join(os.path.dirname(path), request.json['name']  + ".yml")
    if path.lower() != newPath.lower() and os.path.exists(newPath):
        return jsonify({'error': 'File with the name already exists'})

    updated_file = NluService().update(path, request.json)



    return jsonify({'result': updated_file})

@app.route('/api/nlu/file', methods=['PUT'])
def api_nlu_put():
    if not request.json["name"]:
        return jsonify({'error': 'Name is required'})

    if NluService().get_by_name(request.json["name"]):
        return jsonify({'error': 'File with the name already exits.'})

    created_file = NluService().create(request.json)
    return jsonify({'result': created_file})

@app.route('/api/nlu/file', methods=['DELETE'])
def api_nlu_delete():
    path = request.args.get('path')
    NluService().delete(path)
    return jsonify({'result': 'ok'})

