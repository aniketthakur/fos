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
from datetime import timedelta
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
#@login_required
def home_page():
    kwargs = locals()
    return render_template("dashboard.html", **kwargs)

@organisation_views.route('/upload_documents', methods=["GET"])
#@login_required
def upload_documents():
    kwargs = locals()
    return render_template("upload_documents.html", **kwargs)


@organisation_views.route('/application_status', methods=["GET"])
#@login_required
def application_status():
    kwargs = locals()
    return render_template("centers_n_groups.html", **kwargs)

@organisation_views.route('/applications', methods=["GET"])
#@login_required
def applications():
    kwargs = locals()
    return render_template("applications_list.html", **kwargs)

@organisation_views.route('/application/<app_id>/track', methods=["GET"])
#@login_required
def applications_track(app_id):
    kwargs = locals()
    return render_template("application_tracking.html", **kwargs)

@organisation_views.route('/download_disbusement', methods=["GET"])
#@login_required
def download_disbusement():
    kwargs = locals()
    return render_template("download_disbusement.html", **kwargs)

@organisation_views.route('/download_grt', methods=["GET"])
#@login_required
def download_grt():
    kwargs = locals()
    return render_template("download_grt.html", **kwargs)



@organisation_views.route('/application/<application_id>', methods=["GET"])
#@login_required
def application_manual_DE(application_id):
    kwargs = locals()
    print application_id
    return render_template("application_manual_DE.html", **kwargs)

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

