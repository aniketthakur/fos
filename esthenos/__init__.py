#!/usr/bin/python

#from flask_debugtoolbar import DebugToolbarExtension
#from flask.ext.mongoengine import  MongoEngineSessionInterface
import os
from datetime import timedelta
from num2words import num2words
from flask import Flask, redirect, session, render_template
from flask.ext.babel import Babel, gettext
from flask.ext.mongoengine import MongoEngine
from flask_login import  LoginManager
from werkzeug.contrib.fixers import ProxyFix

import boto
from boto.s3.connection import S3Connection

mainapp = Flask(__name__)
mainapp.wsgi_app = ProxyFix(mainapp.wsgi_app)
mainapp.url_map.strict_slashes = False
mainapp.config['MAX_CONTENT_LENGTH'] = 5024000
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
mainapp.config['DATA_ROOT'] = os.path.join(mainapp.config['ROOT'],'pitaya/data/')
mainapp.config['UPLOAD_FOLDER'] = os.path.join(mainapp.config['ROOT'],'pitaya/uploads')
mainapp.config.update(
    CELERY_BROKER_URL='amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks',
    CELERY_RESULT_BACKEND='amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks',#train.pixuate.com
)
mainapp.config.update(
    DEBUG = True,
    TESTING = False,
    MONGODB_SETTINGS = {
        'HOST': 'ds061228.mongolab.com',
        'PORT': 61228,
        'DB': 'saggrahadb',
        'USERNAME':'saggraha-user',
        'PASSWORD':'saggraha-password'
    },
)
mainapp.config.update(
    FEATURES = {
        "questions_grt": True,
        "questions_cgt1": True,
        "questions_cgt2": True,
        "questions_telecalling": True,
        "questions_psychometric": True,
        "reports": True,
        "scrutiny": True,
        "applications": True,
        "disbursement": True,
        "enroll_customers": False,
    }
)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.needs_refresh_message = u"To protect your account, please re-authenticate to access this page."
login_manager.needs_refresh_message_category = "info"
login_manager.init_app(mainapp)
mainapp.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=30)

LANGUAGES = {
    'en' : 'English'
}

babel = Babel(mainapp)
db = MongoEngine(mainapp)

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

def get_ses_conn():
    global conn
    if conn ==None:
        conn = boto.connect_ses(
            aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))
    return conn

@login_manager.user_loader
def load_user(userid):
    from e_admin.models import EsthenosUser
    user = EsthenosUser.objects(id=userid).first()
    if user is not None and not session.has_key('role') :
        if user.has_role("ADMIN"):
            session['role'] = "ADMIN"
    return user

@login_manager.unauthorized_handler
def unauthorized():
    session.clear()
    return redirect("/accounts/login")

@babel.localeselector
def get_locale():
    return 'en'# request.accept_languages.best_match(LANGUAGES.keys())

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

@mainapp.template_filter('num2words')
def _jinja2_filter_datetime(num):
    return num2words(num).upper()

@mainapp.template_filter('timeformat')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%H:%%M'))

@mainapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@mainapp.errorhandler(403)
def page_not_allowed(e):
    if session['role'].startswith("ORG_"):
        kwargs = {"redirect_url": "/" }
        return render_template('403.html', **kwargs), 403

    elif session['role'].startswith("ADMIN"):
        kwargs = {"redirect_url": "/admin/dashboard" }
        return render_template('403.html', **kwargs), 403

