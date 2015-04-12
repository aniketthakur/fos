__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template, request,Response
from flask_login import current_user, login_required
from e_tokens.utils import login_or_key_required
import json,hashlib
from e_admin.models import EsthenosUser
from e_organisation.models import EsthenosOrgApplicationHighMark,EsthenosOrgApplicationHighMarkRequest
from flask import  Blueprint
import os,tempfile
from esthenos.crossdomain import *
from esthenos.utils import random_with_N_digits
#import flickr_api
#flickr_api.set_keys(api_key = "8766ced6ec90eb38a32778e847a83233", api_secret = "cda7061fdbd608fd")
storage_path =  os.path.join(os.curdir,'pitaya/uploads')
admin_reports_views = Blueprint('admin_reports_views', __name__,
    template_folder='templates')

from flask.ext import excel
from flask import Flask, make_response
from reports.views import get_application_headers,get_application_rowdata
@admin_reports_views.route('/admin/reports/internal_main/download', methods=["GET"])
@login_or_key_required
def admin_internal_main_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplication
    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)

        app_headers = get_application_headers()
        app_headers.append("Organisation Name")

        applications = EsthenosOrgApplication.objects.all()

        application_data = list()


        headers = app_headers
        application_data.append(headers)
        for app in applications:
            app_row_data= get_application_rowdata(app)
            app_row_data.append(app.organisation.name)
            app_row_data = app_row_data
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=internal_main_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output