from views_base import *


@organisation_views.route('/group/status/psychometric', methods=["PUT"])
@login_required
@feature_enable("questions_psychometric")
def group_psychometric():
    if not session['role'].startswith("ORG_"):
        abort(403)

    data = json.loads(request.json)
    group_id = data['group_id']
    reqstatus = data['status']

    user = EsthenosUser.objects.get(id=current_user.id)
    group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_id=group_id)
    applications = EsthenosOrgApplication.objects.filter(group=group,status__gte=250)

    for app in applications:
        status_code = 272 if reqstatus == "true" else 270
        app.update_statue(250)
        app.update_statue(status_code)
        app.save()

    content = {'response': 'OK'}
    return Response(response=content, status=200, mimetype="application/json")


