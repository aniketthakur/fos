__author__ = 'prathvi'
from e_admin.models import EsthenosUser
from esthenos.mongo_encoder import *
from flask_sauth.views import flash_errors
from mongoengine import Q
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template,session,request,Response,abort
import json
from PIL import Image
from flask_login import current_user, login_required
from esthenos  import mainapp
from esthenos.utils import request_wants_json
from esthenos.mongo_encoder import encode_model
from flask.views import View
from esthenos.utils import random_with_N_digits
import os,tempfile
from pixuate_storage_digikyc import upload_images, get_url_with_id
from flask_login import current_user, login_user, logout_user, login_required
from datetime import timedelta
import datetime
import uuid
from e_admin.models import EsthenosSettings
from models import EsthenosOrgUserUploadSession,EsthenosOrgApplicationMap,EsthenosOrgCenter,EsthenosOrgGroup,EsthenosOrgApplication,EsthenosOrg, EsthenosOrgProduct
from models import EsthenosOrgApplicationStatusType,EsthenosOrgNotification,EsthenosOrgApplicationStatus
import traceback
from e_tokens.utils import login_or_key_required
class RenderTemplateView(View):
    def __init__(self, template_name):
        self.template_name = template_name
    def dispatch_request(self):
        return render_template(self.template_name)

from flask import  Blueprint
organisation_views = Blueprint('organisation_views', __name__,
                        template_folder='templates')

from math import log10, floor
def round_to_1(x):
    if x < 0:
        return 0
    return round(x, -int(floor(log10(x))))

@organisation_views.route('/', methods=["GET"])
@login_required
def home_page():
    print session['role']
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("dashboard.html", **kwargs)

@organisation_views.route('/accounts/logout', methods=["GET"])
@login_required
def admin_logout():
    if not session['role'].startswith("ORG_"):
        abort(403)
    logout_user()
    return redirect("/accounts/login")

@organisation_views.route('/center/status/cgt1', methods=["PUT"])
@login_required
def center_cgt1():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    data = json.loads(request.json)
    center_id = data['center_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    center = EsthenosOrgCenter.objects.get(organisation=user.organisation,center_id=center_id)
    applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=190)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=190)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
        if reqstatus ==  True:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 220
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=210)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 210
        app.save()

    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/api/organisation/products', methods=["GET"])
@login_or_key_required
def org_products():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisations = EsthenosOrg.objects.all()
    products = EsthenosOrgProduct.objects.all()
    content = list()
    for product in products:
        pr = dict()
        pr["product_name"] = product["product_name"]
        pr["loan_amount"] = product["loan_amount"]
        pr["life_insurance"] = product["life_insurance"]
        pr["eligible_cycle"] = product["eligible_cycle"]
        pr["number_installments"] = product["number_installments"]
        pr["emi"] = product["emi"]
        pr["last_emi"] = product["last_emi"]
        pr["processing_fee"] = product["processing_fee"]
        pr["total_processing_fees"] = product["total_processing_fees"]
        pr["interest_rate"] = product["interest_rate"]
        pr["insurance_period"] = product["insurance_period"]
        pr["emi_repayment"] = product["emi_repayment"]
        content.append(pr)
    kwargs = locals()
    return Response(json.dumps({'products':content}), content_type="application/json", mimetype='application/json')

@organisation_views.route('/reports', methods=["GET"])
@login_required
def admin_reports():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisations = EsthenosOrg.objects.all()
    tagged_applications = EsthenosOrgApplication.objects.all()
    kwargs = locals()
    return render_template("client_reports.html", **kwargs)

@organisation_views.route('/center/status/cgt2', methods=["PUT"])
@login_required
def center_cgt2():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    center_id = data['center_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    center = EsthenosOrgCenter.objects.get(organisation=user.organisation,center_id=center_id)
    applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=220)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
        if reqstatus ==  True:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 250
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=240)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 240
        app.save()
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/center/status/grt', methods=["PUT"])
@login_required
def center_grt():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    center_id = data['center_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    center = EsthenosOrgCenter.objects.get(organisation=user.organisation,center_id=center_id)
    applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=250)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
        if reqstatus ==  True:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=272)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 272
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=270)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 270

        app.save()
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/group/status/cgt1', methods=["PUT"])
@login_required
def group_cgt1():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=190)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=190)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
        if reqstatus ==  True:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 220
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=210)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 210
        app.save()
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/group/status/cgt2', methods=["PUT"])
@login_required
def group_cgt2():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=220)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
        if reqstatus ==  True:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 250
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=240)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 240
        app.save()
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/group/status/grt', methods=["PUT"])
@login_required
def group_grt():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=250)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
        if reqstatus ==  True:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=272)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 272
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=270)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 270
        app.save()
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/uploads_group_app', methods=["GET","POST"])
@login_required
def uploads_group_app():
    print session['role']
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname,file.filename))
        file_id = file.filename.split("_")[0]
        print file_id

        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            if (app.file_id) == int(file_id):
                application = app
                break

        if application == None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = int(file_id)
        print uploaded_resp
        application.app_file_pixuate_id.append(uploaded_resp[0]["id"])
        session_obj.applications[file_id]=application
        session_obj.number_of_applications = session_obj.number_of_applications + 1
        session_obj.save()
        print session_obj.id

    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")


