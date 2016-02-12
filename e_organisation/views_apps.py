from views_base import *


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

  hierarchy = EsthenosOrgHierarchy.objects.get(organisation=org, role="ORG_CM")

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
      fos_agents = EsthenosUser.objects.filter(organisation=org, hierarchy=hierarchy, access_branches__in=branch)

  if area:
    if fos_agents:
      fos_agents = fos_agents.filter(access_areas__in=area)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org, hierarchy=hierarchy, access_areas__in=area)

  if region:
    if fos_agents:
      fos_agents = fos_agents.filter(access_regions__in=region)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org, hierarchy=hierarchy, access_regions__in=region)

  if state:
    if fos_agents:
      fos_agents = fos_agents.filter(access_states__in=state)
    else:
      fos_agents = EsthenosUser.objects.filter(organisation=org, hierarchy=hierarchy, access_states__in=state)

  kwargs = locals()
  return render_template("apps/applications_centers_n_groups.html", **kwargs)


@organisation_views.route('/applications/fos/<fos_id>', methods=["GET"])
@login_required
def application_list_fos(fos_id):
  appId = request.args.get('appId', '')
  appName = request.args.get('appName', '')

  user = EsthenosUser.objects.get(id=current_user.id)
  fos_agent = EsthenosUser.objects.get(id=fos_id)

  if (appId is not None) and (appId != ''):
    applications = EsthenosOrgApplication.objects.filter(owner=fos_agent, application_id=appId)

  elif (appName is not None) and (appName != ''):
    applications = EsthenosOrgApplication.objects.filter(owner=fos_agent, applicant_name=appName)

  else:
    applications = EsthenosOrgApplication.objects.filter(owner=fos_agent)

  title = "FOS: {fname} {lname}".format(fname=fos_agent.first_name, lname=fos_agent.last_name)
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
    applications = EsthenosOrgApplication.objects.filter(organisation=org, application_id=appId)

  elif (appName is not None) and (appName != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=org, applicant_name=appName)

  else:
    applications = EsthenosOrgApplication.objects.filter(organisation=org)

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

      application.primary_business_income_monthly = float(request.form.get("primary_income"))
      application.tertiary_business_income_monthly = float(request.form.get("tertiary_income"))
      application.secondary_business_income_monthly = float(request.form.get("secondary_income"))
      application.other_income = float(request.form.get("other_income"))

      application.food_expense = float(request.form.get("food_expense"))
      application.other_expense = float(request.form.get("other_expense"))
      application.travel_expense = float(request.form.get("travel_expense"))
      application.medical_expense = float(request.form.get("medical_expense"))
      application.festival_expense = float(request.form.get("festival_expenditure"))
      application.educational_expense = float(request.form.get("educational_expense"))
      application.entertainment_expense = float(request.form.get("entertainment_expense"))

      application.primary_business_expense_rent = float(request.form.get("business_expense_rent"))
      application.primary_business_expense_admin = float(request.form.get("business_expense_admin"))
      application.primary_business_expense_other = float(request.form.get("business_expense_other"))
      application.primary_business_expense_working_capital = float(request.form.get("business_expense_working_capital"))
      application.primary_business_expense_employee_salary = float(request.form.get("business_expense_employee_salary"))
      application.tertiary_business_expenses_monthly = float(request.form.get("tertiary_business_expense"))
      application.secondary_business_expenses_monthly = float(request.form.get("secondary_business_expense"))

      application.other_outstanding_emi = float(request.form.get("other_outstanding_emi"))
      application.other_outstanding_chit = float(request.form.get("other_outstanding_chit"))
      application.other_outstanding_insurance = float(request.form.get("other_outstanding_insurance"))
      application.oother_outstanding_familynfriends = float(request.form.get("other_outstanding_familynfriends"))

      application.expected_tenure_in_months = int(request.form.get("expected_tenure_in_months"))
      application.expected_emi_amount_served = float(request.form.get("expected_emi_amount_served"))

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
  applications = []
  if (branchId is not None) and (branchId != ""):
      branch = EsthenosOrgBranch.objects.get(id=branchId)
      applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch, status__gte=191)

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
    application.scrutiny = scrutiny
    application.update_status(status_code)
    application.save()

    return redirect(url_for("organisation_views.scrutiny"))


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

  applications = []
  if (branchId is not None) and (branchId != ""):
      branch = EsthenosOrgBranch.objects.get(id=branchId)
      applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, branch=branch, status__gte=192)

  kwargs = locals()
  return render_template("sanctions/sanctions_list.html", **kwargs)


@organisation_views.route('/sanctions/<app_id>', methods=["GET", "POST"])
@login_required
@feature_enable("features_applications_sanction")
def sanctions_application(app_id):
  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

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
