#!/usr/bin/env python
from flask import Flask, request, jsonify
from commands.commands import GetResponse
import json

app = Flask(__name__)


@app.route('/')
@app.route('/rwconnector')
def rw_connector():
    x = GetResponse(request)
    return x.response, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route('/admin/sign/RWUnitTypeAction', methods=['POST', 'GET'])
def authentication():
    if request.method == 'POST':
        print('This is running')
        response = app.response_class(
            response=json.dumps({"status": "success", "code": 0, "data": {"Name": "Eyong", "Age": 30}}),
            status=200,
            mimetype='application/json'
        )
        return response
    if request.method == 'GET':
        print('This is a get.')
        return "Success", 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)