@organisation_views.route('/uploads_group_kyc', methods=["GET","POST"])
@login_required
def uploads_group_kyc():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname,file.filename))
        file_id = file.filename.split("_")[0]
        kyc_type = file.filename.split("_")[1][0]
        print file_id
        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            if (app.file_id) == int(file_id):
                application = app
                break

        if application == None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = int(file_id)
        application.kyc_file_pixuate_id[kyc_type] = uploaded_resp[0]["id"]
        session_obj.applications[file_id]=application
        session_obj.number_of_kycs = session_obj.number_of_kycs+ 1
        session_obj.save()
        print session_obj.id
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/uploads_group_gkyc', methods=["GET","POST"])
@login_required
def uploads_group_gkyc():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname,file.filename))
        file_id = file.filename.split("_")[0]
        kyc_type = file.filename.split("_")[1][0]
        print file_id
        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            if (app.file_id) == int(file_id):
                application = app
                break
        if application == None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = int(file_id)
        application.gkyc_file_pixuate_id[kyc_type] = uploaded_resp[0]["id"]
        session_obj.applications[file_id]=application
        session_obj.number_of_kycs = session_obj.number_of_gkycs+ 1
        session_obj.save()
        print session_obj.id
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/uploads_indivijual_app', methods=["GET","POST"])
@login_required
def uploads_indivijual_app():
    if not session['role'] or not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname,file.filename))
        kyc_type = file.filename.split("_")[1][0]
        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            if app.file_id == 100:
                application = app
                break

        if application == None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = 100
        application.app_file_pixuate_id.append(uploaded_resp[0]["id"])
        session_obj.applications["1"] = application
        session_obj.number_of_applications = 1
        session_obj.save()
        print session_obj.id
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/uploads_indivijual_kyc', methods=["GET","POST"])
@login_required
def uploads_indivijual_kyc():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname,file.filename))
        kyc_type = file.filename.split("_")[1][0]
        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            if app.file_id == 100:
                application = app
                break

        if application == None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = 100
        application.kyc_file_pixuate_id[kyc_type] = uploaded_resp[0]["id"]
        session_obj.applications["1"] = application
        session_obj.number_of_kycs = session_obj.number_of_kycs+ 1
        session_obj.save()
        print session_obj.id
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")


@organisation_views.route('/uploads_indivijual_gkyc', methods=["GET","POST"])
@login_required
def uploads_indivijual_gkyc():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname,file.filename))
        kyc_type = file.filename.split("_")[1][0]
        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        index = -1
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            index = index+1
            if app.file_id == 100:
                application = app
                break

        if application == None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = 100
        application.gkyc_file_pixuate_id[kyc_type] = uploaded_resp[0]["id"]
        session_obj.applications["1"] = application
        session_obj.number_of_kycs = session_obj.number_of_kycs+ 1
        session_obj.save()
        print session_obj.id
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

