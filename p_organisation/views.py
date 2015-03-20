__author__ = 'prathvi'
from p_admin.models import EsthenosUser
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
from pixuate_storage import upload_images
from flask_login import current_user, login_user, logout_user, login_required
from datetime import timedelta
import uuid
from models import EsthenosOrgUserUploadSession,EsthenosOrgApplicationMap,EsthenosOrgCenter,EsthenosOrgGroup,EsthenosOrgApplication,EsthenosOrg
import traceback
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
    return redirect( "/accounts/login")

@organisation_views.route('/uploads_group_app', methods=["GET","POST"])
@login_required
def update_session_data():
    print session['role']
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    center_name = request.form.get('center_name')
    group_game = request.form.get('group_game')
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
    unique_key = request.form.get('unique_key')

    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        upload_images(o_fname)
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

    unique_key = request.form.get('unique_key')
    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        upload_images(o_fname)
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")

@organisation_views.route('/uploads_indivijual_app', methods=["GET","POST"])
@login_required
def uploads_indivijual_app():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    file = request.files['file']
    unique_key = request.form.get('unique_key')
    session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
    index = -1
    application = None
    for app in session_obj.applications:
        index = index+1
        if app.file_id == 100:
            application = app
            break

    if application == None:
        application =  EsthenosOrgApplicationMap()
        application.file_id = 100

    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname))
        application.app_file_pixuate_id.append(uploaded_resp[0]["id"])
        if index == -1:
            application.applications = []
            session_obj.applications.append(application)
            session_obj.number_of_applications = 1
        else:
            session_obj.applications[index] = application
            session_obj.number_of_applications = 1
        session_obj.save()
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
    unique_key = request.form.get('unique_key')
    session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
    application = None
    index = -1
    for app in session_obj.applications:
        index = index+1
        if app.file_id == 100:
            application = app
            break

    if application == None:
        application =  EsthenosOrgApplicationMap()
        application.file_id = 100
    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname))
        application.kyc_file_pixuate_id.append(uploaded_resp[0]["id"])
        if index == -1:
            application.applications = []
            session_obj.applications.append(application)
            session_obj.number_of_kycs = 1
        else:
            session_obj.applications[index] = application
            session_obj.number_of_kycs = session_obj.number_of_kycs+ 1
        session_obj.save()
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
    unique_key = request.form.get('unique_key')
    session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
    application = None
    index = -1
    for app in session_obj.applications:
        index = index+1
        if app.file_id == 100:
            application = app
            break

    if application == None:
        application =  EsthenosOrgApplicationMap()
        application.file_id = 100
    if file:
        filename = secure_filename(file.filename)
        filename = str(random_with_N_digits(6)) +filename
        o_fname = os.path.abspath(os.path.join(tempfile.gettempdir(), filename))
        if os.path.exists(o_fname):
            os.remove(o_fname)
        print "saving to .."+o_fname
        file.save(o_fname)
        uploaded_resp =  json.loads(upload_images(o_fname))
        application.gkyc_file_pixuate_id.append(uploaded_resp[0]["id"])
        if index == -1:
            application.applications = []
            session_obj.applications.append(application)
            session_obj.number_of_kycs = 1
        else:
            session_obj.applications[index] = application
            session_obj.number_of_kycs = session_obj.number_of_kycs+ 1
        session_obj.save()
    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")


