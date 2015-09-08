from mongoengine import Q

import boto
import pyexcel
import datetime
import traceback
import os, io, StringIO
import tempfile, zipfile, uuid, json
from PIL import Image
from math import log10, floor
from datetime import timedelta
from werkzeug.utils import secure_filename

from flask.ext import excel
from flask.views import View
from flask import Blueprint, redirect, url_for, render_template, session, request, Response, abort, make_response
from flask_sauth.views import flash_errors
from flask_login import current_user, login_user, logout_user, login_required

from esthenos import s3_bucket, mainapp
from esthenos.mongo_encoder import encode_model
from e_admin.forms import AddOrganizationEmployeeForm
from e_tokens.utils import login_or_key_required, feature_enable
from e_reports.views import get_application_headers, get_application_rowdata
from e_admin.models import EsthenosSettings, EsthenosUser
from esthenos.utils import request_wants_json, random_with_N_digits
from esthenos.tasks import generate_post_grt_applications, downloadFile, zip_custom
from e_pixuate.pixuate import upload_images, get_url_with_id
from e_organisation.forms import AddApplicationMobile
from e_organisation.models import *


conn_s3 = boto.connect_s3(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))

organisation_views = Blueprint('organisation_views', __name__, template_folder='templates')

class RenderTemplateView(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)

def round_to_1(x):
    if x < 0:
        return 0
    return round(x, -int(floor(log10(x))))