#@organisation_views.route('/api/organisation/centers_n_groups', methods=["POST"])
#@login_or_key_required
#def create_centers_n_groups():
##    if not session['role'].startswith("ORG_"):
##        abort(403)
#    username = current_user.name
#    c_user = current_user
#    user = EsthenosUser.objects.get(id=c_user.id)
#    organisation = user.organisation
#    center_name = request.form.get('center_name')
#    group_name = request.form.get('group_name')
#    if center_name == None:
#        center_name = group_name
#    if center_name !=None and len(center_name)>0 and group_name !=None and len(group_name) != None :
#        unique_center_id = user.organisation.name.upper()[0:2]+"C"+"{0:06d}".format(user.organisation.center_count)
#        center,status = EsthenosOrgCenter.objects.get_or_create(center_name=center_name,organisation=user.organisation)
#        if status:
#            center.center_id = unique_center_id
#            center.save()
#            EsthenosOrg.objects.get(id = user.organisation.id).update(inc__center_count=1)
#
#        unique_group_id = user.organisation.name.upper()[0:2]+"G"+"{0:06d}".format(user.organisation.group_count)
#        group,status = EsthenosOrgGroup.objects.get_or_create(center=center,organisation=user.organisation,group_name=group_name)
#        if status:
#            group.group_id = unique_group_id
#            group.save()
#            EsthenosOrg.objects.get(id = user.organisation.id).update(inc__group_count=1)
#
#        return Response('{"success":True}', content_type="application/json", mimetype='application/json')
#    return Response('{"success":False}', content_type="application/json", mimetype='application/json')

@organisation_views.route('/api/organisation/centers_n_groups', methods=["GET"])
@login_or_key_required
def get_centers_n_groups():
#    if not session['role'].startswith("ORG_"):
#        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=organisation)
    centers_list = []
    all_group_list = []
    for cen in centers:
        groups = EsthenosOrgGroup.objects.filter(organisation=organisation,center = cen)
        groups_list = []
        for grp in groups:
            groups_list.append({'id':str(grp.group_id),
                                'group_name':str(grp.group_name)
            })

        centers_list.append(
            {'id':str(cen.center_id),
                    'center_name':str(cen.center_name),'groups':groups_list}
        )
    groups = EsthenosOrgGroup.objects.filter(organisation=organisation)
    for grp in groups:
        all_group_list.append({'id':str(grp.group_id),
                               'group_name':str(grp.group_name)
        })

    data = '{"centers":'+json.dumps(centers_list)+',"groups":'+json.dumps(all_group_list)+'}'
    print data
    return Response(data, content_type="application/json", mimetype='application/json')


@organisation_views.route('/api/organisation/update_group_details', methods=["PUT"])
@login_or_key_required
def update_group_number():
#    if not session['role'].startswith("ORG_"):
#        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = user.organisation
    print request.form
    group_name = request.form.get('group_name')
    group = EsthenosOrgGroup.objects.filter(organisation=user.organisation,group_name=group_name)[0]
    group_size = request.form.get('group_size')
    group.size = int(group_size)
    group_leader_name = request.form.get('group_leader_name')
    group.leader_name = group_leader_name
    group_leader_number = request.form.get('group_leader_number')
    group.leader_number = group_leader_number
    group.save()
    data = '{"success":true}'
    print data
    return Response(data, content_type="application/json", mimetype='application/json')


@organisation_views.route('/api/organisation/applications', methods=["GET"])
@login_or_key_required
def get_application():
#    if not session['role'].startswith("ORG_"):
#        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    center_name = request.form.get('center_name')
    group_name = request.args['group_name']
    print  group_name
    group = EsthenosOrgGroup.objects.filter(organisation=user.organisation,group_name=group_name)[0]

    if center_name != None and group_name != None:
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation,center__contains=center_name,group=group).only("application_id","applicant_name","date_created","upload_type","current_status","loan_eligibility_based_on_net_income","loan_eligibility_based_on_company_policy")
    elif center_name != None:
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation,center__center_name__contains=center_name).only("application_id","applicant_name","date_created","upload_type","current_status","loan_eligibility_based_on_net_income","loan_eligibility_based_on_company_policy")
    elif group_name != None:
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation,group=group).only("application_id","applicant_name","date_created","upload_type","current_status","loan_eligibility_based_on_net_income","loan_eligibility_based_on_company_policy")
    else:
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation).only("application_id","applicant_name","date_created","upload_type","current_status","loan_eligibility_based_on_net_income","loan_eligibility_based_on_company_policy")
    resp = list()
    for app in applications:
        item = dict()
        item["id"] = app["application_id"]
        item["applicant_name"] = app["applicant_name"]
        item["date_created"] = app["date_created"]
        item["current_status"] = app["current_status"].status_message
        item["loan_eligibility_based_on_net_income"] = app["loan_eligibility_based_on_net_income"]
        item["loan_eligibility_based_on_company_policy"] = app["loan_eligibility_based_on_company_policy"]
    #center = EsthenosOrgCenter.objects.filter(center_name=center_name)[0]

    resp = dict()
    applications_list = []
    #resp['center'] = center.name
    #resp['center_size'] = center.size
    if group!=None:
        resp['group'] =  group.group_name
        resp['group_size'] = group.size
    for app in applications:
        applications_list.append({'id':str(app.application_id),
              'date_created':str(app.date_created),
              'upload_type':app.upload_type,
              'current_status':str(app.current_status),
    })

    resp["applications"] = applications_list

    return Response(response=json.dumps(resp),
        status=200,\
        mimetype="application/json")



