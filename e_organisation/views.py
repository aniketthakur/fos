from views_base import *

# import views for user applications.
from views_apps import *

# import views for feature - grt.
from views_grt import *

# import views for feature - cgt1.
from views_cgt1 import *

# import views for feature - cgt2.
from views_cgt2 import *

# import views for feature - tele-calling.
from views_telecalling import *

# import views for feature - psychometric test.
from views_psychometric import *


@organisation_views.route('/', methods=["GET"])
@login_required
def home_page():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    kwargs = locals()
    return render_template("dashboard.html", **kwargs)


@organisation_views.route('/profile', methods=["GET","POST"])
@login_required
def user_profile_page():

    user = EsthenosUser.objects.get(id=current_user.id)
    kwargs = locals()

    if request.method == "GET":
        return render_template("user_profile.html", **kwargs)

    if request.method == "POST":
        file = request.files['file']
        if file is not None and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            o_fname = os.path.abspath(os.path.join(mainapp.config['UPLOAD_FOLDER'], filename))
            image_file = io.BytesIO(file.read())
            im = Image.open(image_file)
            new_file = None

            if im.size[0] > 120:
                new_file = resize(im,120)
            else:
                new_file = im

            new_file.save(o_fname)
            original_key = str(c_user.id) + '/pic/'+filename
            upload_to_s3(s3_bucket(),o_fname,original_key,'public-read',True)
            user.profile_pic = 'https://s3.amazonaws.com/digikyc/'+original_key

        user.name = request.form.get('name')
        user.last_name = request.form.get('last_name')
        user.first_name = request.form.get('first_name')
        user.allow_contact = bool(request.form.get('allow_contact',False))
        user.email_updates = bool(request.form.get('email_updates',False))
        user.train_complete = bool(request.form.get('train_complete',False))
        user.email_quota_limit = bool(request.form.get('email_quota_limit',False))
        user.save()
        return render_template("user_profile.html", **kwargs)


@organisation_views.route('/reports', methods=["GET", "POST"])
@login_required
def reports_internal_main():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)

    if request.method == "GET":
        kwargs = locals()
        return render_template("client_reports.html", **kwargs)

    if request.method == "POST":
        applications = []
        application_data = [
          ["ApplicationID", "Applicant Name", "Group Name", "Branch Name", "Cheque #", "Bank Name"]
        ]

        report_name = "eqifax_reports.csv"
        report_end = request.form.get("end-date")
        report_start = request.form.get("start-date")

        if (report_start is None) or (report_end is None):
            report_name = "eqifax_full_reports.csv"
            applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

        else:
            from datetime import datetime
            endDate = datetime.strptime(report_end, "%m/%d/%Y")
            startDate = datetime.strptime(report_start, "%m/%d/%Y")
            report_name = "eqifax_range_reports.csv"
            applications = EsthenosOrgApplication.objects.filter(date_created__gte=startDate, date_created__lte=endDate, organisation=user.organisation)

        for app in applications:
            app_branch = app.group.branch.branch_name if app.group.branch else ""
            app_row_data = [app.application_id, app.applicant_name, app.group.group_name, app_branch, app.cheque_no, app.cheque_bank_name]
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=%s" % report_name
        output.headers["Content-type"] = "text/csv"
        return output


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


@organisation_views.route('/accounts/logout', methods=["GET"])
@login_required
def admin_logout():
    if not session['role'].startswith("ORG_"):
        abort(403)
    logout_user()
    return redirect("/accounts/login")


@organisation_views.route('/uploads_group_app', methods=["GET", "POST"])
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

        file.save(o_fname)
        uploaded_resp = json.loads(upload_images(o_fname,file.filename))
        file_id = file.filename.split("_")[0]

        unique_key = request.form.get('unique_key')
        session_obj = EsthenosOrgUserUploadSession.objects.get(unique_session_key=unique_key)
        application = None
        for appkey in session_obj.applications.keys():
            app = session_obj.applications[appkey]
            if app.file_id == int(file_id):
                application = app
                break

        if application is None:
            application = EsthenosOrgApplicationMap()
            application.file_id = int(file_id)

        application.app_file_pixuate_id.append(uploaded_resp[0]["id"])
        session_obj.applications[file_id]=application
        session_obj.number_of_applications = session_obj.number_of_applications + 1
        session_obj.save()
        print session_obj.id

    content = {'response': 'OK'}
    return Response(response=content,
        status=200,\
        mimetype="application/json")


@organisation_views.route('/uploads_group_kyc', methods=["GET", "POST"])
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


@organisation_views.route('/uploads_group_gkyc', methods=["GET", "POST"])
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


@organisation_views.route('/uploads_indivijual_app', methods=["GET", "POST"])
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


