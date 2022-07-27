#!/usr/bin/env python
from flask import Flask, request, jsonify
from commands.commands import GetResponse
import json
from flask_apscheduler import APScheduler
import arrow
from libcal.libcal import RoomBookings
from cache.libcal import LibCalCache

app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

all_current_bookings = LibCalCache(RoomBookings('10024', arrow.utcnow().format('YYYYMMDD')).get_bookings())


@scheduler.task('interval', id='libcal', seconds=900, misfire_grace_time=900)
def job2():
    """Updates the LibCal Cache that is passed to routes. Variable is a Borg Singleton that is garbage collected."""
    all_current_bookings_two = LibCalCache(RoomBookings('10024', arrow.utcnow().format('YYYYMMDD')).get_bookings())
    """Print current bookings to log."""
    print(all_current_bookings.current)


scheduler.start()


@app.route('/')
@app.route('/rwconnector')
def rw_connector():
    """Routes GET requests to root or /rwconnector.

    This route handles all traffic to / or /rwconnector. The route passes all HTTP parameters to the GetResponse in
    the commands package. Because of that, both about_connector and get_bookings routing is handled here.

    Returns:
        tuple: A tuple with the appropriate XML response from the related API at index 0, 200 at index 1, and a dict
        specifying the content type of the response at index 2.

    """
    x = GetResponse(request, all_current_bookings.current)
    return x.response, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route('/admin/sign/RWUnitTypeAction', methods=['POST'])
def authentication():
    """Routes POST requests to the expected authentication endpoint for validation.

        This route handles all POST traffic to /admin/sign/RWUnitTypeAction. Since we do not use authentication, the
        response is always a Flask Response with a JSON success message, a status code of 200, and a mimetype of
        'application/json'.

        Returns:
            flask.wrappers.Response: a Flask Response with a JSON success message, a status code of 200, and a mimetype
            of 'application/json'

        """
    response = app.response_class(
        response=json.dumps({"status": "success", "code": 0, "data": {"Success": True}}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)