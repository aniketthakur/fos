from views_base import *
from esthenos.settings import APP_STATUS
import xml.etree.ElementTree as ET
from lxml import html

@organisation_views.route('/applications', methods=["GET"])
@login_required
def application_list():
  user = EsthenosUser.objects.get(id=current_user.id)
  org = user.organisation
  branches = EsthenosOrgBranch.objects.all()
  branchId = request.args.get('branchId', '')
  areaId = request.args.get('areaId', '')
  regionId = request.args.get('regionId', '')
  stateId = request.args.get('stateId', '')
  branch = ""
  area = ""
  region = ""
  state = ""

  hierarchy = EsthenosOrgHierarchy.objects.filter(organisation=org, role="ORG_ILE")

  fos_agents = []

  if (branchId is not None) and (branchId != ''):
    branch = EsthenosOrgBranch.objects.filter(id=branchId)

  if (areaId is not None) and (areaId != ''):
    area = EsthenosOrgArea.objects.filter(id=areaId)

  if (regionId is not None) and (regionId != ''):
    region = EsthenosOrgRegion.objects.filter(id=regionId)

  if (stateId is not None) and (stateId != ''):
    state = EsthenosOrgState.objects.filter(id=stateId)

  if branch:
    if fos_agents:
      fos_agents = fos_agents.filter(access_branches__in=branch)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org, hierarchy = hierarchy[0], access_branches__in=branch)

  if area:
    if fos_agents:
      fos_agents = fos_agents.filter(access_areas__in=area)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org,  hierarchy = hierarchy[0], access_areas__in=area)

  if region:
    if fos_agents:
      fos_agents = fos_agents.filter(access_regions__in=region)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org,  hierarchy = hierarchy[0], access_regions__in=region)

  if state:
    if fos_agents:
      fos_agents = fos_agents.filter(access_states__in=state)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org,  hierarchy = hierarchy[0], access_states__in=state)

  kwargs = locals()
  return render_template("apps/applications_centers_n_groups.html", **kwargs)


@organisation_views.route('/applications/fos/<fos_id>', methods=["GET"])
@login_required
def application_list_fos(fos_id):
  appId = request.args.get('appId', '')
  appName = request.args.get('appName', '')
  user = EsthenosUser.objects.get(id=current_user.id)
  fos_user = EsthenosUser.objects.get(id = fos_id)
  applications = EsthenosOrgApplication.objects.filter(owner= fos_user)

  title = "FOS: FOS Application"
  kwargs = locals()
  return render_template("apps/applications_list.html", **kwargs)


@organisation_views.route('/applications/branch/<branch_id>', methods=["GET"])
@login_required
def application_list_branch(branch_id):
  appId = request.args.get('appId', '')
  appName = request.args.get('appName', '')

  user = EsthenosUser.objects.get(id=current_user.id)
  org = user.organisation
  branch = EsthenosOrgBranch.objects.get(id=branch_id)

  applications = []
  if (appId is not None) and (appId != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=org, application_id=appId , branch = branch)

  elif (appName is not None) and (appName != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=org, applicant_name=appName, branch = branch)

  else:
    applications = EsthenosOrgApplication.objects.filter(organisation=org,branch = branch)

  title = "Branch: {branch}".format(branch=branch.name)
  kwargs = locals()
  return render_template("apps/applications_list.html", **kwargs)


@organisation_views.route('/application/<app_id>/cashflow', methods=["GET"])
@login_required
def application_cashflow(app_id):

  user = EsthenosUser.objects.get(id=current_user.id)
  applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, application_id=app_id)

  if len(applications) == 0:
    redirect("/application_status")

  app_urls = list()
  application = applications[0]

  kwargs = locals()
  return render_template("apps/application_cashflow.html", **kwargs)


