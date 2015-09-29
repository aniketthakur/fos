from views_base import *


@organisation_views.route('/applications', methods=["GET"])
@login_required
def application_list():
  if not session['role'].startswith("ORG_"):
      abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  org = user.organisation
  branches = EsthenosOrgBranch.objects.all()

  fosId = request.args.get('fosId', '')
  branchId = request.args.get('branchId', '')

  if (fosId is not None) and (fosId != ''):
    fos_agents = EsthenosUser.objects.filter(organisation=org, roles__contains="ORG_CM", id=fosId)

  elif (branchId is not None) and (branchId != ''):
    fos_agents = EsthenosUser.objects.filter(organisation=org, roles__contains="ORG_CM", org_branch=branchId)

  else:
    fos_agents = EsthenosUser.objects.filter(organisation=org, roles__contains="ORG_CM")

  kwargs = locals()
  return render_template("apps/applications_centers_n_groups.html", **kwargs)


@organisation_views.route('/applications/fos/<fos_id>', methods=["GET"])
@login_required
def application_list_fos(fos_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

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
  if not session['role'].startswith("ORG_"):
    abort(403)

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

  title = "Branch: {branch}".format(branch=branch.branch_name)
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

      if request.form.get("status") == "true":
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=170)[0]
        application.current_status_updated = datetime.datetime.now()
        application.status = 170

      else:
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=180)[0]
        application.current_status_updated = datetime.datetime.now()
        application.status = 170

      application.save()

    return redirect("/application/%s/cashflow" % app_id)


@organisation_views.route('/application/<app_id>/track', methods=["GET"])
@login_required
def applications_track(app_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(organisation=user.organisation, application_id=app_id)
  kwargs = locals()
  return render_template("apps/application_tracking.html", **kwargs)


@organisation_views.route('/application/<app_id>/kyc', methods=["GET"])
@login_required
def application_kyc(app_id):

  user = EsthenosUser.objects.get(id=current_user.id)
  applications = EsthenosOrgApplication.objects.filter(application_id=app_id)

  if len(applications) == 0:
    redirect("/applications")

  app_urls = []
  kyc_urls, kyc_ids = [], []
  gkyc_urls, gkyc_ids = [], []
  application = applications[0]

  if application.tag is not None:
    for kyc_id in application.tag.app_file_pixuate_id:
      app_urls.append(get_url_with_id(kyc_id))

    for kyc_id_key in application.tag.kyc_file_pixuate_id.keys():
      kyc_id = application.tag.kyc_file_pixuate_id[kyc_id_key]
      kyc_ids.append(kyc_id)
      kyc_urls.append(get_url_with_id(kyc_id))

    for gkyc_id_key in application.tag.gkyc_file_pixuate_id.keys():
      gkyc_id = application.tag.gkyc_file_pixuate_id[gkyc_id_key]
      gkyc_ids.append(gkyc_id)
      gkyc_urls.append(get_url_with_id(gkyc_id))

  today = datetime.datetime.today()
  disbursement_date = datetime.datetime.today() + timedelta(days=1)
  disbursement_date_str = disbursement_date.strftime('%d/%m/%Y')
  products = EsthenosOrgProduct.objects.filter(organisation=application.owner.organisation)

  kwargs = locals()
  return render_template("apps/application_details.html", **kwargs)


@organisation_views.route('/scrutiny', methods=["GET"])
@login_required
@feature_enable("accounts_scrutiny")
def scrutiny():
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id = current_user.id)
  groups = EsthenosOrgGroup.objects.filter(organisation = user.organisation)

  appId = request.args.get('appId', '')
  appName = request.args.get('appName', '')
  groupId = request.args.get('groupId', '')
  groupName = request.args.get('groupName', '')
  centerName = request.args.get('centerName', '')
  scrutinyStatus = request.args.get('scrutinyStatus', '')

  if (appId is not None) and (appId != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, application_id=appId)

  elif (appName is not None) and (appName != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, applicant_name=appName)

  elif (groupId is not None) and (groupId != ''):
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=groupId)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, group=group)

  elif (groupName is not None) and (groupName != ''):
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_name=groupName)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, group=group)

  elif (centerName is not None) and (centerName != ''):
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, location_name=centerName)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, group=group)

  else:
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_list.html", **kwargs)


@organisation_views.route('/scrutiny/<app_id>', methods=["GET", "POST"])
@login_required
@feature_enable("accounts_scrutiny")
def scrutiny_application(app_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  if request.method == "GET":
    today = datetime.datetime.now()
    user = EsthenosUser.objects.get(id=current_user.id)
    application = EsthenosOrgApplication.objects.get(application_id=app_id)

    print application.applicant_docs

    kwargs = locals()
    return render_template("scrutiny/scrutiny_details.html", **kwargs)


  elif request.method == "POST":
    return redirect(url_for("organisation_views.scrutiny"))


@organisation_views.route('/scrutiny/<app_id>/print', methods=["GET"])
@login_required
@feature_enable("accounts_scrutiny")
def scrutiny_application_print(app_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  today = datetime.datetime.now()
  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_print.html", **kwargs)


@organisation_views.route('/sanctions', methods=["GET"])
@login_required
@feature_enable("accounts_sanctions")
def sanctions():
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  groups = EsthenosOrgGroup.objects.filter(organisation=user.organisation)

  appId = request.args.get('appId', '')
  appName = request.args.get('appName', '')
  groupId = request.args.get('groupId', '')
  groupName = request.args.get('groupName', '')
  centerName = request.args.get('centerName', '')
  scrutinyStatus = request.args.get('scrutinyStatus', '')

  if (appId is not None) and (appId != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, application_id=appId)

  elif (appName is not None) and (appName != ''):
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, applicant_name=appName)

  elif (groupId is not None) and (groupId != ''):
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=groupId)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, group=group)

  elif (groupName is not None) and (groupName != ''):
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_name=groupName)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, group=group)

  elif (centerName is not None) and (centerName != ''):
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, location_name=centerName)
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, group=group)

  else:
    applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, status__gte=0)

  kwargs = locals()
  return render_template("sanctions/sanctions_list.html", **kwargs)


@organisation_views.route('/sanctions/<app_id>', methods=["GET", "POST"])
@login_required
@feature_enable("accounts_sanctions")
def sanctions_application(app_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  if request.method == "GET":
    today = datetime.datetime.now()
    user = EsthenosUser.objects.get(id=current_user.id)
    application = EsthenosOrgApplication.objects.get(application_id=app_id)

    kwargs = locals()
    return render_template("sanctions/sanctions_details.html", **kwargs)


  elif request.method == "POST":
    return redirect(url_for("organisation_views.sanctions"))
