__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template, request,Response
from flask_login import current_user, login_required
from e_tokens.utils import login_or_key_required
import json,hashlib
from e_admin.models import EsthenosUser
from flask import  Blueprint
import os,tempfile
from esthenos.crossdomain import *
from esthenos.utils import random_with_N_digits
#import flickr_api
#flickr_api.set_keys(api_key = "8766ced6ec90eb38a32778e847a83233", api_secret = "cda7061fdbd608fd")
storage_path =  os.path.join(os.curdir,'pitaya/uploads')
reports_views = Blueprint('reports_views', __name__,
                        template_folder='templates')

from flask.ext import excel
from flask import Flask, make_response


@reports_views.route('/reports/download', methods=["GET"])
@login_or_key_required
def get_buckets_logs():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplication
    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)
        applications = EsthenosOrgApplication.objects(organisation=user.organisation)
        application_data = list()
        headers = list()
        headers.append("Application ID")

        application_data.append(headers)
        for app in applications:
            row_data = list()
            row_data.append(app["application_id"])

            application_data.append(row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=pan_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output