@organisation_views.route('/application/<app_id>/update_status', methods=["GET", "POST"])
@login_required
def application_update_status(app_id):

  user = EsthenosUser.objects.get(id=current_user.id)
  applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, application_id=app_id)

  if len(applications) == 0:
    redirect("/application_status")

  app_urls = list()
  application = applications[0]

  statuslist = filter(lambda x: x['status_code'] >= 190 and x['status_code'] < application.status, APP_STATUS)
  status = application.status

  if request.method == "GET":
    kwargs = locals()
    return render_template("apps/application_update_status.html", **kwargs)

  if request.method == "POST":
      form = request.form
      application.update_status(int(form["app-status"]))
      application.save()
      return redirect(url_for("organisation_views.application_list_branch", branch_id=application.branch.id))


@organisation_views.route('/application/<app_id>/cashflow', methods=["POST"])
@login_required
def cashflow_statusupdate(app_id):

    user = EsthenosUser.objects.get(id=current_user.id)
    application = EsthenosOrgApplication.objects.filter(application_id=app_id)

    if len(application) >= 0:
      application = application[0]
      status = EsthenosOrgApplicationStatus(status=application.current_status, updated_on=datetime.datetime.now())
      status.save()
      application.timeline.append(status)


      application.total_annual_revenue_credit = float(request.form.get("Total Annual Revenue-Credit"))
      application.total_annual_revenue_cash =  float(request.form.get("Total Annual Revenue-Cash"))

      application.house_monthly_rent = float(request.form.get("monthly_rent"))
      application.average_monthly_bill = float(request.form.get("average_monthly_bill_phone"))
      application.electricity_monthly_bill = float(request.form.get("average_monthly_bill_electricity"))

      application.grocery_expenses = float(request.form.get("grocery_expenses"))
      application.conveyance_expenses = float(request.form.get("conveyance_expenses"))
      application.medical_expenses = float(request.form.get("medical_expenses"))
      application.education_expenses = float(request.form.get("education_expenses"))
      application.family_other_expenses = float(request.form.get("other_expenses"))
      application.monthly_rent = float(request.form.get("monthly_rent"))

      application.electricity_charges = float(request.form.get("electricity_charges"))
      application.petrol_expenses = float(request.form.get("petrol_expenses"))
      application.freight_charges = float(request.form.get("freight_charges"))
      application.salaries_and_wages = float(request.form.get("salaries_and_wages"))
      application.other_expenses = float(request.form.get("other_expenses"))

      application.loan_details1.emi_repayments = float(request.form.get("emi_payment1"))
      application.loan_details2.emi_repayments  = float(request.form.get("emi_payment2"))
      application.loan_details3.emi_repayments  = float(request.form.get("emi_payment3"))
      application.loan_details4.emi_repayments  = float(request.form.get("emi_payment4"))

      application.total_annual_purchase_cash = float(request.form.get("total_annual_purchase_cash"))
      application.total_annual_purchase_credit = float(request.form.get("total_annual_purchase_credit"))

    status_code = 170 if request.form.get("status") == "true" else 180
    application.update_status(status_code)
    application.save()

    return redirect("/application/%s/cashflow" % app_id)


@organisation_views.route('/application/<app_id>/track', methods=["GET"])
@login_required
def applications_track(app_id):
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(organisation=user.organisation, application_id=app_id)
  kwargs = locals()
  return render_template("apps/application_tracking.html", **kwargs)


