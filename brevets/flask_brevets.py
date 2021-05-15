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
    app.logger.info("Got a JSON request")
    km = request.args.get('km', 0, type=float)  # control_disk_km
    brevet_dist_km = request.args.get("brevet_dist_km", 0, type=float)
    brevet_start_time = request.args.get("brevet_start_time", "2017-01-01T00:00:00",
                                         type=str)
    app.logger.info("km={}".format(km))
    app.logger.debug("brevet_dist_km={}".format(brevet_dist_km))
    app.logger.debug("brevet_start_time={}".format(brevet_start_time))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    open_time = acp_times.open_time(km, brevet_dist_km, brevet_start_time)
    print("This is open time in flask.py: {}".format(open_time))
    close_time = acp_times.close_time(km, brevet_dist_km, brevet_start_time)
    result = {"open": open_time, "close": close_time}
    app.logger.debug("Sending results: {}".format(result))
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