from e_organisation.models import EsthenosOrgSettings
@organisation_views.route('/upload_documents', methods=["GET","POST"])
@login_required
def upload_documents():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    if request.method == "GET":
        unique_key =  uuid.uuid4()
        session_obj =  EsthenosOrgUserUploadSession()
        session_obj.owner = user
        print unique_key
        session_obj.unique_session_key = str(unique_key)
        session_obj.save()
        print session_obj.id
#        from esthenos.tasks import prefill_applications
#        prefill_applications()
        kwargs = locals()
        return render_template("upload_documents.html", **kwargs)
    elif request.method == "POST":
        center_name = request.form.get('i_center_name')
        group_name = request.form.get('i_group_name')
        if center_name ==None:
            center_name = request.form.get('g_center_name')
            group_name = request.form.get('g_group_name')

        center = None
        group = None
        if center_name == None:
            center_name = group_name
        if center_name !=None and len(center_name)>0 and group_name !=None and len(group_name) != None :
            unique_center_id = user.organisation.name.upper()[0:2]+"C"+"{0:06d}".format(user.organisation.center_count)
            center,status = EsthenosOrgCenter.objects.get_or_create(center_name=center_name,organisation=user.organisation)
            if status:
                center.center_id = unique_center_id
                center.save()
                EsthenosOrg.objects.get(id = user.organisation.id).update(inc__center_count=1)

            unique_group_id = user.organisation.name.upper()[0:2]+"G"+"{0:06d}".format(user.organisation.group_count)
            group,status = EsthenosOrgGroup.objects.get_or_create(organisation=user.organisation,group_name=group_name)
            if status:
                group.group_id = unique_group_id
                group.save()
                EsthenosOrg.objects.get(id = user.organisation.id).update(inc__group_count=1)



        if center!=None or group != None:
            unique_key = request.form.get('unique_key')
            session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key,tagged=False)
            inc_count = EsthenosOrg.objects.get(id = user.organisation.id).application_count+1
            int_x = 0
            for appkey in session_obj.applications.keys():
                app = session_obj.applications[appkey]
                tagged_application =  EsthenosOrgApplication()
                tagged_application.organisation = user.organisation
                tagged_application.center = center
                tagged_application.group = group
                tagged_application.tag  = app
                tagged_application.owner = user
                tagged_application.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=0)
                settings = EsthenosSettings.objects.all()[0]
                tagged_application.application_id = user.organisation.name.upper()[0:2]+str(settings.organisations_count)+"{0:06d}".format(inc_count)
                tagged_application.upload_type = "MANUAL_UPLOAD"
                tagged_application.status = 0
                tagged_application.save()
                inc_count = inc_count+1
                int_x = int_x+1

            EsthenosOrg.objects.get(id = user.organisation.id).update(inc__application_count=int_x)

            session_obj.center = center
            session_obj.group = group
            session_obj.tagged = True
            session_obj.save()
            print session_obj.id
        unique_key =  uuid.uuid4()
        session_obj =  EsthenosOrgUserUploadSession()
        session_obj.owner = user
        session_obj.unique_session_key = str(unique_key)
        session_obj.save()
        print session_obj.id


        kwargs = locals()
        return render_template("upload_documents.html", **kwargs)




@organisation_views.route('/application_status', methods=["GET"])
@login_required
def application_status():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    kwargs = locals()
    return render_template("centers_n_groups.html", **kwargs)

@organisation_views.route('/applications', methods=["GET"])
@login_required
def applications():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group")
    #    print  center_id," ",group_id
    #    center = None
    #    if center_id is not None and center_id != '':
    #        center = EsthenosOrgCenter.objects.get(center_id=center_id)
    #        print center.center_name
    #    else:
    #        group_id = ''
    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        print group.group_name
    else:
        center_id = ''
    print  "filter "+ group.group_name

    applications = None
    #    if center != None:
    #        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=11)
    #    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=110)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=110)

    kwargs = locals()
    return render_template("applications_list.html", **kwargs)

