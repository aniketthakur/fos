from views_base import *


@organisation_views.route('/center/status/cgt2', methods=["PUT"])
@login_required
def center_cgt2():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    center_id = data['center_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    center = EsthenosOrgCenter.objects.get(organisation=user.organisation,center_id=center_id)
    applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=220)

    for app in applications:
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)

        if reqstatus ==  "true":
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 250
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=240)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 240
        app.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/group/status/cgt2', methods=["PUT"])
@login_required
def group_cgt2():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=220)

    for app in applications:
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)

        if reqstatus ==  "true":
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 250
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=240)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 240
        app.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/check_cgt2', methods=["GET"])
@login_required
def check_cgt2():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org  = user.organisation
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    cgt2_sessions = EsthenosOrgGroupCGT2Session.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("cgt2/cgt2_group_list.html", **kwargs)


@organisation_views.route('/check_cgt2/group/<group_id>/questions', methods=["GET","POST"])
@login_required
def cgt2_question(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation
    if request.method == "GET":
        questions = EsthenosOrgCGT2TemplateQuestion.objects.filter(organisation=org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.filter(group_id=group_id)[0]
        kwargs = locals()
        return render_template("cgt2/cgt2_group_questions.html", **kwargs)

    elif request.method == "POST":
        i = 0
        total_score= 0.0
        questions = EsthenosOrgCGT2TemplateQuestion.objects.filter(organisation=org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        grt_session, status = EsthenosOrgGroupCGT2Session.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i + 1
            (k, v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score + int(v)

        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_cgt2")


@organisation_views.route('/check_cgt2/group/<group_id>', methods=["GET"])
@login_required
def check_cgt2_applicant(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)

    applications = None
    if group is not None:
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=220)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=220)

    kwargs = locals()
    return render_template("cgt2/cgt2_group_detail.html", **kwargs)
