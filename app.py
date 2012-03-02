#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template
#from middlewares.gzipper import Gzipper
from babel.numbers import format_decimal
from libs.utils import getRSS, getTwitterNbFollowers, getDribbbleShots
from libs.decorators import minified, cached

import logging, sys

app = Flask(__name__)


@app.route('/')
#@cached(60, 'index')
#@minified
def index():
    """Main page"""
    entries = getRSS('http://feeds2.feedburner.com/phollow/iuEO')     
    nb_followers = getTwitterNbFollowers('phollow') 
    dribbble_shots = getDribbbleShots('phollow')

    return render_template('index.html', **locals())


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/apple-touch-icon.png')
@app.route('/apple-touch-icon<format>.png')
def apple_touch(format=""):
    """Shitty logo Apple"""
    file = 'apple-touch-icon' + format + '.png'
    return app.send_static_file(file)

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 5 minutes. Should be served by
    Varnish servers.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response


@app.template_filter()
def number_format(number):
    """
    Custom Jinja filter for adding a better number display, according
    to the locale
    """
    return format_decimal(number, locale='en_US')


if __name__ == '__main__':
    app.debug = True
    # Gzipping, not worth it on my free Heroku cedar
    # Cloudflare will do it for me.
    # app.wsgi_app = Gzipper(app.wsgi_app, compresslevel=6)
    port = int(os.environ.get('PORT', 5000))
    # logging
    if not app.debug: 
        handler = logging.StreamHandler(sys.__stdout__) 
        handler.setLevel(logging.INFO) 
        app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=port)