@organisation_views.route('/application/<app_id>/track', methods=["GET"])
@login_required
def applications_track(app_id):
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    application = EsthenosOrgApplication.objects.get(organisation = user.organisation,application_id=app_id)
    #print application.timeline
    kwargs = locals()
    return render_template("application_tracking.html", **kwargs)

@organisation_views.route('/check_disbusement', methods=["GET"])
@login_required
def check_disbusement():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("centers_n_groups_disbussment.html", **kwargs)

from esthenos.tasks import generate_post_grt_applications
@organisation_views.route('/disburse_group', methods=["PUT"])
@login_required
def disburse_document():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    group = EsthenosOrgGroup.objects.get(group_id=request.form.get("group_id"))
    apps = EsthenosOrgApplication.objects.filter(organisation=org,group=group)
    print request.form.get("group_id")
    dis_date_str =request.form.get("disbursement_date")
    col_date_str =request.form.get("collection_date")
    dis_date =    datetime.datetime.strptime(dis_date_str, "%d-%m-%Y").date()
    col_date =   datetime.datetime.strptime(col_date_str, "%d-%m-%Y").date()
    generate_post_grt_applications.apply_async((org.id,request.form.get("group_id"),dis_date_str,(col_date-dis_date).days))
    for app in apps:
        app.generate_disbursement = True
        app.save()
    kwargs = locals()
    return Response(json.dumps({"result":"We are preparing your download document, please wait !"},default=encode_model), content_type="application/json", mimetype='application/json')

import boto
conn_s3 = boto.connect_s3(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))
import tempfile

@organisation_views.route('/download_disbursement', methods=["GET"])
@login_required
def download_disbusement():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group_id")

    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        bucket = conn_s3.get_bucket("hindusthanarchives")
        bucket_list = bucket.list()

        for l in bucket_list:
            print l
            print group.disbursement_pdf_link
            if group.disbursement_pdf_link[1:] == l.key:
                keyString = str(l.key)
                # check if file exists locally, if not: download it
                if not os.path.exists(group.disbursement_pdf_link):
                    l.get_contents_to_filename(group.disbursement_pdf_link)
                filehandle = open(group.disbursement_pdf_link, 'rb')
                data = StringIO.StringIO(filehandle.read())
                output = make_response(data.getvalue())
                output.headers["Content-Disposition"] = "attachment; filename=%s" %group_id
                output.headers["Content-type"] = "application/zip"
                return output
        print group.group_name
    return Response(json.dumps({"success":False},default=encode_model), content_type="application/json", mimetype='application/json')
    # Grab ZIP file from in-memory, make response with correct MIME-type



@organisation_views.route('/telecalling', methods=["GET"])
@login_required
def telecalling():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    call_sessions = EsthenosOrgIndivijualTeleCallingSession.objects.filter(organisation=org)
    kwargs = locals()
    return render_template("centers_n_groups_tc.html", **kwargs)

@organisation_views.route('/check_tele_applicant', methods=["GET"])
@login_required
def check_tele_applicant():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group")
#    print  center_id," ",group_id
#    center = None
#    if center_id is not None and center_id != '':
#        center = EsthenosOrgCenter.objects.get(center_id=center_id)
#        print center.center_name
#    else:
#        group_id = ''
    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        print group.group_name
    else:
        center_id = ''
    print  "filter "+ group.group_name
    applications = None
#    if center != None:
#        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=11)
#    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=272)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=272)
    kwargs = locals()
    return render_template("update_tele_indivijual.html", **kwargs)

