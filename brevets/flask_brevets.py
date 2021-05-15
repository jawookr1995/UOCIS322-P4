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
    flask.session['linkback'] = flask.url_for("index")
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
    app.logger.debug("Got a JSON request")
    json_dict = request.args  # Get the whole dictionary from request.args.
    app.logger.debug("request.args: {}".format(request.args))

    km = int(json_dict['km']) or 0  # Extract the Control
    brevet_dist = int(json_dict['brevet_dist']) or 200  # Extract the whole brevet distance
    # Extract brevet begin time.
    brevet_begin = json_dict['brevet_begin'] or arrow.now().isoformat()

    # Use Fail if input is too large.
    open_time = acp_times.open_time(km, brevet_dist, brevet_begin) or "Fail"
    close_time = acp_times.close_time(km, brevet_dist, brevet_begin) or "Fail"

    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