@organisation_views.route('/scrutiny', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def scrutiny():
  user = EsthenosUser.objects.get(id = current_user.id)
  org = user.organisation
  branchId = request.args.get('branchId', None)
  areaId = request.args.get('areaId', '')
  regionId = request.args.get('regionId', '')
  stateId = request.args.get('stateId', '')
  branch = ""
  area = ""
  region = ""
  state = ""
  applications = []

  if (branchId is not None) and (branchId != ""):
    branch = EsthenosOrgBranch.objects.get(id=branchId)

  if (areaId is not None) and (areaId != ""):
    area = EsthenosOrgArea.objects.get(id=areaId)

  if (regionId is not None) and (regionId != ""):
    region = EsthenosOrgRegion.objects.get(id=regionId)

  if (stateId is not None) and (stateId != ""):
    state = EsthenosOrgState.objects.get(id=stateId)

  for i in EsthenosOrgApplication.objects.filter(organisation=user.organisation, status__gte=191):
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
      applications.append(i)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_list.html", **kwargs)


@organisation_views.route('/scrutiny/<app_id>', methods=["GET", "POST"])
@login_required
@feature_enable("features_applications_scrutiny")
def scrutiny_application(app_id):
  user = EsthenosUser.objects.get(id=current_user.id)
  today = datetime.datetime.now()
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  if request.method == "GET":
    kwargs = locals()
    return render_template("scrutiny/scrutiny_details.html", **kwargs)

  elif request.method == "POST":

    status_code, status = 191, request.form.get("status")
    if status == "approve":
        status_code, status = 193, "approved"

    elif status == "reject":
      status_code, status = 192, "rejected"

    elif status == "hold":
      status_code, status = 194, "onhold"

    scrutiny = EsthenosOrgApplicationScrutiny(
      owner = user,
      status = status,

      total_income = float(request.form.get("total_income")),
      total_expense = float(request.form.get("total_expenditure")),

      foir_ratio = float(request.form.get("fior")),
      total_ltv = float(request.form.get("total_ltv")),
      total_amount = float(request.form.get("total_amount")),

      memo_business_type = request.form.get("memo_business_type"),
      memo_business_name = request.form.get("memo_business_name"),
      memo_applicant_address = request.form.get("memo_applicant_address"),

      memo_loan_emi = float(request.form.get("memo_loan_emi")),
      memo_loan_amount = float(request.form.get("memo_loan_amount")),
      memo_loan_period = float(request.form.get("memo_loan_period")),
      memo_loan_interest = float(request.form.get("memo_loan_interest")),
      memo_loan_processing_fee = float(request.form.get("memo_loan_processing_fee"))
    )
    application.scrutiny = scrutiny
    application.update_status(status_code)
    application.save()

    return redirect(url_for("organisation_views.scrutiny"))

@organisation_views.route('/scrutiny/<app_id>/download', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def sheet_download(app_id):
    tmp_files = list()
    user = EsthenosUser.objects.get(id=current_user.id)
    application = EsthenosOrgApplication.objects.get(organisation=user.organisation, id=app_id)
    dir = "%s/" % tempfile.mkdtemp(prefix='pdf_')
    tfa = dir + app_id + "_readysheet.pdf"

    #TODO remove localhost
    downloadFile("http://localhost:8080/internal/datasheet/%s" % (app_id), tfa)
    tmp_files.append(tfa)

    tf = "%s/%s" % (tempfile.mkdtemp(prefix='zip_'), app_id)
    zip_custom(dir, tf)
    filehandle = open(tf + ".zip", 'rb')

    data = StringIO.StringIO(filehandle.read())
    output = make_response(data.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=%s.zip" % app_id
    output.headers["Content-type"] = "application/zip"
    return output


@organisation_views.route('/scrutiny/<app_id>/print', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def scrutiny_application_print(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_print.html", **kwargs)

@organisation_views.route('/sanctions', methods=["GET"])
@login_required
@feature_enable("features_applications_sanction")
def sanctions():
  user = EsthenosUser.objects.get(id=current_user.id)
  org = user.organisation
  branchId = request.args.get('branchId', None)
  areaId = request.args.get('areaId', '')
  regionId = request.args.get('regionId', '')
  stateId = request.args.get('stateId', '')
  branch = ""
  area = ""
  region = ""
  state = ""
  applications = []

  if (branchId is not None) and (branchId != ""):
    branch = EsthenosOrgBranch.objects.get(id=branchId)

  if (areaId is not None) and (areaId != ""):
    area = EsthenosOrgArea.objects.get(id=areaId)

  if (regionId is not None) and (regionId != ""):
    region = EsthenosOrgRegion.objects.get(id=regionId)

  if (stateId is not None) and (stateId != ""):
    state = EsthenosOrgState.objects.get(id=stateId)

  for i in EsthenosOrgApplication.objects.filter(organisation=user.organisation, status__gte=192):
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
      applications.append(i)

  kwargs = locals()
  return render_template("sanctions/sanctions_list.html", **kwargs)

@organisation_views.route('/balance_sheet/<app_id>', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def balancesheet_page(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  app = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/balance_sheet.html", **kwargs)

@organisation_views.route('/balance_sheet/<app_id>/print', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def balancesheet_page_print(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  app = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/balance_sheet_print.html", **kwargs)

@organisation_views.route('/deviation_sheet/<app_id>', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def deviation_page(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  app = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/deviation_sheet.html", **kwargs)

@organisation_views.route('/deviation_sheet/<app_id>/print', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def deviation_page_print(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  app = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/deviation_sheet_print.html", **kwargs)

@organisation_views.route('/banking_sheet/<app_id>', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def banking_page(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/banking_sheet.html", **kwargs)


@organisation_views.route('/banking_sheet/<app_id>/print', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def banking_page_print(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/banking_sheet_print.html", **kwargs)


@organisation_views.route('/sanctions/<app_id>', methods=["GET", "POST"])
@login_required
@feature_enable("features_applications_sanction")
def sanctions_application(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)
  credit_score = 0

  if application.highmark_response and ET.fromstring(application.highmark_response).find(".//PRINTABLE-REPORT/CONTENT"):
    html_content = ET.fromstring(application.highmark_response).find(".//PRINTABLE-REPORT/CONTENT").text
    html_tree = html.fromstring(html_content)
    credit_score = html_tree.xpath('//td[@class="dataValueValue"]')
    credit_score = 0 if not credit_score else credit_score[0].text

  if request.method == "GET":
    kwargs = locals()
    return render_template("sanctions/sanctions_details.html", **kwargs)

  elif request.method == "POST":

    status_code, status = 201, request.form.get("status")
    if status == "approve":
        status_code, status = 203, "approved"

    elif status == "reject":
      status_code, status = 202, "rejected"

    elif status == "hold":
      status_code, status = 204, "onhold"

    sanction = EsthenosOrgApplicationSanction(
      owner = user,
      status = status,

      total_income = float(request.form.get("total_income")),
      total_expense = float(request.form.get("total_expenditure")),

      foir_ratio = float(request.form.get("fior")),
      total_value = float(request.form.get("total_ltv")),
      total_amount = float(request.form.get("total_amount")),

      memo_business_type = request.form.get("memo_business_type"),
      memo_business_name = request.form.get("memo_business_name"),
      memo_applicant_address = request.form.get("memo_applicant_address"),

      memo_loan_emi = float(request.form.get("memo_loan_emi")),
      memo_loan_amount = float(request.form.get("memo_loan_amount")),
      memo_loan_period = float(request.form.get("memo_loan_period")),
      memo_loan_interest = float(request.form.get("memo_loan_interest")),
      memo_loan_processing_fee = float(request.form.get("memo_loan_processing_fee"))
    )
    application.sanction = sanction
    application.update_status(status_code)
    application.save()

    return redirect(url_for("organisation_views.sanctions"))


@organisation_views.route('/sanctions/<app_id>/print', methods=["GET"])
@login_required
@feature_enable("features_applications_sanction")
def sanctions_application_print(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("sanctions/sanctions_details_print.html", **kwargs)


@organisation_views.route('/sanctions/<app_id>/highmarkreport/print', methods=["GET"])
@login_required
@feature_enable("features_applications_scrutiny")
def sanction_application_highmarkreport_print(app_id):
    today = datetime.datetime.now()
    user = EsthenosUser.objects.get(id=current_user.id)
    application = EsthenosOrgApplication.objects.get(organisation=user.organisation, id=app_id)
    content = ""

    if request.method == "GET":
        user = EsthenosUser.objects.get(id=current_user.id)
        application = EsthenosOrgApplication.objects.get(organisation=user.organisation, id=app_id)
        response = application.highmark_response
        content = ""

        if response and ET.fromstring(response).find(".//PRINTABLE-REPORT/CONTENT") is not None:
            content = ET.fromstring(response).find(".//PRINTABLE-REPORT/CONTENT").text

    return content
