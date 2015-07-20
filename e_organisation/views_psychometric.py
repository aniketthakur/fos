from views_base import *


@organisation_views.route('/api/organisation/products', methods=["GET"])
@login_or_key_required
def org_products():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisations = EsthenosOrg.objects.all()
    products = EsthenosOrgProduct.objects.all()
    content = list()
    for product in products:
        pr = dict()
        pr["product_name"] = product["product_name"]
        pr["loan_amount"] = product["loan_amount"]
        pr["life_insurance"] = product["life_insurance"]
        pr["eligible_cycle"] = product["eligible_cycle"]
        pr["number_installments"] = product["number_installments"]
        pr["emi"] = product["emi"]
        pr["last_emi"] = product["last_emi"]
        pr["processing_fee"] = product["processing_fee"]
        pr["total_processing_fees"] = product["total_processing_fees"]
        pr["interest_rate"] = product["interest_rate"]
        pr["insurance_period"] = product["insurance_period"]
        pr["emi_repayment"] = product["emi_repayment"]
        content.append(pr)
    kwargs = locals()
    return Response(json.dumps({'products':content}), content_type="application/json", mimetype='application/json')


@organisation_views.route('/group/status/psychometric', methods=["PUT"])
@login_required
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


