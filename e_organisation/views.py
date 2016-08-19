from views_base import *

# import views for user applications.
from views_apps import *

# import views for cbcheck functionalities.
from views_cbcheck import *

# import views for feature - psychometric test.
from views_psychometric import *
from esthenos import settings
from flask import jsonify

from e_highmark import utils

@organisation_views.route('/', methods=["GET"])
@login_required
def home_page():
    user = EsthenosUser.objects.get(id=current_user.id)
    date = request.args.get('date', datetime.datetime.now().strftime("%Y%m%d"))
    time = datetime.datetime.strptime(date, "%Y%m%d")
    month = user.stats(time)
    todays, weekly, monthly = month.only(time), month.week(time), month.day(time)

    focus = settings.SERVER_SETTINGS["location"]

    kwargs = locals()
    return render_template("dashboard.html", **kwargs)


@organisation_views.route('/api/organisation/branches', methods=["GET"])
@login_or_key_required
@feature_enable("features_fos_branches")
def centers_list():
    user = EsthenosUser.objects.get(id=current_user.id)

    if user.hierarchy.role == "ORG_CE":
        branches = user.branches

    if user.hierarchy.role == "ORG_ILE":
        branches = user.branches

    if branches is not []:
        return jsonify({
            "count" : len(branches),
            "branches" : [branch.json for branch in branches]
        })
    else:
        return jsonify({
            "success": False,
            "message": "Please assign states to ce"
        })

@organisation_views.route('/profile', methods=["GET","POST"])
@login_required
@feature_enable("features_profile")
def user_profile_page():
    user = EsthenosUser.objects.get(id=current_user.id)
    kwargs = locals()
    return render_template("user_profile.html", **kwargs)


@organisation_views.route('/reports', methods=["GET", "POST"])
@login_required
def reports_internal_main():
    user = EsthenosUser.objects.get(id=current_user.id)

    if request.method == "GET":
        kwargs = locals()
        return render_template("client_reports.html", **kwargs)

    if request.method == "POST":
        applications = []
        application_data = [
          get_application_headers()
        ]

        report_name = "internal_report.csv"
        report_end = request.form.get("end-date")
        report_start = request.form.get("start-date")

        if (report_start is None) or (report_end is None):
            report_name = "internal_full_report.csv"
            applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

        else:
            from datetime import datetime
            endDate = datetime.strptime(report_end, "%m/%d/%Y")
            startDate = datetime.strptime(report_start, "%m/%d/%Y")
            report_name = "internal_range_report.csv"
            applications = EsthenosOrgApplication.objects.filter(date_created__gte=startDate, date_created__lte=endDate, organisation=user.organisation)

        for app in applications:
            app_row_data = get_application_rowdata(app)
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=%s" % report_name
        output.headers["Content-type"] = "text/csv"
        return output


@organisation_views.route('/notifications', methods=["GET"])
@login_required
@feature_enable("features_notifications")
def notifications_page():
    user = EsthenosUser.objects.get(id=current_user.id)

    notifications = EsthenosOrgNotification.objects.filter(to_user=user, read_state=False)
    notifications_read = EsthenosOrgNotification.objects.filter(to_user=user, read_state=False).update(set__read_state=True)

    count = len(notifications)
    kwargs = locals()
    return render_template("notifications.html", **kwargs)


@organisation_views.route('/organisation/cheque_info/<group_id>', methods=["POST"])
@login_required
def cheque_info_import(group_id):
    c_user = current_user
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


@organisation_views.route('/api/user/performance', methods=["GET"])
@login_or_key_required
@feature_enable("features_api_performance_target")
def performance():
    user = EsthenosUser.objects.get(id=current_user.id)
    performance, status = EsthenosOrgUserPerformance.objects.get_or_create(owner=user)
    return Response(json.dumps(performance.json), content_type="application/json", mimetype='application/json')


@organisation_views.route('/api/organisation/applications', methods=["GET"])
@login_or_key_required
@feature_enable("features_api_applications_list")
def get_application():
    user = EsthenosUser.objects.get(id=current_user.id)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

    applications_list = list()
    for app in applications:
        item = {
            "id" : app.application_id,
            "date_created" : str(app.date_created),
            "applicant_name" : app.applicant_name,
            "current_status" : app.current_status.status_message
        }
        # "loan_eligibility_based_on_net_income" : app.loan_eligibility_based_on_net_income(),
        #     "loan_eligibility_based_on_company_policy" : app.loan_eligibility_based_on_company_policy
        applications_list.append(item)

    resp = dict()
    resp["applications"] = applications_list
    return Response(response=json.dumps(resp), status=200, mimetype="application/json")


import wtforms_json
wtforms_json.init()

