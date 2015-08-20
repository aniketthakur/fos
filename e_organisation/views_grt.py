from views_base import *


@organisation_views.route('/check_grt', methods=["GET"])
@login_required
@feature_enable("questions_grt")
def grt_list():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org  = user.organisation
    grt_sessions = EsthenosOrgGroupGRTSession.objects.filter(organisation=org)

    groupId = request.args.get('groupId', '')
    groupName = request.args.get('groupName', '')

    if (groupId is not None) and (groupId != ''):
      groups = EsthenosOrgGroup.objects.filter(organisation=org, group_id=groupId)

    elif (groupName is not None) and (groupName != ''):
      groups = EsthenosOrgGroup.objects.filter(organisation=org, group_name=groupName)

    else:
      groups = EsthenosOrgGroup.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("grt/grt_group_list.html", **kwargs)


@organisation_views.route('/group/status/grt', methods=["PUT"])
@login_required
@feature_enable("questions_grt")
def grt_group_status():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=250)

    for app in applications:
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)

        if reqstatus ==  "true":
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=272)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 272
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=270)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 270
        app.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/check_grt/group/<group_id>/questions', methods=["GET","POST"])
@login_required
@feature_enable("questions_grt")
def grt_questions(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation

    if request.method == "GET":
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        kwargs = locals()
        return render_template("grt/grt_group_questions.html", **kwargs)

    elif request.method == "POST":
        i = 0
        total_score = 0.0
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation=org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        grt_session, status = EsthenosOrgGroupGRTSession.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i + 1
            (k, v) = (v,request.form[v])
            if k.startswith("rating"):
                key = k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score + int(v)

        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_grt")


@organisation_views.route('/check_grt/group/<group_id>/download/<disbursement_date>', methods=["GET"])
@login_required
@feature_enable("questions_grt")
def grt_downloads(group_id, disbursement_date):
    if not session['role'].startswith("ORG_"):
        abort(403)

    tmp_files = list()
    user = EsthenosUser.objects.get(id=current_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=group_id)

    dir = "%s/" % tempfile.mkdtemp(prefix='pdf_')
    tfa = dir + group_id + "_agreement.pdf"

    #TODO remove localhost
    downloadFile("http://localhost:8080/internal/pdf_la/%s/%s" % (group_id, disbursement_date), tfa)
    tmp_files.append(tfa)

    tf = "%s/%s" % (tempfile.mkdtemp(prefix='zip_'), group_id)
    zip_custom(dir, tf)
    filehandle = open(tf + ".zip", 'rb')

    data = StringIO.StringIO(filehandle.read())
    output = make_response(data.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=%s.zip" % group_id
    output.headers["Content-type"] = "application/zip"
    return output


@organisation_views.route('/check_grt/group/<group_id>', methods=["GET"])
@login_required
@feature_enable("questions_grt")
def grt_group_list(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)

    applications = None
    if group is not None:
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=250)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=250)

    kwargs = locals()
    return render_template("grt/grt_group_detail.html", **kwargs)
