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
import settings
from boto.s3.connection import S3Connection

mainapp = Flask(__name__)
mainapp.wsgi_app = ProxyFix(mainapp.wsgi_app)
mainapp.url_map.strict_slashes = False
mainapp.config['MAX_CONTENT_LENGTH'] = 5024000
mainapp.config['SERVER_EMAIL'] = "support@esthenos.com"
mainapp.config['MIN_IMAGE_DIMENSION'] = 300
mainapp.config["SECRET_KEY"] = "^udtr!d^_vw22_+a=f1*au01xn(adtyce7^5k5ndkf6e%2z%aq"
mainapp.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
mainapp.config["USER_MODEL_CLASS"] = "e_organisation.models.EsthenosUser"
mainapp.config['ROOT'] = os.curdir
mainapp.config['DATA_ROOT'] = os.path.join(mainapp.config['ROOT'],'pitaya/data/')
mainapp.config['UPLOAD_FOLDER'] = os.path.join(mainapp.config['ROOT'],'pitaya/uploads')
mainapp.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=30)

# applying settings.
mainapp.config["FEATURES"] = settings.FEATURES
mainapp.config["SERVER_SETTINGS"] = settings.SERVER_SETTINGS
mainapp.config["MONGODB_SETTINGS"] = settings.MONGODB_SETTINGS

# updating settings.
mainapp.config.update(settings.AWS_SETTINGS)
mainapp.config.update(settings.CELERY_SETTINGS)

# updating debug settings.
mainapp.config.update(
    DEBUG = True,
    TESTING = False,
)


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.needs_refresh_message = u"To protect your account, please re-authenticate to access this page."
login_manager.needs_refresh_message_category = "info"
login_manager.init_app(mainapp)

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
    from e_organisation.models import EsthenosUser
    return EsthenosUser.objects(id=userid).first()

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

@mainapp.template_filter('percentformat')
def _jinja2_filter_percentformat(fraction):
    return "%.0f" % (fraction * 100)

@mainapp.template_filter('enabledfilter')
def _jinja2_filter_enabledfilter(active):
    return "enabled" if active else "disabled"

@mainapp.template_filter('enabledbutton')
def _jinja2_filter_enabledbutton(active):
    return "btn-primary" if active else "btn-danger"

@mainapp.template_filter('permissionfilter')
def _jinja2_filter_permissionfilter(permission):
    return "checked" if permission else "unchecked"

@mainapp.template_filter('cdnassets')
def _jinja2_filter_cdn_assets(asset):
    cdn = settings.AWS_SETTINGS["AWS_CDN_PATH"]
    bucket = settings.AWS_SETTINGS["AWS_S3_BUCKET"]
    return "%s/%s/%s" % (cdn, bucket,  asset)

@mainapp.template_filter('css_approve_reject')
def _jinja2_filter_css_approve_reject(value):
    if value == "approved":
        return "btn-primary"

    if value == "rejected":
        return "btn-danger"

    if value == "onhold":
        return "btn-warning"

    return ""

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
    kwargs = {"redirect_url": "/" }
    return render_template('403.html', **kwargs), 403