@organisation_views.route('/organisation/cheque_info/<group_id>', methods=["POST"])
@login_required
def cheque_info_import(group_id):
    c_user = current_user
    print request.form
    print request.files
    if request.method == 'POST' and 'file' in request.files:
        # handle file upload
        filename = request.files['file'].filename
        extension = filename.split(".")[1]
        # Obtain the file extension and content
        # pass a tuple instead of a file name
        sheet = pyexcel.load_from_memory(extension, request.files['file'].read())
        # then use it as usual
        data = pyexcel.to_dict(sheet)
        for k,v in data.items():
            if k != "Series_1":
                print k,v[0],v[1],v[2],v[3],v[4],v[5]
                app = EsthenosOrgApplication.objects.filter(application_id=v[0])[0]
                app.cheque_no = v[4]
                app.cheque_bank_name = v[5]
                app.save()

    return Response(json.dumps({'status':'sucess'}), content_type="application/json", mimetype='application/json')


@organisation_views.route('/uploads_indivijual_kyc', methods=["GET", "POST"])
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

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/uploads_indivijual_gkyc', methods=["GET", "POST"])
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

        if application is None:
            application =  EsthenosOrgApplicationMap()
            application.file_id = 100

        application.gkyc_file_pixuate_id[kyc_type] = uploaded_resp[0]["id"]
        session_obj.applications["1"] = application
        session_obj.number_of_kycs = session_obj.number_of_kycs+ 1
        session_obj.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/api/organisation/centers_n_groups', methods=["POST"])
@login_or_key_required
def create_centers_n_groups():
#    if not session['role'].startswith("ORG_"):
#        abort(403)
   user = EsthenosUser.objects.get(id=current_user.id)
   group_name = request.form.get('group_name')
   center_name = request.form.get('center_name')

   if center_name is None:
       center_name = group_name

   if (center_name is not None) and len(center_name) > 0 and (group_name is not None) and len(group_name) != None:
       unique_center_id = user.organisation.name.upper()[0:2]+"C"+"{0:06d}".format(user.organisation.center_count)

       center, status = EsthenosOrgCenter.objects.get_or_create(center_name=center_name,organisation=user.organisation)
       if status:
           center.center_id = unique_center_id
           center.save()
           EsthenosOrg.objects.get(id = user.organisation.id).update(inc__center_count=1)

       unique_group_id = user.organisation.name.upper()[0:2]+"G"+"{0:06d}".format(user.organisation.group_count)

       group, status = EsthenosOrgGroup.objects.get_or_create(center=center,organisation=user.organisation,group_name=group_name)
       if status:
           group.group_id = unique_group_id
           group.save()
           EsthenosOrg.objects.get(id = user.organisation.id).update(inc__group_count=1)
       return Response('{"success":True}', content_type="application/json", mimetype='application/json')

   return Response('{"success":False}', content_type="application/json", mimetype='application/json')


@organisation_views.route('/api/organisation/centers_n_groups', methods=["GET"])
@login_or_key_required
def get_centers_n_groups():
    user = EsthenosUser.objects.get(id=current_user.id)
    organisation = user.organisation

    centers = EsthenosOrgCenter.objects.filter(organisation=organisation)
    centers_list = []
    for center in centers:
        groups = EsthenosOrgGroup.objects.filter(organisation=organisation,center = center)
        groups_list = []
        for group in groups:
            groups_list.append({'id':str(group.group_id), 'group_name':str(group.group_name), 'group_location':str(group.location_name)})

    groups = EsthenosOrgGroup.objects.filter(organisation=organisation)
    groups_list = []
    for group in groups:
        applications_all = EsthenosOrgApplication.objects.filter(group=group)
        applications_cgt_ready = EsthenosOrgApplication.objects.filter(group=group,status__gte=190)
        if len(applications_all) == 0 or len(applications_all) > len(applications_cgt_ready):
            groups_list.append({'id':str(group.group_id), 'group_name':str(group.group_name), 'group_location':str(group.location_name)})

    data = '{"centers":'+json.dumps(centers_list)+',"groups":'+json.dumps(groups_list)+'}'
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


@organisation_views.route('/api/organisation/products', methods=["GET"])
@login_or_key_required
def org_products():
    user = EsthenosUser.objects.get(id=current_user.id)
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
    myapps = list()
    for app in applications:
        item = dict()
        item["id"] = app["application_id"]
        item["applicant_name"] = app["applicant_name"]
        item["date_created"] = str(app["date_created"])
        item["current_status"] = app["current_status"].status_message
        item["loan_eligibility_based_on_net_income"] = app["loan_eligibility_based_on_net_income"]
        item["loan_eligibility_based_on_company_policy"] = app["loan_eligibility_based_on_company_policy"]
        myapps.append(item)
    #center = EsthenosOrgCenter.objects.filter(center_name=center_name)[0]

    resp = dict()
    applications_list = []
    #resp['center'] = center.name
    #resp['center_size'] = center.size
    if group!=None:
        resp['group'] =  group.group_name
        resp['group_size'] = group.size

    resp["applications"] = myapps

    return Response(response=json.dumps(resp),
        status=200,\
        mimetype="application/json")


