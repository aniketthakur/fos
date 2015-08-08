from views_base import *


@organisation_views.route('/applications', methods=["GET"])
@login_required
def applications():
  if not session['role'].startswith("ORG_"):
    abort(403)

  group = None
  user = EsthenosUser.objects.get(id=current_user.id)
  applications = EsthenosOrgApplication.objects.filter(status__gte=0)

  kwargs = locals()
  return render_template("apps/applications_list.html", **kwargs)


@organisation_views.route('/applications/group/<group_id>', methods=["GET"])
@login_required
def application_list(group_id):
  if not session['role'].startswith("ORG_"):
    abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=group_id)
  applications = EsthenosOrgApplication.objects.filter(group=group, status__gte=0)

  kwargs = locals()
  return render_template("apps/applications_list.html", **kwargs)


@organisation_views.route('/application_status', methods=["GET"])
@login_required
def application_status():
  if not session['role'].startswith("ORG_"):
      abort(403)

  user = EsthenosUser.objects.get(id=current_user.id)
  org  = user.organisation
  groups = EsthenosOrgGroup.objects.filter(organisation=org)
  centers = EsthenosOrgCenter.objects.filter(organisation=org)

  kwargs = locals()
  return render_template("apps/applications_centers_n_groups.html", **kwargs)


@organisation_views.route('/application/<app_id>/cashflow', methods=["GET"])
@login_required
def admin_application_cashflow(app_id):

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

      if request.form.get("status") == "true":
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=170)[0]
        application.current_status_updated = datetime.datetime.now()
        application.status = 170

      else:
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=180)[0]
        application.current_status_updated = datetime.datetime.now()
        application.status = 170

      application.save()
      new_num = int(app_id[-6:]) + 1
      new_id = app_id[0:len(app_id) - 6] + "{0:06d}".format(new_num)
      new_apps = EsthenosOrgApplication.objects.filter(application_id=new_id)

      if len(new_apps) > 0:
        return redirect("/application/%s/cashflow" % new_id)

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


@organisation_views.route('/application/<app_id>/details', methods=["GET"])
@login_required
def client_application_id(app_id):

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
