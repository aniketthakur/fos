from views import *


@organisation_views.route('/users', methods=["GET"])
@login_required
def all_users():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    try:
        employees = EsthenosUser.objects.filter(organisation=user.organisation)
    except Exception as e:
        print e.message
    kwargs = locals()
    return render_template("org_employees.html", **kwargs)


@organisation_views.route('/users/add', methods=["GET","POST"])
@login_required
def admin_organisation_add_emp():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    print "reached here"
    if request.method == "POST":
        print request.form
        org_emp  = AddOrganizationEmployeeForm(request.form)
        form=org_emp
        print user.organisation.id
        form.save(user.organisation.id)
        if (form.validate()):
            form.save(user.organisation.id)
            print "formValidated"
            return redirect("/users")
        else:
            print "some Error"
            flash_errors(form)
            print form.errors
            org = EsthenosOrg.objects.get(id=user.organisation.id)
            kwargs = locals()
            return render_template("org_add_emp.html", **kwargs)
    else:

        org = EsthenosOrg.objects.get(id=user.organisation.id)
        branches = EsthenosOrgBranch.objects.filter(organisation = org)
        kwargs = locals()
        return render_template("org_add_emp.html", **kwargs)


@organisation_views.route('/find_users', methods=["GET"])
@login_required
def search_user():
    query_param = request.args.get('q')
    print query_param
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    users = EsthenosUser.objects(Q(name__contains=query_param) |Q(first_name__contains=query_param) | Q(last_name__contains=query_param) |Q(email__contains=query_param) ).only("name","email","id")
    user_dict = list()
    for result in users:
        if str(result.id) != str(c_user.id):
            obj = dict()
            obj['name'] = result.name
            obj['email'] = result.email
            obj['id'] = str(result.id)
            user_dict.append(obj)

    return Response('{"users":'+json.dumps(user_dict)+'}', content_type="application/json", mimetype='application/json')