@organisation_views.route('/api/organisation/applications', methods=['POST'])
@login_or_key_required
@feature_enable("features_api_applications_post")
def mobile_application_json():
    app_form = AddApplicationMobile.from_json(request.json)

    try:
        applicationID = request.json.get('application_id', '')
        mainapp.logger.debug("applicationID: %s " % applicationID)
        app = EsthenosOrgApplication.objects.get(application_id=applicationID) if applicationID else ''
    except:
        app = ''

    # app = app[0] if app else ''
    # TODO: IMPROVE THE CODE

    if app:
        if app.is_registered:
            return jsonify({
                "success": False,
                "message": "application submission failed"
            })
    else:
        app = ''

    mainapp.logger.debug("app: %s " % len(app))
    if app_form.validate():
        app_form.save(app)
        return jsonify({
            "success": True,
            "message": "application submission successful"
        })

    return jsonify({
        "success": False,
        "message": "application submission failed: %s" % str(app_form.errors)
    })

    # user = EsthenosUser.objects.get(id=current_user.id)
    # app_form = AddApplicationMobile.from_json(request.json)
    #
    # if app_form.validate():
    #     print "Form Validated, Saving."
    #     app_form.save()
    #     return Response(json.dumps({'success':'true'}), content_type="application/json", mimetype='application/json')
    #
    # else:
    #     print "Could Not validate" + str(app_form.errors)
    #     return Response(json.dumps({'success':'false'}), content_type="application/json", mimetype='application/json')

@organisation_views.route('/check_disbursement', methods=["GET"])
@login_required
@feature_enable("features_applications_disbursement")
def check_disbursement():
    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation
    branchId = request.args.get('branchId', '')
    areaId = request.args.get('areaId', '')
    regionId = request.args.get('regionId', '')
    stateId = request.args.get('stateId', '')
    branch = ""
    area = ""
    region = ""
    state = ""

    apps = []

    if (branchId is not None) and (branchId != ''):
        branch = EsthenosOrgBranch.objects.get(id=branchId)

    if (areaId is not None) and (areaId != ""):
        area = EsthenosOrgArea.objects.get(id=areaId)

    if (regionId is not None) and (regionId != ""):
        region = EsthenosOrgRegion.objects.get(id=regionId)

    if (stateId is not None) and (stateId != ""):
        state = EsthenosOrgState.objects.get(id=stateId)

    for i in EsthenosOrgApplication.objects.filter(organisation=user.organisation, status=240):
        t = ""
        if branch and i.branch == branch:
            t = i
        if area:
            if t and not t.branch.parent == area:
                t = ''
            elif not t and i.branch.parent == area:
                t = i
        if region:
            if t and not t.branch.parent.parent == region:
                t = ''
            elif not t and i.branch.parent.parent == region:
                t = i
        if state:
            if t and not t.branch.parent.parent.parent == state:
                t = ''
            elif not t and i.branch.parent.parent.parent == state:
                t = i
        if t:
            apps.append(i)

    kwargs = locals()
    return render_template("disburse/disbursement.html", **kwargs)


@organisation_views.route('/disburse_group', methods=["PUT"])
@login_required
@feature_enable("features_applications_disbursement")
def disburse_document():
    applicant_id = request.form.get("applicant_id")
    col_date_str = request.form.get("collection_date")
    dis_date_str = request.form.get("disbursement_date")

    user = EsthenosUser.objects.get(id=current_user.id)
    org  = user.organisation
    apps = EsthenosOrgApplication.objects.filter(organisation=org, status__gte=240)

    dis_date = datetime.datetime.strptime(dis_date_str, "%d-%m-%Y").date()
    col_date = datetime.datetime.strptime(col_date_str, "%d-%m-%Y").date()

    generate_post_grt_applications.apply_async((org.id, applicant_id, dis_date_str, (col_date-dis_date).days))
    for app in apps:
        app.generate_disbursement = True
        app.save()

    kwargs = locals()
    response = {"result":"We are preparing your download document, please wait !"}
    return Response(json.dumps(response, default=encode_model), content_type="application/json", mimetype='application/json')


