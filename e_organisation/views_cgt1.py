from views_base import *


@organisation_views.route('/center/status/cgt1', methods=["PUT"])
@login_required
def center_cgt1():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    data = json.loads(request.json)
    center_id = data['center_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    center = EsthenosOrgCenter.objects.get(organisation=user.organisation,center_id=center_id)
    applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=190)
    for app in applications:
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=190)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)

        if reqstatus ==  "true":
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 220
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=210)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 210
        app.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/group/status/cgt1', methods=["PUT"])
@login_required
def group_cgt1():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=190)

    for app in applications:
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=190)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)

        if reqstatus ==  "true":
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 220
        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=210)[0]
            app.current_status_updated  = datetime.datetime.now()
            app.status = 210
        app.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


@organisation_views.route('/check_cgt1', methods=["GET"])
@login_required
def check_cgt1():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org  = user.organisation
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    cgt1_sessions = EsthenosOrgGroupCGT1Session.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("cgt1/cgt1_group_list.html", **kwargs)


@organisation_views.route('/cgt1_question', methods=["GET","POST"])
@login_required
def cgt1_question():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org=user.organisation
    if request.method == "GET":
        group_id = request.args.get("group_id")
        questions = EsthenosOrgCGT1TemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        kwargs = locals()
        return render_template("grt_group_questions.html", **kwargs)

    elif request.method == "POST":
        i = 0
        total_score= 0.0
        group_id = request.args.get("group_id")
        questions = EsthenosOrgCGT1TemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        grt_session,status = EsthenosOrgGroupCGT1Session.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i+1
            (k,v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score+ int(v)

        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_cgt1")


@organisation_views.route('/check_cgt1/group/<group_id>', methods=["GET"])
@login_required
def check_cgt1_applicant(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)

    applications = None
    if group is not None:
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=190)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=190)

    kwargs = locals()
    return render_template("cgt1/cgt1_group_detail.html", **kwargs)