@organisation_views.route('/admin/mobile/application', methods=['POST'])
@login_or_key_required
def mobile_application():
    username = current_user.name
    c_user = current_user
    import wtforms_json
    wtforms_json.init()
    user = EsthenosUser.objects.get(id=c_user.id)
    form= request.form
    print form
    center_name = request.form.get('center_name')
    group_name = request.form.get('group_name')
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

        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_name=group_name)
        EsthenosOrg.objects.get(id = user.organisation.id).update(inc__group_count=1)
    app_form=AddApplicationMobile(form)
    if(app_form.validate()):
        print "Form Validated"
        print "Saving Form"
        app_form.save()
        return Response(json.dumps({'status':'sucess'}), content_type="application/json", mimetype='application/json')
    else:
        print app_form.errors
        print "Could Not validate"
    kwargs = locals()
    return render_template("auth/login_admin.html", **kwargs)

import wtforms_json
wtforms_json.init()

@organisation_views.route('/mobile/application/json', methods=['POST'])
@login_or_key_required
def mobile_application_json():
    username = current_user.name
    c_user = current_user
    print request.json
    user = EsthenosUser.objects.get(id=c_user.id)
    form= request.json #get_json(force=True)
    print form
    center_name = request.json.get('center_name')
    group_name = request.json.get('group_name')
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

        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_name=group_name)
        EsthenosOrg.objects.get(id = user.organisation.id).update(inc__group_count=1)
    app_form=AddApplicationMobile.from_json(form)
    if(app_form.validate()):
        print "Form Validated"
        print "Saving Form"
        app_form.save()
        return Response(json.dumps({'status':'success'}), content_type="application/json", mimetype='application/json')
    else:
        print app_form.errors
        print "Could Not validate"
    kwargs = locals()
    return render_template("auth/login_admin.html", **kwargs)


@organisation_views.route('/upload_documents', methods=["GET","POST"])
@login_required
@feature_enable("enroll_customers")
def enroll_customers():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    if request.method == "GET":
        unique_key =  uuid.uuid4()
        session_obj =  EsthenosOrgUserUploadSession()
        session_obj.owner = user
        session_obj.unique_session_key = str(unique_key)
        session_obj.save()

        kwargs = locals()
        return render_template("upload_documents.html", **kwargs)

    elif request.method == "POST":
        center_name = request.form.get('i_center_name')
        group_name = request.form.get('i_group_name')
        if center_name is None:
            center_name = request.form.get('g_center_name')
            group_name = request.form.get('g_group_name')

        center, group = (None, None)
        if center_name is None:
            center_name = group_name

        if (center_name is not None) and len(center_name)>0 and (group_name is not None) and len(group_name)>0:
            unique_center_id = user.organisation.name.upper()[0:2]+"C"+"{0:06d}".format(user.organisation.center_count)
            center, status = EsthenosOrgCenter.objects.get_or_create(center_name=center_name, organisation=user.organisation)
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

        if (center is not None) or (group is not None):
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
                tagged_application.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=100)
                settings = EsthenosSettings.objects.all()[0]
                tagged_application.application_id = user.organisation.name.upper()[0:2]+str(settings.organisations_count)+"{0:06d}".format(inc_count)
                tagged_application.upload_type = "MANUAL_UPLOAD"
                tagged_application.status = 100
                tagged_application.save()
                inc_count = inc_count+1
                int_x = int_x+1

            EsthenosOrg.objects.get(id = user.organisation.id).update(inc__application_count=int_x)
            session_obj.center = center
            session_obj.group = group
            session_obj.tagged = True
            session_obj.save()

        unique_key = uuid.uuid4()
        session_obj = EsthenosOrgUserUploadSession()
        session_obj.owner = user
        session_obj.unique_session_key = str(unique_key)
        session_obj.save()

        kwargs = locals()
        return render_template("upload_documents.html", **kwargs)


@organisation_views.route('/check_disbursement', methods=["GET"])
@login_required
@feature_enable("disbursement")
def check_disbursement():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    centers = EsthenosOrgCenter.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("centers_n_groups_disbussment.html", **kwargs)


@organisation_views.route('/disburse_group', methods=["PUT"])
@login_required
@feature_enable("disbursement")
def disburse_document():
    if not session['role'].startswith("ORG_"):
        abort(403)

    print request.form.get("group_id")
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


@organisation_views.route('/download_disbursement', methods=["GET"])
@login_required
@feature_enable("disbursement")
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
                output.headers["Content-Disposition"] = "attachment; filename=%s.zip" %group_id
                output.headers["Content-type"] = "application/zip"
                return output
        print group.group_name
    return Response(json.dumps({"success":False},default=encode_model), content_type="application/json", mimetype='application/json')
    # Grab ZIP file from in-memory, make response with correct MIME-type


@organisation_views.route('/disbursement/download/<app_id>', methods=["GET","POST"])
@login_required
@feature_enable("disbursement")
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

