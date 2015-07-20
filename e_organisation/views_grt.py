from views_base import *


@organisation_views.route('/center/status/grt', methods=["PUT"])
@login_required
def center_grt():
    if not session['role'].startswith("ORG_"):
        abort(403)
    c_user = current_user
    data = json.loads(request.json)
    center_id = data['center_id']
    reqstatus = data['status']
    user = EsthenosUser.objects.get(id=c_user.id)
    center = EsthenosOrgCenter.objects.get(organisation=user.organisation,center_id=center_id)
    applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=250)

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


@organisation_views.route('/group/status/grt', methods=["PUT"])
@login_required
def group_grt():
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


@organisation_views.route('/check_grt', methods=["GET"])
@login_required
def check_grt():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    grt_sessions = EsthenosOrgGroupGRTSession.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("centers_n_groups_grt.html", **kwargs)


@organisation_views.route('/grt_question', methods=["GET","POST"])
@login_required
def grt_question():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org=user.organisation
    if request.method == "GET":
        group_id = request.args.get("group_id")
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        kwargs = locals()
        return render_template("centers_n_groups_grt_questions.html", **kwargs)
    elif request.method == "POST":
        print request.form
        i = 0
        total_score= 0.0
        group_id = request.args.get("group_id")
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation = org)
        centers = EsthenosOrgCenter.objects.filter(organisation=org)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)

        grt_session,status = EsthenosOrgGroupGRTSession.objects.get_or_create(group=group,organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i+1
            (k,v) = (v,request.form[v])
            if k.startswith("rating"):
                key =  k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score+ int(v)
        print total_score/i
        print questions
        grt_session.questions = question_dict
        grt_session.score = float(total_score/i)
        grt_session.save()
        kwargs = locals()
        return redirect("/check_grt")


@organisation_views.route('/check_grt_applicant', methods=["GET"])
@login_required
def check_grt_applicant():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    #center_id = request.args.get("center")
    group_id = request.args.get("group")
    #    print  center_id," ",group_id
    #    center = None
    #    if center_id is not None and center_id != '':
    #        center = EsthenosOrgCenter.objects.get(center_id=center_id)
    #        print center.center_name
    #    else:
    #        group_id = ''
    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print group_id
    if group_id is not None and group_id != '':
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id.strip(" "))
        print group.group_name
    else:
        center_id = ''
    print  "filter "+ group.group_name
    applications = None
    #    if center != None:
    #        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=250)
    #    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=250)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=250)
    kwargs = locals()
    return render_template("update_grt_indivijual.html", **kwargs)
