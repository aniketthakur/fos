from views_base import *


@organisation_views.route('/telecalling', methods=["GET"])
@login_required
def telecalling():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org  = user.organisation
    centers = EsthenosOrgCenter.objects.filter(organisation=org)
    groups = EsthenosOrgGroup.objects.filter(organisation=org)
    call_sessions = EsthenosOrgIndivijualTeleCallingSession.objects.filter(organisation=org)
    kwargs = locals()
    return render_template("centers_n_groups_tc.html", **kwargs)


@organisation_views.route('/check_tele_applicant', methods=["GET"])
@login_required
def check_tele_applicant():
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
#        applications = EsthenosOrgApplication.objects.filter(center=center,status__gte=11)
#    el
    if group != None:
        print  "filter "+ group.group_name
        applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=272)
    else:
        applications = EsthenosOrgApplication.objects.filter(status__gte=272)
    kwargs = locals()
    return render_template("update_tele_indivijual.html", **kwargs)


@organisation_views.route('/check_tele_applicant_questions', methods=["GET","POST"])
@login_required
def check_tele_applicant_questions():
    if not session['role'].startswith("ORG_"):
        abort(403)
    username = current_user.name
    c_user = current_user
    center_id = request.args.get("center")
    group_id = request.args.get("group")
    print  center_id," ",group_id
    center = None
    if center_id is not None and center_id != '':
        center = EsthenosOrgCenter.objects.get(center_id=center_id)
        print center.center_name

    user = EsthenosUser.objects.get(id=c_user.id)
    group = None
    print  group_id
    if group_id is not None :
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
        print group.group_name


    app_id = request.args.get("app_id")

    if request.method == "GET":
        print app_id
        questions = EsthenosOrgTeleCallingTemplateQuestion.objects.all()

        kwargs = locals()
        return render_template("update_indivijual_tele_questions.html", **kwargs)
    if request.method == "POST":
        print request.form
        print  group
        i = 0
        total_score= 0.0
        questions = EsthenosOrgTeleCallingTemplateQuestion.objects.filter(organisation = user.organisation)
        application = EsthenosOrgApplication.objects.get(application_id = app_id)
        tele_session,status = EsthenosOrgIndivijualTeleCallingSession.objects.get_or_create(application=application,group=group,organisation=user.organisation)
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
        tele_session.questions = question_dict
        tele_session.score = float(total_score/i)
        tele_session.save()
        kwargs = locals()
        return redirect("/check_tele_applicant?group="+group_id)