organisation_views.route('/organisation/<org_id>/application', methods=["POST"])
@login_required
def submit_application():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)

    pass

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
        session_obj.unique_session_key = str(unique_key)
        session_obj.save()
        kwargs = locals()
        return render_template("upload_documents.html", **kwargs)
    elif request.method == "POST":
        center_name = request.form.get('center_name')
        group_name = request.form.get('group_name')
        center = None
        group = None
        if center_name !=None and len(center_name)>0 and group_name !=None and len(group_name) != None :
            center,status = EsthenosOrgCenter.objects.get_or_create(center_name=center_name,organisation=user.organisation)
            group,status = EsthenosOrgGroup.objects.get_or_create(center=center,organisation=user.organisation,group_name=group_name)
        elif center_name !=None and len(center_name)>0:
            group,status = EsthenosOrgGroup.objects.get_or_create(organisation=user.organisation,group_name=group_name)
        if center!=None or group != None:
            unique_key = request.form.get('unique_key')
            session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
            for app in session_obj.applications:
                EsthenosOrg.objects.get(id = user.organisation.id).update(inc__application_count=1)

                tagged_application =  EsthenosOrgApplication()
                tagged_application.organisation = user.organisation
                tagged_application.center = center
                tagged_application.group = group
                tagged_application.tag  = app
                tagged_application.application_id = user.organisation.name.upper()[0:2]+"{0:06d}".format(user.organisation.application_count)
                tagged_application.upload_type = "MANUAL_UPLOAD"
                tagged_application.status = "TAGGING_DONE"
                tagged_application.save()

            session_obj.center = center
            session_obj.group = group
            session_obj.tagged = True
            session_obj.save()
        unique_key =  uuid.uuid4()
        session_obj =  EsthenosOrgUserUploadSession()
        session_obj.owner = user
        session_obj.unique_session_key = str(unique_key)
        session_obj.save()
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
    center_id = request.args.get("center")
    group_id = request.args.get("group")
    print  center_id," ",group_id
    center = None
    if center_id is not None and center_id != '':
        center = EsthenosOrgCenter.objects.get(id=center_id)
        print center.center_name
    else:
        group_id = ''
    group = None
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(id=group_id)
        print group.group_name
    else:
        center_id = ''

    user = EsthenosUser.objects.get(id=c_user.id)
    applications = None
    if center != None:
        applications = EsthenosOrgApplication.objects.filter(center=center)
    elif group != None:
        applications = EsthenosOrgApplication.objects.filter(group=group)
    else:
        applications = EsthenosOrgApplication.objects.all()

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

@organisation_views.route('/download_disbusement', methods=["GET"])
@login_required
def download_disbusement():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("download_disbusement.html", **kwargs)


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

    kwargs = locals()
    return render_template("centers_n_groups_grt.html", **kwargs)

@organisation_views.route('/download_grt', methods=["GET"])
@login_required
def download_grt():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("download_grt.html", **kwargs)

@organisation_views.route('/billing', methods=["GET"])
@login_required
def billing_view():
    username = current_user.name
    c_user = current_user
    from p_payments.models import PCardInfo
    cards = PCardInfo.objects(user_id=str(current_user.id))
    p_user_type = session['p_user_type']
    billing = None
    if p_user_type == "ACCOUNT_OWNER":
        billing  = PUserBilling.objects.get(user = c_user.id)
        print p_user_type
        kwargs = locals()
        return render_template("user_billing.html", **kwargs)
    else:
        abort(401)
from werkzeug.utils import secure_filename
import os,io
from esthenos  import  s3_bucket


@organisation_views.route('/profile', methods=["GET","POST"])
@login_required
def user_profile_page():
    username = current_user.name
    c_user = current_user
    profile = PUser.objects.get(id=current_user.id)
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
    notifications = PUserNotification.objects.filter(to_user = c_user.id,read_state=False)
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
    res = PUserNotification.objects.filter(to_user = c_user.id,read_state=False).update(set__read_state=True)
    return Response('{"message":"status updated"}', content_type="application/json", mimetype='application/json')


@organisation_views.route('/find_users', methods=["GET"])
@login_required
def search_user():
    query_param = request.args.get('q')
    print query_param
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    users = PUser.objects(Q(name__contains=query_param) |Q(first_name__contains=query_param) | Q(last_name__contains=query_param) |Q(email__contains=query_param) ).only("name","email","id")
    user_dict = list()
    for result in users:
        if str(result.id) != str(c_user.id):
            obj = dict()
            obj['name'] = result.name
            obj['email'] = result.email
            obj['id'] = str(result.id)
            user_dict.append(obj)

    return Response('{"users":'+json.dumps(user_dict)+'}', content_type="application/json", mimetype='application/json')

