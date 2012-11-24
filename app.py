#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import hashlib
import flask
from flask import Flask, render_template, request
from raven.contrib.flask import Sentry
from babel.numbers import format_decimal
from libs.utils import getRSS

app = Flask(__name__)
launch_date = datetime.datetime.now()


@app.route('/')
def index():
    """Main page"""
    entries = getRSS('http://feeds2.feedburner.com/phollow/iuEO')
    return render_template('index.html', entries=entries)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/apple-touch-icon.png')
@app.route('/apple-touch-icon<format>.png')
def apple_touch(format=""):
    """Shitty logo Apple"""
    file = 'apple-touch-icon%s.png' % format
    return app.send_static_file(file)


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# caching stuff
@app.before_request
def handle_cache():
    """if resource is the same, return 304"""
    # we test Etag first, as it's a strong validator
    etag = hashlib.sha1(request.url).hexdigest()
    if request.headers.get('If-None-Match') == etag:
        return flask.Response(status=304)
    # then we try with Last-Modified
    if request.headers.get('If-Modified-Since') == str(launch_date):
        return flask.Response(status=304)


@app.after_request
def add_header(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 5 minutes. Should be served by
    Varnish servers.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=300'
    #response.headers['Last-Modified'] = launch_date
    return response


@app.template_filter()
def number_format(number):
    """Custom Jinja filter for adding a better number display, according
    to the locale
    """
    return format_decimal(number, locale='en_US')


# Sentry
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
if SENTRY_DSN:
    app.config['SENTRY_DSN'] = SENTRY_DSN
    sentry = Sentry(app)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