from models import EsthenosOrgTeleCallingTemplateQuestion,EsthenosOrgIndivijualTeleCallingSession
@organisation_views.route('/check_tele_applicant_questions', methods=["GET","POST"])
@login_required
def check_tele_applicant_questions():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    center_id = request.args.get("center")
    group_id = request.args.get("group")
    print  center_id," ",group_id
    center = None
    if center_id is not None and center_id != '':
        center = EsthenosOrgCenter.objects.get(center_id=center_id)
        print center.center_name

    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print  group_id
    if group_id is not None :
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        print group.group_name


    app_id = request.args.get("app_id")

    if request.method == "GET":
        print app_id
        questions = EsthenosOrgTeleCallingTemplateQuestion.objects.all()

        kwargs = locals()
        return render_template("update_indivijual_tele_questions.html", **kwargs)
    if request.method == "POST":
        print request.form
        print  group
        i = 0
        total_score= 0.0
        questions = EsthenosOrgTeleCallingTemplateQuestion.objects.filter(organisation = user.organisation)
        application = EsthenosOrgApplication.objects.get(application_id = app_id)
        tele_session,status = EsthenosOrgIndivijualTeleCallingSession.objects.get_or_create(application=application,group=group,organisation=user.organisation)
        question_dict = dict()

        for v in request.form:
            i = i+1
            (k,v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score+ int(v)
        print total_score/i
        print questions
        tele_session.questions = question_dict
        tele_session.score = float(total_score/i)
        tele_session.save()
        kwargs = locals()
        return redirect("/check_tele_applicant?group="+group_id)

from e_organisation.models import EsthenosOrgGroupCGT1Session,EsthenosOrgGroupCGT2Session
@organisation_views.route('/check_cgt1', methods=["GET"])
@login_required
def check_cgt1():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    cgt1_sessions = EsthenosOrgGroupCGT1Session.objects.filter(organisation=org)
    kwargs = locals()
    return render_template("centers_n_groups_cgt1.html", **kwargs)

from e_organisation.models import EsthenosOrgGRTTemplateQuestion,EsthenosOrgGroupGRTSession,EsthenosOrgCGT1TemplateQuestion,EsthenosOrgCGT2TemplateQuestion
@organisation_views.route('/cgt1_question', methods=["GET","POST"])
@login_required
def cgt1_question():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org=user.organisation
    if request.method == "GET":
        group_id = request.args.get("group_id")
        questions = EsthenosOrgCGT1TemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        kwargs = locals()
        return render_template("centers_n_groups_grt_questions.html", **kwargs)
    elif request.method == "POST":
        print request.form
        i = 0
        total_score= 0.0
        group_id = request.args.get("group_id")
        questions = EsthenosOrgCGT1TemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        grt_session,status = EsthenosOrgGroupCGT1Session.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i+1
            (k,v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score+ int(v)
        print total_score/i
        print questions
        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_cgt1")

@organisation_views.route('/check_cgt1_applicant', methods=["GET"])
@login_required
def check_cgt1_applicant():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group")
    #    print  center_id," ",group_id
    #    center = None
    #    if center_id is not None and center_id != '':
    #        center = EsthenosOrgCenter.objects.get(center_id=center_id)
    #        print center.center_name
    #    else:
    #        group_id = ''
    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        print group.group_name
    else:
        center_id = ''
    print  "filter "+ group.group_name
    applications = None
    #    if center != None:
    #        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=190)
    #    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=190)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=190)
    kwargs = locals()
    return render_template("update_cgt1_indivijual.html", **kwargs)


@organisation_views.route('/check_cgt2', methods=["GET"])
@login_required
def check_cgt2():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    cgt2_sessions = EsthenosOrgGroupCGT2Session.objects.filter(organisation=org)
    kwargs = locals()
    return render_template("centers_n_groups_cgt2.html", **kwargs)

@organisation_views.route('/cgt2_question', methods=["GET","POST"])
@login_required
def cgt2_question():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org=user.organisation
    if request.method == "GET":
        group_id = request.args.get("group_id")
        questions = EsthenosOrgCGT2TemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.filter(group_id=group_id)[0]
        kwargs = locals()
        return render_template("centers_n_groups_grt_questions.html", **kwargs)
    elif request.method == "POST":
        print request.form
        i = 0
        total_score= 0.0
        group_id = request.args.get("group_id")
        questions = EsthenosOrgCGT2TemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        grt_session,status = EsthenosOrgGroupCGT2Session.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i+1
            (k,v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score+ int(v)
        print total_score/i
        print questions
        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_cgt2")

@organisation_views.route('/check_cgt2_applicant', methods=["GET"])
@login_required
def check_cgt2_applicant():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group")
    #    print  center_id," ",group_id
    #    center = None
    #    if center_id is not None and center_id != '':
    #        center = EsthenosOrgCenter.objects.get(center_id=center_id)
    #        print center.center_name
    #    else:
    #        group_id = ''
    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        print group.group_name
    else:
        center_id = ''
    print  "filter "+ group.group_name
    applications = None
    #    if center != None:
    #        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=220)
    #    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=220)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=220)
    kwargs = locals()
    return render_template("update_cgt2_indivijual.html", **kwargs)



@organisation_views.route('/check_grt_applicant', methods=["GET"])
@login_required
def check_grt_applicant():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group")
    #    print  center_id," ",group_id
    #    center = None
    #    if center_id is not None and center_id != '':
    #        center = EsthenosOrgCenter.objects.get(center_id=center_id)
    #        print center.center_name
    #    else:
    #        group_id = ''
    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        print group.group_name
    else:
        center_id = ''
    print  "filter "+ group.group_name
    applications = None
    #    if center != None:
    #        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=250)
    #    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=250)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=250)
    kwargs = locals()
    return render_template("update_grt_indivijual.html", **kwargs)

@organisation_views.route('/check_grt', methods=["GET"])
@login_required
def check_grt():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    grt_sessions = EsthenosOrgGroupGRTSession.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("centers_n_groups_grt.html", **kwargs)

@organisation_views.route('/application/<app_id>/cashflow', methods=["GET"])
@login_required
def admin_application_cashflow(app_id):
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    try:
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation,application_id = app_id)
    except Exception as e:
        print e.message
    if len(applications)==0:
        redirect("/application_status")
    app_urls = list()
    application = applications[0]
    kwargs = locals()
    return render_template("org_cf.html", **kwargs)


@organisation_views.route('/users', methods=["GET"])
@login_required
def all_users():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    try:
        employees = EsthenosUser.objects.filter(organisation=user.organisation)
    except Exception as e:
        print e.message
    kwargs = locals()
    return render_template("org_employees.html", **kwargs)

from e_admin.forms import AddOrganizationEmployeeForm

@organisation_views.route('/users/add', methods=["GET","POST"])
@login_required
def admin_organisation_add_emp():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    print "reached here"
    if request.method == "POST":
        print request.form
        org_emp  = AddOrganizationEmployeeForm(request.form)
        form=org_emp
        print user.organisation.id
        form.save(user.organisation.id)
        if (form.validate()):
            form.save(user.organisation.id)
            print "formValidated"
            return redirect("/users")
        else:
            print "some Error"
            flash_errors(form)
            print form.errors
            org = EsthenosOrg.objects.get(id=user.organisation.id)
            kwargs = locals()
            return render_template("org_add_emp.html", **kwargs)
    else:

        org = EsthenosOrg.objects.get(id=user.organisation.id)
        kwargs = locals()
        return render_template("org_add_emp.html", **kwargs)

from e_organisation.models import EsthenosOrgGRTTemplateQuestion,EsthenosOrgGroupGRTSession
@organisation_views.route('/grt_question', methods=["GET","POST"])
@login_required
def grt_question():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org=user.organisation
    if request.method == "GET":
        group_id = request.args.get("group_id")
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        kwargs = locals()
        return render_template("centers_n_groups_grt_questions.html", **kwargs)
    elif request.method == "POST":
        print request.form
        i = 0
        total_score= 0.0
        group_id = request.args.get("group_id")
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)

        grt_session,status = EsthenosOrgGroupGRTSession.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i+1
            (k,v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score+ int(v)
        print total_score/i
        print questions
        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_grt")

from e_organisation.models import EsthenosOrgApplicationStatus
@organisation_views.route('/application/<app_id>/cashflow', methods=["POST"])
@login_required
def cashflow_statusupdate(app_id):
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    try:
        application = EsthenosOrgApplication.objects.filter(application_id = app_id)
        if len(application) >= 0:
            application = application[0]
            status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=datetime.datetime.now())
            status.save()
            application.timeline.append(status)

            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=12)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.status = 12
            application.save()
            new_num = int(app_id[-6:])+1
            new_id = app_id[0:len(app_id)-6] + "{0:06d}".format(new_num)
            new_apps = EsthenosOrgApplication.objects.filter(application_id = new_id)
            if len(new_apps) >0:
                return redirect("/application/"+new_id+"/cashflow")
    except Exception as e:
        print e.message
    return redirect("/application/"+app_id+"/cashflow")

