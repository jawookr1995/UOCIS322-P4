"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request");

    # Get args
    km = request.args.get('km', 0, type=float)
    distance = request.args.get('distance', 0, type=float)
    date = request.args.get('date', 0, type=str)
    time = request.args.get('time', 0, type=str)

    # format date_time
    date_time = date + ' ' + time + ':00'
    arrow_time = arrow.get(date_time, 'YYYY-MM-DD HH:mm:ss')

    open_time = acp_times.open_time(km, distance, arrow_time.isoformat())
    close_time = acp_times.close_time(km, distance, arrow_time.isoformat())
    result = {"open": open_time, "close": close_time}

    return jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
