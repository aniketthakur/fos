from views_base import *

# import views for user applications.
from views_apps import *

# import views for cbcheck functionalities.
from views_cbcheck import *

# import views for feature - psychometric test.
from views_psychometric import *


@organisation_views.route('/', methods=["GET"])
@login_required
def home_page():
    t = datetime.datetime.now()
    user = EsthenosUser.objects.get(id=current_user.id)

    hour = datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour)
    hourly, status = EsthenosOrgStats.objects.get_or_create(
      organisation=user.organisation, starttime=hour, granularity="HOURLY"
    )

    today = datetime.datetime(year=t.year, month=t.month, day=t.day, hour=0)
    todays, status = EsthenosOrgStats.objects.get_or_create(
      organisation=user.organisation, starttime=today, granularity="TODAY"
    )

    #todo: fix start of the week.
    week = datetime.datetime(year=t.year, month=t.month, day=1)
    weekly, status = EsthenosOrgStats.objects.get_or_create(
      organisation=user.organisation, starttime=week, granularity="WEEKLY"
    )

    month = datetime.datetime(year=t.year, month=t.month, day=1)
    monthly, status = EsthenosOrgStats.objects.get_or_create(
      organisation=user.organisation, starttime=month, granularity="MONTHLY"
    )

    kwargs = locals()
    return render_template("dashboard.html", **kwargs)


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


@organisation_views.route('/api/user/performance', methods=["GET"])
@login_or_key_required
@feature_enable("features_api_performance_target")
def performance():
    user = EsthenosUser.objects.get(id=current_user.id)
    performance, status = EsthenosOrgUserPerformance.objects.get_or_create(owner=user)
    return Response(json.dumps(performance.json), content_type="application/json", mimetype='application/json')


@organisation_views.route('/api/organisation/products', methods=["GET"])
@login_or_key_required
@feature_enable("features_api_products")
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
            "current_status" : app.current_status.status_message,
            "loan_eligibility_based_on_net_income" : app.loan_eligibility_based_on_net_income(),
            "loan_eligibility_based_on_company_policy" : app.loan_eligibility_based_on_company_policy
        }
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

    print request.json
    user = EsthenosUser.objects.get(id=current_user.id)
    app_form = AddApplicationMobile.from_json(request.json)

    if app_form.validate():
        print "Form Validated, Saving."
        app_form.save()
        return Response(json.dumps({'success':'true'}), content_type="application/json", mimetype='application/json')

    else:
        print "Could Not validate" + str(app_form.errors)
        return Response(json.dumps({'success':'false'}), content_type="application/json", mimetype='application/json')


@organisation_views.route('/check_disbursement', methods=["GET"])
@login_required
@feature_enable("features_applications_disbursement")
def check_disbursement():
    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation
    apps = EsthenosOrgApplication.objects.filter(organisation=user.organisation, status__gte=240)

    kwargs = locals()
    return render_template("disburse/disbursement.html", **kwargs)


@organisation_views.route('/disburse_group', methods=["PUT"])
@login_required
@feature_enable("features_applications_disbursement")
def disburse_document():
    applicant_id = request.form.get("applicant_id")
    col_date_str = request.form.get("collection_date")
    dis_date_str = request.form.get("disbursement_date")
    print applicant_id, col_date_str, dis_date_str

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
    bucket = conn_s3.get_bucket("hindusthanarchives")
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
