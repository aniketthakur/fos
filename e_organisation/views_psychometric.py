from views_base import *


@organisation_views.route('/group/status/psychometric', methods=["PUT"])
@login_required
@feature_enable("questions_psychometric")
def group_psychometric():
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
        print app.application_id
        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=250)[0],updated_on=datetime.datetime.now())
        status.save()
        app.timeline.append(status)
        print reqstatus
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
    return Response(response=content,
        status=200,\
        mimetype="application/json")


