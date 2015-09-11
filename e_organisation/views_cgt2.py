from views_base import *


@organisation_views.route('/check_cgt2', methods=["GET"])
@login_required
@feature_enable("questions_cgt2")
def cgt2_list():
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org  = user.organisation

    pending = EsthenosOrgGroupCGT2Session.objects(
      Q(organisation=org) & Q(state="none")
    )
    finalized = EsthenosOrgGroupCGT2Session.objects(
      Q(organisation=org) & (Q(state="pass") | Q(state="fail"))
    )

    groupId = request.args.get('groupId', '')
    groupName = request.args.get('groupName', '')

    if (groupId is not None) and (groupId != ''):
      groups = EsthenosOrgGroup.objects.filter(organisation=org, group_id=groupId)

    elif (groupName is not None) and (groupName != ''):
      groups = EsthenosOrgGroup.objects.filter(organisation=org, group_name=groupName)

    else:
      groups = EsthenosOrgGroup.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("cgt2/cgt2_group_list.html", **kwargs)


@organisation_views.route('/check_cgt2/group/<group_id>/status', methods=["POST"])
@login_required
@feature_enable("questions_cgt2")
def cgt2_group_status(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org  = user.organisation

    group = EsthenosOrgGroup.objects.get(organisation=org, group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group, status__gte=220)

    reqstatus = request.form.get("status")

    qsession = EsthenosOrgGroupCGT2Session.objects.get(group=group, organisation=org)
    qsession.state = "pass" if reqstatus == "true" else "fail"
    qsession.save()

    for app in applications:
        status = EsthenosOrgApplicationStatus(
            status=EsthenosOrgApplicationStatusType.objects.filter(status_code=220)[0],
            updated_on=datetime.datetime.now()
        )
        status.save()
        app.timeline.append(status)

        if reqstatus == "true":
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0]
            app.current_status_updated = datetime.datetime.now()
            app.status = 250

        else:
            app.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=240)[0]
            app.current_status_updated = datetime.datetime.now()
            app.status = 240

        app.save()

    return redirect("/check_cgt2")


@organisation_views.route('/check_cgt2/group/<group_id>/questions', methods=["GET","POST"])
@login_required
@feature_enable("questions_cgt2")
def cgt2_questions(group_id):
    if not session['role'].startswith("ORG_"):
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation
    if request.method == "GET":
        group = EsthenosOrgGroup.objects.get(organisation=org, group_id=group_id)
        questions = EsthenosOrgCGT2TemplateQuestion.objects.filter(organisation=org)

        kwargs = locals()
        return render_template("cgt2/cgt2_group_questions.html", **kwargs)

    elif request.method == "POST":
        i = 0
        total_score = 0.0
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation, group_id=group_id)
        qsession, status = EsthenosOrgGroupCGT2Session.objects.get_or_create(group=group, organisation=org)
        question_dict = dict()

        for v in request.form:
            i = i + 1
            (k, v) = (v, request.form[v])
            if k.startswith("rating"):
                key = k.split("rating")[1]
                question_dict[key] = str(v)
                total_score = total_score + int(v)

        qsession.questions = question_dict
        qsession.score = float(total_score/i)
        qsession.save()

        kwargs = locals()
        return redirect("/check_cgt2")
