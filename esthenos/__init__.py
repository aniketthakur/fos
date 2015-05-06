#!/usr/bin/python
# vim: set expandtab:

from flask import Flask,redirect,session
from flask.ext.mongoengine import MongoEngine
#from flask_debugtoolbar import DebugToolbarExtension
#from flask.ext.mongoengine import  MongoEngineSessionInterface
import os,sys

sys.path.insert(0,os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../esthenos"))

mainapp = Flask(__name__)
mainapp.config['MAX_CONTENT_LENGTH'] = 5024000
from werkzeug.contrib.fixers import ProxyFix
mainapp.wsgi_app = ProxyFix(mainapp.wsgi_app)

mainapp.url_map.strict_slashes = False
mainapp.config['DEBUG'] = True
mainapp.config.update(
    DEBUG = True,
    TESTING = False,
    MONGODB_SETTINGS = {
        'HOST': '128.199.156.24',#
        'PORT': 27017,
        'USERNAME':'hindustan',
        'PASSWORD':'Ofn2cXHkTMQ8LE',
        #'DB': 'pitaya_local',
        #'DB': 'esthenos_test_v1',
        'DB': 'hindustan_v1',
        "w":1,
        "j":True,
        #'replicaset':"rs0"
    },
)

#mongoengine as session store
db = MongoEngine(mainapp)
#mainapp.session_interface = MongoEngineSessionInterface(db)
mainapp.config['MAX_CONTENT_LENGTH'] = 5024000
from werkzeug.contrib.fixers import ProxyFix
mainapp.wsgi_app = ProxyFix(mainapp.wsgi_app)
"""

    """
mainapp.url_map.strict_slashes = False
mainapp.config['SERVER_EMAIL'] = "support@esthenos.com"
mainapp.config['MIN_IMAGE_DIMENSION'] = 300
mainapp.config["region_list"] = ['us-east-1','us-west-1','us-west-2']
mainapp.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

mainapp.config['AWS_S3_BUCKET_DIRECT'] = 'esthenos'

mainapp.config["AWS_ACCESS_KEY_ID"] = 'AKIAITWBEHC2SAGDFQSA'

mainapp.config["AWS_SECRET_ACCESS_KEY"] = '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'

mainapp.config["SECRET_KEY"] = "^udtr!d^_vw22_+a=f1*au01xn(adtyce7^5k5ndkf6e%2z%aq"

mainapp.config["USER_MODEL_CLASS"] = "e_admin.models.EsthenosUser"

mainapp.config['ROOT'] = os.curdir
print mainapp.config['ROOT']
mainapp.config['UPLOAD_FOLDER'] = os.path.join(mainapp.config['ROOT'],'pitaya/uploads')
mainapp.config['DATA_ROOT'] = os.path.join(mainapp.config['ROOT'],'pitaya/data/')

mainapp.config.update(
    CELERY_BROKER_URL='amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks',
    CELERY_RESULT_BACKEND='amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks',#train.pixuate.com
)
from boto.s3.connection import S3Connection
connection = None
def get_s3_connection():
    global connection
    if connection == None:
        connection = S3Connection(mainapp.config['AWS_ACCESS_KEY_ID'], mainapp.config['AWS_SECRET_ACCESS_KEY'])
    return connection
bucket = None
def s3_bucket():
    global bucket
    if bucket == None:
        conn = get_s3_connection()
        bucket = conn.lookup('esthenos')
    return bucket

from esthenos.job import *

import boto
def get_ses_conn():
    global conn
    if conn ==None:
        conn = boto.connect_ses(
            aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))
    return conn
#DEBUG_TB_PANELS = ['flask.ext.mongoengine.panels.MongoDebugPanel']
#toolbar = DebugToolbarExtension(mainapp)
from datetime import timedelta
from flask_login import  LoginManager
login_manager = LoginManager()
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
    )
login_manager.needs_refresh_message_category = "info"
#login_manager.session_protection = "basic"
login_manager.session_protection = "strong"
mainapp.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=30)


@login_manager.user_loader
def load_user(userid):
    from e_admin.models import EsthenosUser
    user = EsthenosUser.objects(id=userid).first()
    if user is not None and not session.has_key('role') :
        print "In load user"
        if user.has_role("ADMIN"):
            session['role'] = "ADMIN"
    return user

@login_manager.unauthorized_handler
def unauthorized():
    print "unauthorised"
    session.clear()
    return redirect("/accounts/login")

login_manager.init_app(mainapp)

#loading templates with jinga
import jinja2
template_dir = os.path.join(mainapp.config['ROOT'], '../p_user/templates')
my_loader = jinja2.ChoiceLoader([
    mainapp.jinja_loader,
    jinja2.FileSystemLoader(template_dir),
    ])
mainapp.jinja_loader = my_loader
import  dateutil

from flask.ext.babel import Babel
babel = Babel(app)
# -*- coding: utf-8 -*-
# ...
# available languages
LANGUAGES = {
    'en': 'English'
}

@babel.localeselector
def get_locale():
    return 'en'# request.accept_languages.best_match(LANGUAGES.keys())

import datetime
from flask.ext.babel import gettext

@mainapp.template_filter('dateformat')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%d/%%m/%%Y'))

@mainapp.template_filter('fulldayformat')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%A'))


@mainapp.template_filter('timeformat')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%H:%%M'))


################ends ################
from flask import render_template
@mainapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

