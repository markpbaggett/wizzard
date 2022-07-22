#!/usr/bin/env python
from flask import Flask, request
from commands.commands import AboutConnector

app = Flask(__name__)


@app.route('/')
@app.route('/rwconnector')
def rw_connector():
    command = request.args.get('command', default='about_connector')
    time_zone = request.args.get('time_zone', default='US/Eastern')
    x = AboutConnector(time_zone)
    return x.response, 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)