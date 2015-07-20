from views import *


@organisation_views.route('/users', methods=["GET"])
@login_required
def all_users():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    employees = EsthenosUser.objects.filter(organisation=user.organisation)
    kwargs = locals()
    return render_template("org_employees.html", **kwargs)


@organisation_views.route('/users/add', methods=["GET","POST"])
@login_required
def admin_organisation_add_emp():
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)

    if request.method == "POST":
        org_emp = AddOrganizationEmployeeForm(request.form)
        form = org_emp
        form.save(user.organisation.id)

        if form.validate():
            form.save(user.organisation.id)
            return redirect("/users")

        else:
            flash_errors(form)
            org = EsthenosOrg.objects.get(id=user.organisation.id)
            kwargs = locals()
            return render_template("org_add_emp.html", **kwargs)

    else:
        org = EsthenosOrg.objects.get(id=user.organisation.id)
        branches = EsthenosOrgBranch.objects.filter(organisation=org)
        kwargs = locals()
        return render_template("org_add_emp.html", **kwargs)


@organisation_views.route('/users/find', methods=["GET"])
@login_required
def search_user():
    query_param = request.args.get('q')
    users = EsthenosUser.objects(
      Q(name__contains=query_param)
      | Q(first_name__contains=query_param)
      | Q(last_name__contains=query_param)
      | Q(email__contains=query_param)
    ).only("name","email","id")

    user_dict = list()
    for result in users:
        if str(result.id) != str(current_user.id):
            user = {
              "id": str(result.id),
              "name": result.name,
              "email": result.email,
            }
            user_dict.append(user)

    return Response('{"users":'+json.dumps(user_dict)+'}', content_type="application/json", mimetype='application/json')