@organisation_views.route('/download_disbursement/<applicant_id>', methods=["GET"])
@login_required
@feature_enable("features_applications_disbursement")
def download_disbursement(applicant_id):
    user = EsthenosUser.objects.get(id=current_user.id)
    app = EsthenosOrgApplication.objects.get(organisation=user.organisation, application_id=applicant_id)
    bucket = conn_s3.get_bucket(settings.AWS_SETTINGS['AWS_S3_BUCKET'])
    bucket_list = bucket.list()

    for item in bucket_list:
        print item, item.key, app.disbursement_pdf_link
        if app.disbursement_pdf_link[1:] == item.key:
            # check if file exists locally, if not: download it
            if not os.path.exists(app.disbursement_pdf_link):
                item.get_contents_to_filename(app.disbursement_pdf_link)

            filehandle = open(app.disbursement_pdf_link, 'rb')
            data = StringIO.StringIO(filehandle.read())
            output = make_response(data.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=%s.zip" % applicant_id
            output.headers["Content-type"] = "application/zip"
            return output

    return Response(json.dumps({"success":False},default=encode_model), content_type="application/json", mimetype='application/json')


@organisation_views.route('/api/organisation/centers/branches/application/update_neighbor', methods=["POST"])
@login_or_key_required
@feature_enable("features_api_applications_list")
def neighbour_complete_list():
    user = EsthenosUser.objects.get(id=current_user.id)

    if request.method == 'POST':
        form = request.json
        application = EsthenosOrgApplication.objects.get(application_id=form['applicant_id'])

        if application:
            application.update_neighbor_data(form)
            application.save()

            return jsonify({
                "success": True,
                "message": "neighbor submission successful"
            })
        else:
            return jsonify({
                "success": False,
                "message": "neighbor submission unsuccessful"
            })

@organisation_views.route('/api/organisation/luc_submission', methods=["POST"])
@login_or_key_required
@feature_enable("features_api_applications_list")
def luc_submission():
    user = EsthenosUser.objects.get(id=current_user.id)

    if request.method == 'POST':
        loan = request.form.get("loan","")
        date = request.form.get("date","")
        remarks = request.form.get("remarks","")
        application_id = request.form.get("app_id","")
        app = EsthenosOrgApplication.objects.get(application_id = application_id)
        app.luc_remarks = remarks
        app.luc_loan = loan
        app.luc_date = date
        app.update_status(245)
        app.save()

        return jsonify({
                "success": True,
                "message": "luc submission successful"
            })

@organisation_views.route('/api/organisation/mv_submission', methods=["POST"])
@login_or_key_required
@feature_enable("features_api_applications_list")
def mv_submission():
    user = EsthenosUser.objects.get(id=current_user.id)

    if request.method == 'POST':
        visit_Date = request.form.get("visit_Date","")
        remarks = request.form.get("remarks","")
        application_id = request.form.get("app_id","")
        app = EsthenosOrgApplication.objects.get(application_id = application_id)
        app.mv_date = visit_Date
        app.mv_remarks = remarks
        app.update_status(247)
        app.save()
        return jsonify({
                "success": True,
                "message": "mv submission successful"
            })


@organisation_views.route('/api/organisation/applications/pre_register', methods=['POST'])
@login_or_key_required
@feature_enable("features_api_applications_post")
def application_pre_register_group():

    from e_highmark import parse_response as pr
    import xml.etree.ElementTree as ET
    import esthenos

    form = request.json
    application_params = {}
    address_params = {}
    applicant_params = {}

    user = EsthenosUser.objects.get(id=current_user.id)
    user.organisation.update(inc__application_count=1)
    applicant = form["applicant_other_card_cbcheck"]
    branch = EsthenosOrgBranch.objects.get(id=form['branch'])
    app = EsthenosOrgApplication(
            applicant_name=applicant['name'],
            owner=user,
            organisation=user.organisation,
            branch = branch
        )

    app.update_status(105)
    app.update_status(110)
    app.update_status(120)
    app.update_status(125)
    app.update_status(126)
    app.update_status(130)
    app.is_pre_registered = True
    app.save()
    app_count = EsthenosOrg.objects.get(id=user.organisation.id).application_count + 1
    app.application_id = user.organisation.name.upper()[0:2] + user.organisation.code + "{0:07d}".format(app_count)
    app.save()

    applicant_params, address_params, application_params = app.get_params_for_pre_highmark(applicant)
    response = pr.handle_request_response(applicant_params, address_params, application_params)
    # fo = open("resp.txt","wb")
    # fo.write(response.text)
    # fo.close()
    if response.status_code == 200 and ET.fromstring(response.content).find("./INDV-REPORTS") is not None:
        app.highmark_response = response.text

        response_p = ET.fromstring(response.content)

        # app.update_cashflow(response_p)
        app.highmark_response = response.content
        temp = pr.get_valules_from_highmark_response(response_p)
        highmark_response = EsthenosOrgApplicationHighMarkResponse(
            national_id_card = pr.get_national_id_card(response_p),
            num_active_account = pr.get_num_active_account(response_p),
            sum_overdue_amount = pr.get_sum_overdue_amount(response_p),
            indv_response_list = temp[0],
            total_loan_balance = temp[1],
            total_dpd_count = temp[2]
        )
        highmark_response.save()
        # highmark_response.indv_response_list = temp[0]
        # highmark_response.toal_loan_balance = temp[1]
        # highmark_response.total_dpd_count = temp[2]
        # highmark_response.save()
        app.highmark_response1 = highmark_response
        app.update_status(140)
        app.save()

        app.update_status(145)
        app.update_status(150)
        app.update_status(160)

        app.update_status(170)
        app.update_status(126)
        app.update_status(185)
        app.save()
        # highmark_status = HighmarkStatus.objects.get(organisation=user.organisation)
        #
        # highmark_status.update_status([response])
        # highmark_status.save()

        # resp = app.highmark_response1
        # app.update_cashflow_from_highmark_response_1(resp)

    return jsonify({
        "success": True,
        "application_id": str(app.application_id),
        "message": "application pre register successful"
    })

@organisation_views.route('/api/organisation/branches/<branchid>/applications/<state>', methods=["GET"])
@login_or_key_required
@feature_enable("features_api_applications_list")
def application_get_group(branchid,state):
    user = EsthenosUser.objects.get(id=current_user.id)
    branch = EsthenosOrgBranch.objects.get(id=branchid)

    if state == "pre_registration":
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch,status=185)
    elif state == "neighbor_feedback":
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch,status=187)
    elif state == "luc_ready":
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch,status=244)
    elif state == "mv_ready":
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch,status=246)
    else:
        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch)

    passed_app_count = 0
    applications_list = []
    for app in applications:
        #ADDED : CONSIDERING OLD APPLICAITONS
        applicant_name = app.applicant_kyc.name.strip().split(' ')
        applicant_name = applicant_name[1:] if applicant_name[0] in ['Mr.', 'Mrs.', 'Miss'] else applicant_name
        applicant_name = ' '.join(applicant_name)
        # "loan_eligibility_based_on_net_income" : app.loan_eligibility_based_on_net_income(),
        #  "loan_eligibility_based_on_company_policy" : int(app.loan_eligibility_based_on_company_policy),
        item = {
            "date_created" : str(app.date_created),
            "applicant_name_title" : app.applicant_kyc.name.strip().split(' ')[0],
            "applicant_name" : applicant_name,
            "spouse_name_title" : app.applicant_kyc.spouse_name.strip().split(' ')[0],
            "spouse_name" : ' '.join(app.applicant_kyc.spouse_name.strip().split(' ')[1:]),
            "current_status" : app.current_status.status_message,
            "address": app.applicant_kyc.address,
            "age": app.applicant_kyc.age,
            "dob": str(app.applicant_kyc.dob),
            "id": app.application_id,
            "mobile_no": app.applicant_kyc.mobile_number,
            "mother_name_title": app.applicant_kyc.mothers_name.strip().split(' ')[0],
            "mother_name": ' '.join(app.applicant_kyc.mothers_name.strip().split(' ')[1:]),
            "father_name": ' '.join(app.applicant_kyc.father_or_husband_name.strip().split(' ')[1:]),
            "father_name_title": app.applicant_kyc.father_or_husband_name.strip().split(' ')[0],
            "state": app.applicant_kyc.state,
            "pincode": app.applicant_kyc.pincode,
            "district": app.applicant_kyc.district,
            "voter_id": app.applicant_kyc.voterid,
            "ration_id": app.applicant_kyc.ration_id,
            "kyc_number": app.applicant_kyc.kyc_number,
            "pan_card_id": app.applicant_kyc.pancard_id
        }

        s = ""

        item["loan"] = s
        item["loan_total"] = ""
        item["loan_default"] = ""
        # item["is_neighbor_complete"] = app.is_neighbor_complete

        if app.highmark_response1:
            for i in app.highmark_response1.indv_response_list:
                if i.is_prohibited:
                    s = s + str(i.mfi_name) + " " + str(i.loan_info_as_on) + " " + str(i.loan_balance) + " " + str(i.dpd_60+i.dpd_90) + " \n"

        item["loan"] = s
        s2 = ""
        bal = 0
        dpd = 0
        if app.highmark_response:
            s2, bal, dpd = utils.get_loan_bal_dpd_from_highmark_response(app.highmark_response)

        s2 = s2.strip()
        item["loan"] = s2
        item["loan_total"] = "Total Balance : " + str(bal)
        item["loan_default"] = "Total Default : " + str(dpd)
        item["status"] = 0
        item["register_complete"] = "yes" if 186 in [status.status.status_code for status in app.timeline] else "no"
        item["is_blocked"] = "yes" if app.is_pre_registered and not app.is_registered else "no"

        if not (app.status <= 26 or app.status in [180, 222, 192, 202, 212, 241]):
            item["status"] = 1

        applications_list.append(item)

        # Text searching for keyword `failed` in App Status
        if 'failed' not in app.current_status.status.lower():
            passed_app_count += 1

    response = {}
    response["applications"] = applications_list
    response['validated_applications'] = passed_app_count

    return Response(response=json.dumps(response), status=200, mimetype="application/json")