from werkzeug.utils import secure_filename, redirect
import os,io
from esthenos  import  s3_bucket
from flask import make_response
import os
import zipfile
import StringIO
@organisation_views.route('/disbursement/download/<app_id>', methods=["GET","POST"])
@login_required
def disbursement(app_id):
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org=user.organisation
    filenames = ["dpn.pdf", "tmp.pdf","pass.pdf"]

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = app_id
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    output = make_response(s.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=%s" %zip_filename
    output.headers["Content-type"] = "application/zip"
    return output

@organisation_views.route('/profile', methods=["GET","POST"])
@login_required
def user_profile_page():
    username = current_user.name
    c_user = current_user
    profile = EsthenosUser.objects.get(id=current_user.id)
    kwargs = locals()

    if request.method == "GET":
        return render_template("user_profile.html", **kwargs)
    if request.method =="POST":
        file = request.files['file']
        if file is not None and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            o_fname = os.path.abspath(os.path.join(mainapp.config['UPLOAD_FOLDER'], filename))
            image_file = io.BytesIO(file.read())
            im = Image.open(image_file)
            new_file = None
            print im.size
            if im.size[0] > 120:
                new_file = resize(im,120)
            else:
                new_file = im
            new_file.save(o_fname)
            original_key = str(c_user.id) + '/pic/'+filename
            print "uploading to s3...\n"+o_fname+" \n"+original_key
            upload_to_s3(s3_bucket(),o_fname,original_key,'public-read',True)
            profile.profile_pic = 'https://s3.amazonaws.com/digikyc/'+original_key
        profile.name = request.form.get('name')
        profile.first_name = request.form.get('first_name')
        profile.last_name = request.form.get('last_name')
        profile.allow_contact = bool(request.form.get('allow_contact',False))
        profile.email_updates = bool(request.form.get('email_updates',False))
        profile.email_quota_limit = bool(request.form.get('email_quota_limit',False))
        profile.train_complete = bool(request.form.get('train_complete',False))
        profile.save()
        return render_template("user_profile.html", **kwargs)


@organisation_views.route('/notifications', methods=["GET"])
@login_required
def notifications_page():
    username = current_user.name
    c_user = current_user
    notifications = EsthenosOrgNotification.objects.filter(to_user = c_user.id,read_state=False)
    if request_wants_json():
        return Response(json.dumps({"result":notifications},default=encode_model), content_type="application/json", mimetype='application/json')
    count = len(notifications)
    kwargs = locals()
    return render_template("notifications.html", **kwargs)

@organisation_views.route('/notifications/read', methods=["PUT"])
@login_required
def set_notif_read():
    username = current_user.name
    c_user = current_user
    res = EsthenosOrgNotification.objects.filter(to_user = c_user.id,read_state=False).update(set__read_state=True)
    return Response('{"message":"status updated"}', content_type="application/json", mimetype='application/json')

@organisation_views.route('/organisation/<org_id>/application/<app_id>', methods=["GET"])
@login_required
def client_application_id(org_id,app_id):
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    print user.roles[0]
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    app_urls = list()
    try:
        applications = EsthenosOrgApplication.objects.filter(application_id = app_id)
    except Exception as e:
        print e.message

    if len(applications)==0:
        redirect("/reports")

    application = applications[0]
    for kyc_id in application.tag.app_file_pixuate_id:
        app_urls.append(get_url_with_id(kyc_id))

    kyc_urls = list()
    kyc_ids = list()
    for kyc_id_key in application.tag.kyc_file_pixuate_id.keys():
        kyc_id = application.tag.kyc_file_pixuate_id[kyc_id_key]
        kyc_ids.append(kyc_id)
        kyc_urls.append(get_url_with_id(kyc_id))

    gkyc_urls = list()
    gkyc_ids = list()
    for gkyc_id_key in application.tag.gkyc_file_pixuate_id.keys():
        gkyc_id = application.tag.gkyc_file_pixuate_id[gkyc_id_key]
        gkyc_ids.append(gkyc_id)
        gkyc_urls.append(get_url_with_id(gkyc_id))

    today= datetime.datetime.today()
    disbursement_date = datetime.datetime.today() + timedelta(days=1)
    disbursement_date_str = disbursement_date.strftime('%d/%m/%Y')
    products = EsthenosOrgProduct.objects.filter(organisation = application.owner.organisation)

    kwargs = locals()
    return render_template("client_application_manual_DE.html", **kwargs)


@organisation_views.route('/find_users', methods=["GET"])
@login_required
def search_user():
    query_param = request.args.get('q')
    print query_param
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    users = EsthenosUser.objects(Q(name__contains=query_param) |Q(first_name__contains=query_param) | Q(last_name__contains=query_param) |Q(email__contains=query_param) ).only("name","email","id")
    user_dict = list()
    for result in users:
        if str(result.id) != str(c_user.id):
            obj = dict()
            obj['name'] = result.name
            obj['email'] = result.email
            obj['id'] = str(result.id)
            user_dict.append(obj)

    return Response('{"users":'+json.dumps(user_dict)+'}', content_type="application/json", mimetype='application/json')

