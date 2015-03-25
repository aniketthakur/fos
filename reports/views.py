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
@reports_views.route('/pan_reports', methods=["GET"])
@login_required
def pan_reports():
    username = current_user.name
    c_user = current_user
    print username
    kwargs = locals()
    return render_template("pan_lists.html", **kwargs)


from werkzeug.utils import secure_filename
from esthenos  import  s3_bucket


@reports_views.route('/pan_reports/download', methods=["GET"])
@login_or_key_required
def get_buckets_logs():
    c_user = current_user
    kwargs = locals()
    from p_storage.models import PANObject
    if request.method == 'GET':
        p_user  = PUser.objects.get(id=c_user.id)
        pans = PANObject.objects(owner=p_user).exclude('raw')
        pan_data = list()
        headers = list()
        headers.append("PAN")
        headers.append("Name")
        headers.append("Date")
        headers.append("Father/Organisation Name")
        headers.append("Created Date")
        headers.append("Validation Status")
        pan_data.append(headers)
        for pan in pans:
            row_data = list()
            row_data.append(pan["pan_number"])
            row_data.append(pan["name"])
            row_data.append(pan["dob"])
            row_data.append(pan["f_or_o_name"])
            row_data.append(pan["date_added"])
            row_data.append(pan["validation_state"])
            pan_data.append(row_data)

        output = excel.make_response_from_array(pan_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=pan_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output



@reports_views.route('/api/pan_cards/', methods=["GET"])
@login_or_key_required
def get_pan_reports():
    c_user = current_user
    kwargs = locals()
    from p_storage.models import PANObject
    if request.method == 'GET':
        p_user  = PUser.objects.get(id=c_user.id)
        pans = PANObject.objects(owner=p_user).exclude('raw')
        return Response(json.dumps({'data':pans},default=encode_model), content_type="application/json", mimetype='application/json')



@reports_views.route('/aadhaar_reports', methods=["GET"])
@login_required
def aadhaar_reports():
    username = current_user.name
    c_user = current_user
    print username
    kwargs = locals()
    return render_template("aadhaar_lists.html", **kwargs)


@reports_views.route('/aadhaar_reports/download', methods=["GET"])
@login_or_key_required
def get_aadhaar_reports():
    c_user = current_user
    kwargs = locals()
    from p_storage.models import PANObject
    if request.method == 'GET':
        p_user  = PUser.objects.get(id=c_user.id)
        pans = AADHAARObject.objects(owner=p_user).exclude('raw')
        pan_data = list()
        headers = list()
        headers.append("Aadhaar Number")
        headers.append("Name")
        headers.append("DOB")
        headers.append("GENDER")
        headers.append("C/O")
        headers.append("Created Date")
        headers.append("Validation Status")
        pan_data.append(headers)
        for pan in pans:
            row_data = list()
            row_data.append(pan["aadhaar_id"])
            row_data.append(pan["name"])
            row_data.append(pan["year_of_birth"])
            row_data.append(pan["gender"])
            row_data.append(pan["care_of"])
            row_data.append(pan["date_added"])
            row_data.append(pan["validation_state"])
            pan_data.append(row_data)

        output = excel.make_response_from_array(pan_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=aadhaar_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output

@reports_views.route('/api/aadhaar_cards/', methods=["GET"])
@login_or_key_required
def get_aadhaar_cards():
    c_user = current_user
    kwargs = locals()
    from p_storage.models import AADHAARObject
    if request.method == 'GET':
        p_user  = PUser.objects.get(id=c_user.id)
        pans = AADHAARObject.objects(owner=p_user).exclude('raw')
        return Response(json.dumps({'data':pans},default=encode_model), content_type="application/json", mimetype='application/json')

@reports_views.route('/vid_reports', methods=["GET"])
@login_required
def vid_reports():
    username = current_user.name
    c_user = current_user
    print username
    kwargs = locals()
    return render_template("vid_lists.html", **kwargs)

@reports_views.route('/vid_reports/download', methods=["GET"])
@login_or_key_required
def download_vid_reports():
    c_user = current_user
    kwargs = locals()
    from p_storage.models import PANObject
    if request.method == 'GET':
        p_user  = PUser.objects.get(id=c_user.id)
        pans = VCObject.objects(owner=p_user).exclude('raw')
        pan_data = list()
        headers = list()
        headers.append("Voter's Card Number")
        headers.append("Name")
        headers.append("DOB")
        headers.append("GENDER")
        headers.append("Father's/Husband Name")
        headers.append("Created Date")
        headers.append("Validation Status")
        pan_data.append(headers)
        for pan in pans:
            row_data = list()
            row_data.append(pan["vc_number"])
            row_data.append(pan["electors_name"])
            row_data.append(pan["dob"])
            row_data.append(pan["gender"])
            row_data.append(pan["f_or_h_name"])
            row_data.append(pan["date_added"])
            row_data.append(pan["validation_state"])
            pan_data.append(row_data)

        output = excel.make_response_from_array(pan_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=vid_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output

@reports_views.route('/api/voters_cards/', methods=["GET"])
@login_or_key_required
def get_vid_reports():
    c_user = current_user
    kwargs = locals()
    from p_storage.models import VCObject
    if request.method == 'GET':
        p_user  = PUser.objects.get(id=c_user.id)
        pans = VCObject.objects(owner=p_user).exclude('raw')
        return Response(json.dumps({'data':pans},default=encode_model), content_type="application/json", mimetype='application/json')

