from views_base import *


@organisation_views.route('/applications', methods=["GET"])
@login_required
def application_list():
  if not session['role'].startswith("ORG_"):
      abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  org  = user.organisation

  groupId = request.args.get('groupId', '')
  groupName = request.args.get('groupName', '')
  centerName = request.args.get('centerName', '')

  if (groupId is not None) and (groupId != ''):
    groups = EsthenosOrgGroup.objects.filter(organisation=org, group_id=groupId)

  elif (groupName is not None) and (groupName != ''):
    groups = EsthenosOrgGroup.objects.filter(organisation=org, group_name=groupName)

  elif (centerName is not None) and (centerName != ''):
    groups = EsthenosOrgGroup.objects.filter(organisation=org, location_name=centerName)

  else:
    groups = EsthenosOrgGroup.objects.filter(organisation=org)

  kwargs = locals()
  return render_template("apps/applications_centers_n_groups.html", **kwargs)


@organisation_views.route('/applications/group/<group_id>', methods=["GET"])
@login_required
def application_list_group(group_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  appId = request.args.get('appId', '')
  appName = request.args.get('appName', '')

  applications = []
  user = EsthenosUser.objects.get(id=current_user.id)
  group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=group_id)

  if (appId is not None) and (appId != ''):
    applications = EsthenosOrgApplication.objects.filter(application_id=appId, group=group, status__gte=0)

  elif (appName is not None) and (appName != ''):
    applications = EsthenosOrgApplication.objects.filter(applicant_name=appName, group=group, status__gte=0)

  else:
    applications = EsthenosOrgApplication.objects.filter(group=group, status__gte=0)

  kwargs = locals()
  return render_template("apps/applications_list.html", **kwargs)


@organisation_views.route('/applications/center/<center_id>', methods=["GET"])
@login_required
def application_list_center(center_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  group = EsthenosOrgGroup.objects.get(organisation=user.organisation, location_name=center_id)
  applications = EsthenosOrgApplication.objects.filter(group=group, status__gte=0)

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

      application.primary_income = float(request.form.get("primary_income"))
      application.tertiary_income = float(request.form.get("tertiary_income"))
      application.secondary_income = float(request.form.get("secondary_income"))
      application.other_income = float(request.form.get("other_income"))
      application.total_income = application.primary_income \
                                 + application.secondary_income \
                                 + application.tertiary_income \
                                 + application.other_income

      application.food_expense = float(request.form.get("food_expense"))
      application.travel_expense = float(request.form.get("travel_expense"))
      application.medical_expense = float(request.form.get("medical_expense"))
      application.business_expense = float(request.form.get("business_expense"))
      application.educational_expense = float(request.form.get("educational_expense"))
      application.entertainment_expense = float(request.form.get("entertainment_expense"))
      application.other_expense = float(request.form.get("other_expense"))
      application.total_expenditure = application.food_expense \
                                 + application.travel_expense \
                                 + application.medical_expense \
                                 + application.business_expense \
                                 + application.educational_expense \
                                 + application.entertainment_expense \
                                 + application.other_expense

      application.other_outstanding_emi = float(request.form.get("other_outstanding_emi"))
      application.other_outstanding_chit = float(request.form.get("other_outstanding_chit"))
      application.other_outstanding_insurance = float(request.form.get("other_outstanding_insurance"))
      application.total_other_outstanding = application.other_outstanding_emi + \
                                            application.other_outstanding_chit + \
                                            application.other_outstanding_insurance

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
def scrutiny():
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  applications = EsthenosOrgApplication.objects.filter(status__gte=0)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_list.html", **kwargs)


@organisation_views.route('/scrutiny/group/<group_id>', methods=["GET"])
@login_required
def scrutiny_list_group(group_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=group_id)
  applications = EsthenosOrgApplication.objects.filter(group=group, status__gte=0)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_list.html", **kwargs)


@organisation_views.route('/scrutiny/center/<group_location>', methods=["GET"])
@login_required
def scrutiny_list_center(group_location):
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  group = EsthenosOrgGroup.objects.get(organisation=user.organisation, location_name=group_location)
  applications = EsthenosOrgApplication.objects.filter(group=group, status__gte=0)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_list.html", **kwargs)


@organisation_views.route('/scrutiny/application/<app_id>', methods=["GET"])
@login_required
def scrutiny_application(app_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  application = EsthenosOrgApplication.objects.get(application_id=app_id)

  kwargs = locals()
  return render_template("scrutiny/scrutiny_details.html", **kwargs)
