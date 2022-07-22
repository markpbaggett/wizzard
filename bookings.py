#!/usr/bin/env python
from flask import Flask, request
from commands.commands import GetResponse

app = Flask(__name__)


@app.route('/')
@app.route('/rwconnector')
def rw_connector():
    x = GetResponse(request)
    return x.response, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route('/admin/sign/RWUnitTypeAction')
def authentication():
    if request.method == 'POST':
        print('This is running')
        return "Success", 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)