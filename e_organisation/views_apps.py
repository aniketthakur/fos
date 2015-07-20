from views_base import *


@organisation_views.route('/applications', methods=["GET"])
@login_required
def applications():
  if not session['role'].startswith("ORG_"):
    abort(403)
  username = current_user.name
  c_user = current_user
  # center_id = request.args.get("center")
  branch_name = request.args.get("branch")
  #    print  center_id," ",group_id
  #    center = None
  #    if center_id is not None and center_id != '':
  #        center = EsthenosOrgCenter.objects.get(center_id=center_id)
  #        print center.center_name
  #    else:
  #        group_id = ''
  user = EsthenosUser.objects.get(id=c_user.id)
  branch = None
  print branch_name
  if branch_name is not None and branch_name != '':
    branch = EsthenosOrgBranch.objects.get(organisation=user.organisation, branch_name=branch_name.strip(" "))
    print branch.branch_name
  else:
    center_id = ''
  print  "filter " + branch.branch_name

  applications = None
  #    if center != None:
  #        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=11)
  #    el
  if branch != None:
    print  "filter " + branch.branch_name
    applications = EsthenosOrgApplication.objects.filter(branch=branch, status__gte=110)

  else:
    applications = EsthenosOrgApplication.objects.filter(status__gte=0)

  kwargs = locals()
  return render_template("applications_list.html", **kwargs)


@organisation_views.route('/applications_list', methods=["GET"])
@login_required
def application_list():
  if not session['role'].startswith("ORG_"):
    abort(403)
  username = current_user.name
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)
  # applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=110)
  # applications = EsthenosOrgApplication.objects.filter(status__gte=110)
  kwargs = locals()
  return render_template("applications_list.html", **kwargs)


@organisation_views.route('/application_status', methods=["GET"])
@login_required
def application_status():
  if not session['role'].startswith("ORG_"):
    abort(403)
  username = current_user.name
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)
  org = user.organisation
  centers = EsthenosOrgCenter.objects.filter(organisation=org)
  # groups = EsthenosOrgGroup.objects.filter(organisation=org)
  # regions = EsthenosOrgRegion.objects.filter(organisation=org)
  branchs = EsthenosOrgBranch.objects.filter(organisation=org)
  users = EsthenosUser.objects.filter(organisation=org)
  kwargs = locals()
  return render_template("centers_n_groups.html", **kwargs)


@organisation_views.route('/application/<app_id>/cashflow', methods=["GET"])
@login_required
def admin_application_cashflow(app_id):
  username = current_user.name
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)

  applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation, application_id=app_id)
  if len(applications) == 0:
    redirect("/application_status")

  kwargs = locals()
  app_urls = list()
  application = applications[0]
  return render_template("org_cf.html", **kwargs)


@organisation_views.route('/application/<app_id>/cashflow', methods=["POST"])
@login_required
def cashflow_statusupdate(app_id):
  username = current_user.name
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)
  try:
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
        return redirect("/application/" + new_id + "/cashflow")
  except Exception as e:
    print e.message
  return redirect("/application/" + app_id + "/cashflow")


@organisation_views.route('/application/<app_id>/track', methods=["GET"])
@login_required
def applications_track(app_id):
  if not session['role'].startswith("ORG_"):
    abort(403)
  username = current_user.name
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)
  application = EsthenosOrgApplication.objects.get(organisation=user.organisation, application_id=app_id)
  # print application.timeline
  kwargs = locals()
  return render_template("application_tracking.html", **kwargs)


@organisation_views.route('/organisation/<org_id>/application/<app_id>', methods=["GET"])
@login_required
def client_application_id(org_id, app_id):
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)
  print user.roles[0]
  username = current_user.name
  c_user = current_user
  user = EsthenosUser.objects.get(id=c_user.id)
  app_urls = list()
  try:
    applications = EsthenosOrgApplication.objects.filter(application_id=app_id)
  except Exception as e:
    print e.message

  if len(applications) == 0:
    redirect("/reports")

  application = applications[0]
  for kyc_id in application.tag.app_file_pixuate_id:
    app_urls.append(get_url_with_id(kyc_id))

  kyc_urls = list()
  kyc_ids = list()
  for kyc_id_key in application.tag.kyc_file_pixuate_id.keys():
    kyc_id = application.tag.kyc_file_pixuate_id[kyc_id_key]
    kyc_ids.append(kyc_id)
    kyc_urls.append(get_url_with_id(kyc_id))

  gkyc_urls = list()
  gkyc_ids = list()
  for gkyc_id_key in application.tag.gkyc_file_pixuate_id.keys():
    gkyc_id = application.tag.gkyc_file_pixuate_id[gkyc_id_key]
    gkyc_ids.append(gkyc_id)
    gkyc_urls.append(get_url_with_id(gkyc_id))

  today = datetime.datetime.today()
  disbursement_date = datetime.datetime.today() + timedelta(days=1)
  disbursement_date_str = disbursement_date.strftime('%d/%m/%Y')
  products = EsthenosOrgProduct.objects.filter(organisation=application.owner.organisation)

  kwargs = locals()
  return render_template("client_application_manual_DE.html", **kwargs)
