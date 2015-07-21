import os
import sys, traceback
import json, psutil, urlparse

import boto, pdfkit
from mongoengine import Q
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from flask import Blueprint, redirect, flash, current_app
from flask import render_template, session, request, Response, jsonify, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required, confirm_login
from flask_sauth.forms import LoginForm
from flask_sauth.views import flash_errors

from e_admin.forms import *
from e_admin.models import *
from e_tokens.utils import login_or_key_required
from e_pixuate.pixuate import *
from e_organisation.forms import *
from e_organisation.models import *

from blinker import signal
from esthenos import mainapp


conn = boto.connect_ses(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))

signal_user_registered = signal('user-registered')


admin_views = Blueprint('admin_views', __name__, template_folder='templates')


@admin_views.route('/admin/dashboard', methods=["GET"])
@login_required
def admin_dashboard():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_dashboard.html", **kwargs)


@admin_views.route('/admin/settings', methods=["GET"])
@login_required
def admin_settings():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    settings = EsthenosSettings.objects.all()[0]
    kwargs = locals()
    return render_template("admin_settings.html", **kwargs)


@admin_views.route('/admin/organisation/products', methods=["GET"])
@login_required
def admin_org_add_product():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    settings = EsthenosSettings.objects.all()[0]
    kwargs = locals()
    return render_template("admin_org_add_product.html", **kwargs)


@admin_views.route('/admin/add_org', methods=["GET","POST"] )
@login_required
def admin_add_org():
    if session['role'] != "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    if request.method == "POST":
        org_form = AddOrganisationForm( request.form)
        form = org_form

        if form.validate():
            org = form.save()
            settings = EsthenosSettings.objects.all()[0]
            settings.update(inc__organisations_count=1)
            return redirect("/admin/update_org/"+str(org.id))

        else:
            flash_errors(org_form)
            user = EsthenosUser.objects.get(id=current_user.id)
            kwargs = {"login_form": org_form}
            return render_template("admin_add_org.html", **kwargs)

    else:
        kwargs = locals()
        return render_template("admin_add_org.html", **kwargs)


@admin_views.route('/admin/update_org/<org_id>', methods=["GET"] )
@login_required
def admin_update_org(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org = EsthenosOrg.objects.get(id=org_id)
    states = EsthenosOrgState.objects.filter(organisation=org)
    regions = EsthenosOrgRegion.objects.filter(organisation=org)
    areas = EsthenosOrgArea.objects.filter(organisation=org)

    print regions
    kwargs = locals()
    return render_template("admin_add_org_details.html", **kwargs)


@admin_views.route('/admin/update_org/<org_id>/group', methods=["GET","POST"] )
@login_required
def admin_update_org_group(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org = EsthenosOrg.objects.get(id=org_id)
    if request.method == "GET":
        states = EsthenosOrgState.objects.filter(organisation=org)
        regions = EsthenosOrgRegion.objects.filter(organisation=org)
        areas = EsthenosOrgArea.objects.filter(organisation=org)
        branches = EsthenosOrgBranch.objects.filter(organisation=org)
        users = EsthenosUser.objects.filter(organisation=org)
        #groups = EsthenosOrgGroup.objects.filter(organisation=org)
        #emp = AddOrganizationEmployeeForm.objects.filtee(organisation=org)
        print branches
        kwargs = locals()
        return render_template("admin_add_org_group.html", **kwargs)
    if request.method == "POST":
        print request.form
        print "hello error"
        data =  request.form.get('org_data').split(",")
        print "hello"
        loc_name = request.form.get('location_name')
        #branch_name = request.form.get('branch_name')
        #group_name = request.form.get('group_name')
        user_name=request.form.get('user_name')
        #emp_name = request.form.get('emp_name')
        #unique_group_id = org.name.upper()[0:2]+"G"+"{0:06d}".format(org.group_count)
        unique_c_user_id = org.name.upper().format(org.user_count)
        branch = EsthenosOrgBranch.objects.get(id=data[3])
        user,status = EsthenosUser.objects.get_or_create(organisation=org,user_name=user_name)
        if status:
            user.location_name=loc_name
            user.branch=branch
            #group.group_id = unique_group_id
            user.save()
            EsthenosOrg.objects.get(id = org.id).update(inc__user_count=1)
        return redirect("/admin/organisations")


@admin_views.route('/admin/update_org/<org_id>/update_regions', methods=["POST"] )
@login_required
def admin_update_org_regions(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org = EsthenosOrg.objects.get(id=org_id)

    if request.method == "POST":
        print request.form
        print request.form.get('org_regions')
        for region in request.form.get('org_regions').split(","):
            state = EsthenosOrgState.objects.get(id=request.form.get('org_state'))
            reg = EsthenosOrgRegion.objects.create(region_name=region,organisation=org,state=state)
            reg.save()

        """
        my_branches = []
        for branch in self.branches.data.split(","):
            br = EsthenosOrgBranch.objects.create(branch_name=branch,organisation=org)
            br.save()
            my_branches.append(br)
        org.branches =my_branches

        """
        return redirect("/admin/organisations")

    else:
        states = EsthenosOrgState.objects.filter(organisation=org)
        regions = EsthenosOrgRegion.objects.filter(organisation=org)
        print regions
        kwargs = locals()
        return render_template("admin_add_org_details.html", **kwargs)


@admin_views.route('/admin/update_org/<org_id>/update_states', methods=["POST"] )
@login_required
def admin_update_states(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org = EsthenosOrg.objects.get(id=org_id)

    if request.method == "POST":
        print request.form
        print request.form.get('org_states')
        for state in request.form.get('org_states').split(","):
            st,status = EsthenosOrgState.objects.get_or_create(state_name=state,organisation=org)
            org.states.append(st)

        org.save()
        """
        my_branches = []
        for branch in self.branches.data.split(","):
            br = EsthenosOrgBranch.objects.create(branch_name=branch,organisation=org)
            br.save()
            my_branches.append(br)
        org.branches =my_branches

        """
        return redirect("/admin/organisations")

    else:
        states = EsthenosOrgState.objects.filter(organisation=org)
        regions = EsthenosOrgRegion.objects.filter(organisation=org)
        print regions
        kwargs = locals()
        return render_template("admin_add_org_details.html", **kwargs)


@admin_views.route('/admin/update_org/<org_id>/update_areas', methods=["POST"] )
@login_required
def admin_update_org_update_areas(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org = EsthenosOrg.objects.get(id=org_id)
    states = org.states
    if request.method == "POST":
        print request.form
        data =  request.form.get('org_data').split(",")
        for area in request.form.get('org_areas').split(","):
            state = EsthenosOrgState.objects.get(id=data[0])
            region = EsthenosOrgRegion.objects.get(id=data[1])
            area_obj = EsthenosOrgArea.objects.create(area_name=area,organisation=org,state=state,region=region)
            area_obj.save()
        return redirect("/admin/organisations")

    else:
        kwargs = locals()
        return render_template("admin_add_org_details.html", **kwargs)


@admin_views.route('/admin/update_org/<org_id>/update_branches', methods=["POST"] )
@login_required
def admin_update_org_update_branches(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org = EsthenosOrg.objects.get(id=org_id)
    if request.method == "POST":
        print request.form
        data =  request.form.get('org_data').split(",")
        brs = request.form.get('org_branch_data').split(",")
        print "Here...............", data,brs
        for branche in brs:
            state = EsthenosOrgState.objects.get(id=data[0])
            region = EsthenosOrgRegion.objects.get(id=data[1])
            area = EsthenosOrgArea.objects.get(id=data[2])
            br_obj = EsthenosOrgBranch.objects.create(branch_name=branche,area=area,organisation=org,state=state,region=region)
            br_obj.save()
        return redirect("/admin/organisations")

    else:
        kwargs = locals()
        return render_template("admin_add_org_details.html", **kwargs)


@admin_views.route('/admin/add_emp', methods=["GET","POST"])
@login_required
def admin_add_emp():
    if session['role'] != "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    if request.method == "POST":
        print "hello"
        org_form = AddEmployeeForm( request.form )
        form = org_form
        if form.validate():
            form.save()
            return redirect("/admin/employees")

        else:
            flash_errors(org_form)
            kwargs = {"login_form": org_form}
            return render_template("admin_add_emp.html", **kwargs)
    else:

        kwargs = locals()
        return render_template("admin_add_emp.html", **kwargs)


@admin_views.route('/admin/employees', methods=["GET"])
@login_required
def admin_employees():
    if session['role'] != "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    employees=EsthenosUser.objects.filter(roles__in=["EMP_EXECUTIVE", "EMP_MANAGER","EMP_VP"])
    kwargs = locals()
    return render_template("admin_employees.html", **kwargs)


@admin_views.route('/admin/organisations', methods=["GET"])
@login_required
def admin_organisations():
    if session['role'] != "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    organisations = EsthenosOrg.objects.all()
    kwargs = locals()
    return render_template("admin_organisation.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>', methods=["GET"])
@login_required
def admin_organisation_dashboard(org_id):
    if session['role'] != "ADMIN":
        abort(403)

    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)

    employees = []
    employees = EsthenosUser.objects.filter(organisation=organisation)

    products = []
    products = EsthenosOrgProduct.objects.filter(organisation=organisation)

    kwargs = locals()
    return render_template("admin_organisation_dashboard.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/settings/role/<role_type>', methods=["GET"])
@login_required
def admin_organisation_settings_role(org_id,role_type):
    if session['role'] != "ADMIN":
        abort(403)

    username = current_user.name
    print role_type
    org = EsthenosOrg.objects.get(id=org_id)
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    org_settings,status = EsthenosOrgRoleSettings.objects.get_or_create(organisation = user.organisation,role=role_type)
    resp = dict()
    resp["access_dash"] = org_settings.access_dash
    resp["access_enroll_customer"]= org_settings.access_enroll_customer
    resp["access_cgt"]= org_settings.access_cgt
    resp["access_grt"]= org_settings.access_grt
    resp["access_disburse"]= org_settings.access_disburse
    resp["access_reports"]= org_settings.access_reports
    resp["access_maker"]= org_settings.access_maker
    resp["access_checker"]= org_settings.access_checker
    resp["noti_de_done"]= org_settings.noti_de_done
    resp["noti_cbc_done"]= org_settings.noti_cbc_done
    resp["noti_cfa_done"]= org_settings.noti_cfa_done
    resp["noti_dd_done"]= org_settings.noti_dd_done
    resp["noti_db_done"]= org_settings.noti_db_done
    resp["reports_all_data"]= org_settings.reports_all_data
    resp["reports_de_done"]= org_settings.reports_de_done
    resp["reports_cbc_done"]= org_settings.reports_cbc_done
    resp["reports_cfa_done"]= org_settings.reports_cfa_done
    resp["reports_dd_done"]= org_settings.reports_dd_done
    resp["reports_db_done"]= org_settings.reports_db_done

    return Response(response=json.dumps(resp),
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/organisation/<org_id>/settings/other', methods=["POST"])
@login_required
def admin_organisation_settings_rbi(org_id):
    if session['role'] != "ADMIN":
        abort(403)

    username = current_user.name

    org = EsthenosOrg.objects.get(id=org_id)
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    settings,status = EsthenosOrgSettings.objects.get_or_create(organisation=organisation)
    if request.method == "POST":
        print request.form
        settings.loan_cycle_1_org = float(request.form.get("loan_cycle_1_org"))
        settings.loan_cycle_1_plus_org = float(request.form.get("loan_cycle_1_plus_org"))
        settings.one_year_tenure_limit_org = float(request.form.get("one_year_tenure_limit_org"))
        settings.hh_annual_income_limit_rural_org = float(request.form.get("hh_annual_income_limit_rural_org"))
        settings.hh_annual_income_limit_urban_org = float(request.form.get("hh_annual_income_limit_urban_org"))
        settings.total_indebtness_org = float(request.form.get("total_indebtness_org"))
        settings.max_existing_loan_count_org = int(request.form.get("max_existing_loan_count_org"))
        settings.product_cycle_1_group_min = int(request.form.get("product_cycle_1_group_min"))
        settings.product_cycle_1_group_max = int(request.form.get("product_cycle_1_group_max"))
        settings.product_cycle_2_group_min = int(request.form.get("product_cycle_2_group_min"))
        settings.product_cycle_2_group_max = int(request.form.get("product_cycle_2_group_max"))
        settings.product_cycle_3_group_min = int(request.form.get("product_cycle_3_group_min"))
        settings.product_cycle_3_group_max = int(request.form.get("product_cycle_3_group_max"))
        settings.product_cycle_4_group_min = int(request.form.get("product_cycle_4_group_min"))
        settings.product_cycle_4_group_max = int(request.form.get("product_cycle_4_group_max"))
        settings.save()
        return redirect("/admin/organisation/"+org_id+"/settings")


@admin_views.route('/admin/organisation/<org_id>/settings', methods=["GET","POST"])
@login_required
def admin_organisation_settings(org_id):
    if session['role'] != "ADMIN":
        abort(403)

    username = current_user.name

    org = EsthenosOrg.objects.get(id=org_id)
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    settings,status = EsthenosOrgSettings.objects.get_or_create(organisation=organisation)
    if request.method == "POST":
        print request.form
        role = request.form.get("role")
        org_settings,status = EsthenosOrgRoleSettings.objects.get_or_create(organisation = user.organisation,role=role)
        org_settings.access_dash = request.form.get("access_dash")
        org_settings.access_enroll_customer = request.form.get("access_enroll_customer")
        org_settings.access_cgt = request.form.get("access_cgt")
        org_settings.access_grt = request.form.get("access_grt")
        org_settings.access_disburse = request.form.get("access_disburse")
        org_settings.access_reports = request.form.get("access_reports")
        org_settings.access_maker = request.form.get("access_maker")
        org_settings.access_checker = request.form.get("access_checker")
        org_settings.noti_de_done = request.form.get("noti_de_done")
        org_settings.noti_cbc_done = request.form.get("noti_cbc_done")
        org_settings.noti_cfa_done = request.form.get("noti_cfa_done")
        org_settings.noti_dd_done = request.form.get("noti_dd_done")
        org_settings.noti_db_done = request.form.get("noti_db_done")
        org_settings.reports_all_data = request.form.get("reports_all_data")
        org_settings.reports_de_done = request.form.get("reports_de_done")
        org_settings.reports_cbc_done = request.form.get("reports_cbc_done")
        org_settings.reports_cfa_done = request.form.get("reports_cfa_done")
        org_settings.reports_dd_done = request.form.get("reports_dd_done")
        org_settings.reports_db_done = request.form.get("reports_db_done")
        org_settings.save()
        kwargs = locals()
        return render_template("admin_org_settings.html", **kwargs)
    else :
        print settings.loan_cycle_1_org
        kwargs = locals()
        return render_template("admin_org_settings.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/add_emp', methods=["GET","POST"])
@login_required
def admin_organisation_add_emp(org_id):
    if session['role'] != "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)

    if request.method == "POST":
        org_emp = AddOrganizationEmployeeForm(request.form)
        form = org_emp
        form.save(org_id)

        if form.validate():
            form.save(org_id)
            return redirect("/admin/organisation/"+org_id)

        else:
            flash_errors(form)
            org = EsthenosOrg.objects.get(id=org_id)
            kwargs = locals()
            return render_template("admin_org_add_emp.html", **kwargs)

    else:
        org = EsthenosOrg.objects.get(id=org_id)
        branches = EsthenosOrgBranch.objects.filter(organisation = org)
        kwargs = locals()
        return render_template("admin_org_add_emp.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/add_product',methods=['GET','POST'])
@login_required
def admin_organisation_product(org_id):
    if session['role'] == 'ADMIN':
        org = EsthenosOrg.objects.get(id=org_id)
        user = current_user
        kwargs = locals()

        if request.method == "GET":
            return render_template("admin_org_add_product.html", **kwargs)

        else:
            product = AddOrganisationProductForm(request.form)
            org_product = product
#            org_product.save(org_id)

            if org_product.validate():
                org_product.save(org_id)
                org = EsthenosOrg.objects.get(id=org_id)
                user = EsthenosUser.objects.get(id=current_user.id)
                organisation = EsthenosOrg.objects.get(id=org_id)
                kwargs = locals()
                return redirect("/admin/organisation/"+org_id)

            else:
                kwargs = locals()
                return redirect("/admin/organisation/"+org_id+"/add_product")

    else:
        return abort(403)


@admin_views.route('/admin/organisation/<org_id>/grt_questions',methods=['GET','POST'])
@login_required
def grt_questions(org_id):
    if session['role']=='ADMIN':
        username=current_user.name
        user=current_user
        org=EsthenosOrg.objects.get(id=org_id)
        questions = EsthenosOrgGRTTemplateQuestion.objects.filter(organisation=org)
        kwargs = locals()
        if request.method=="GET":
            return render_template("admin_organisation_grt_questions.html", **kwargs)
        else:
            question=AddOrgGRTTemplateQuestionsForm(request.form)
            if(question.validate()):
                print "Product Details Validated,Saving the form"
                question.save()
                org = EsthenosOrg.objects.get(id=org_id)
                c_user = current_user
                user = EsthenosUser.objects.get(id=c_user.id)
                return render_template("admin_organisation_grt_questions.html", **kwargs)
            else:
                print "Validation Error"
                print flash_errors(question)
                kwargs = locals()
                return render_template("admin_organisation_grt_questions.html", **kwargs)
    else:
        return abort(403)


@admin_views.route('/admin/organisation/<org_id>/cgt1_questions',methods=['GET','POST'])
@login_required
def cgt1_questions(org_id):
    if session['role']=='ADMIN':
        username=current_user.name
        user=current_user
        org=EsthenosOrg.objects.get(id=org_id)
        questions = EsthenosOrgCGT1TemplateQuestion.objects.filter(organisation=org)
        kwargs = locals()
        if request.method=="GET":
            return render_template("admin_organisation_cgt1_questions.html", **kwargs)
        else:
            question=AddOrgCGT1TemplateQuestionsForm(request.form)
            if(question.validate()):
                print "Product Details Validated,Saving the form"
                question.save()
                org = EsthenosOrg.objects.get(id=org_id)
                c_user = current_user
                user = EsthenosUser.objects.get(id=c_user.id)
                return render_template("admin_organisation_cgt1_questions.html", **kwargs)
            else:
                print "Validation Error"
                print flash_errors(question)
                kwargs = locals()
                return render_template("admin_organisation_cgt1_questions.html", **kwargs)
    else:
        return abort(403)


@admin_views.route('/admin/organisation/<org_id>/cgt2_questions',methods=['GET','POST'])
@login_required
def cgt2_questions(org_id):
    if session['role']=='ADMIN':
        username=current_user.name
        user=current_user
        org=EsthenosOrg.objects.get(id=org_id)
        questions = EsthenosOrgCGT2TemplateQuestion.objects.filter(organisation=org)
        kwargs = locals()
        if request.method=="GET":
            return render_template("admin_organisation_cgt2_questions.html", **kwargs)
        else:
            question=AddOrgCGT2TemplateQuestionsForm(request.form)
            if(question.validate()):
                print "Product Details Validated,Saving the form"
                question.save()
                org = EsthenosOrg.objects.get(id=org_id)
                c_user = current_user
                user = EsthenosUser.objects.get(id=c_user.id)
                return render_template("admin_organisation_cgt2_questions.html", **kwargs)
            else:
                print "Validation Error"
                print flash_errors(question)
                kwargs = locals()
                return render_template("admin_organisation_cgt2_questions.html", **kwargs)
    else:
        return abort(403)


@admin_views.route('/admin/organisation/<org_id>/telecalling_questions',methods=['GET','POST'])
@login_required
def telecalling_questions(org_id):
    if session['role']=='ADMIN':
        username=current_user.name
        user=current_user
        org=EsthenosOrg.objects.get(id=org_id)
        questions = EsthenosOrgTeleCallingTemplateQuestion.objects.filter(organisation=org)
        kwargs = locals()
        if request.method=="GET":
            return render_template("admin_organisation_tele_questions.html", **kwargs)
        else:
            question=AddOrgTeleCallingTemplateQuestionsForm(request.form)
            if(question.validate()):
                print "Product Details Validated,Saving the form"
                question.save()
                org = EsthenosOrg.objects.get(id=org_id)
                c_user = current_user
                user = EsthenosUser.objects.get(id=c_user.id)
                return render_template("admin_organisation_tele_questions.html", **kwargs)
            else:
                print "Validation Error"
                print flash_errors(question)
                kwargs = locals()
                return render_template("admin_organisation_tele_questions.html", **kwargs)
    else:
        return abort(403)


@admin_views.route('/admin/organisation/<org_id>/psychometric_questions',methods=['GET','POST'])
@login_required
def psychometric_questions(org_id):
    if session['role']=='ADMIN':
        username=current_user.name
        user=current_user
        org=EsthenosOrg.objects.get(id=org_id)
        questions = EsthenosOrgPsychometricTemplateQuestion.objects.filter(organisation=org)
        kwargs = locals()
        if request.method=="GET":
            return render_template("admin_organisation_psychometric_questions.html", **kwargs)
        else:
            question=AddOrgPsychometricTemplateQuestionsForm(request.form)
            # answer=AddOrgPsychometricTemplateQuestionsForm(request.form)
            if(question.validate):
                print "Product Details Validated,Saving the form"
                question.save()
                print "save answer"
                # answer.save()
                print "not saved answer"
                org = EsthenosOrg.objects.get(id=org_id)
                c_user = current_user
                user = EsthenosUser.objects.get(id=c_user.id)
                return render_template("admin_organisation_psychometric_questions.html", **kwargs)
            else:
                print "Validation Error"
                print flash_errors(question)
                kwargs = locals()
                return render_template("admin_organisation_psychometric_questions.html", **kwargs)
    else:
        return abort(403)


@admin_views.route('/admin/reports', methods=["GET"])
@login_required
def admin_reports():
#    if session['role'] != "ADMIN":
#        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisations = EsthenosOrg.objects.all()
    tagged_applications = EsthenosOrgApplication.objects.all()
    kwargs = locals()
    return render_template("admin_reports.html", **kwargs)


@admin_views.route('/admin/reports/master/download', methods=["GET"])
@login_required
def admin_reports_download():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisations = EsthenosOrg.objects.all()
    tagged_applications = EsthenosOrgApplication.objects.all()
    kwargs = locals()
    return render_template("admin_reports.html", **kwargs)


@admin_views.route('/admin/applications', methods=["GET"])
@login_required
def admin_application():
    c_user = current_user
    organisations = EsthenosOrg.objects.all()
    user = EsthenosUser.objects.get(id=c_user.id)
    permissions=user.permissions
    if "EMP_EXECUTIVE" in permissions or "EMP_MANAGER" in permissions or "EMP_VP" in permissions:
        if not permissions["data_entry"]=="yes":
            abort(403)
    if session['role'] != "ADMIN" and session['role'] !="EMP_EXECUTIVE":
        abort(403)
    username = current_user.name

    tagged_applications = EsthenosOrgApplication.objects.all() #filter(upload_type="MANUAL_UPLOAD")#.filter(Q(status=1) |Q(status=0))
    kwargs = locals()
    return render_template("admin_applications.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/areas/<reg_id>', methods=["GET"])
@login_required
def admin_org_areas(org_id,reg_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    data = EsthenosOrgArea.objects.get(organisation=organisation,region=reg_id)
    print data
    regions = []
    for br in data:
        regions.append({'id':str(br.id),'name':br.region_name})
    print regions
    return Response(response=json.dumps(regions),
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/organisation/<org_id>/branches/<area_id>', methods=["GET"])
@login_required
def admin_org_branches(org_id,area_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    data = EsthenosOrgBranch.objects.get(organisation=organisation,area=area_id)
    print data
    branches = []
    for br in data:
        branches.append({'id':str(br.id),'name':br.branch_name})
    print branches
    return Response(response=json.dumps(branches),
        status=200,
        mimetype="application/json")


@admin_views.route('/admin/organisation/<org_id>/regions/<state_id>', methods=["GET"])
@login_required
def admin_org_regions(org_id,state_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    data = EsthenosOrgBranch.objects.get(organisation=organisation,state=state_id)
    print data
    regions = []
    for br in data:
        regions.append({'id':str(br.id),'name':br.region_name})
    print regions
    return Response(response=json.dumps(regions),
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/organisation/<org_id>/applications', methods=["GET"])
@login_required
def admin_org_applications(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    applications = EsthenosOrgApplication.objects.filter(organisation=organisation)
    applications_list = []
    for app in applications:
        applications_list.append({'id':str(app.id),
                                      'date_created':str(app.date_created),
                                      'upload_type':app.upload_type,
                                      'current_status':str(app.current_status.status)
        })

    return Response(response=json.dumps(applications_list),
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/organisation/<org_id>/application/<app_id>', methods=["GET"])
@login_required
def admin_application_id(org_id,app_id):
    if not session['role'] == "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    app_urls = list()
    applications = EsthenosOrgApplication.objects.filter(application_id = app_id)

    if len(applications)==0:
        redirect("/admin/applications")

    application = applications[0]
    kyc_urls, kyc_ids = [], []
    gkyc_urls, gkyc_ids = [], []

    if application.tag is not None:
        for kyc_id in application.tag.app_file_pixuate_id:
            app_urls.append(get_url_with_id(kyc_id))

        for kyc_id_key in application.tag.kyc_file_pixuate_id.keys():
            kyc_id = application.tag.kyc_file_pixuate_id[kyc_id_key]
            kyc_ids.append(kyc_id)
            kyc_urls.append(get_url_with_id(kyc_id))

        for gkyc_id_key in application.tag.gkyc_file_pixuate_id.keys():
            gkyc_id = application.tag.gkyc_file_pixuate_id[gkyc_id_key]
            gkyc_ids.append(gkyc_id)
            gkyc_urls.append(get_url_with_id(gkyc_id))

    today = datetime.datetime.today()
    disbursement_date = datetime.datetime.today() + timedelta(days=1)
    disbursement_date_str = disbursement_date.strftime('%d/%m/%Y')
    products = EsthenosOrgProduct.objects.filter(organisation = application.owner.organisation)

    kwargs = locals()
    return render_template("admin_application_manual_DE.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/application/<app_id>', methods=["POST"])
@login_required
def submit_application(org_id,app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    application_id = request.form.get("application_id")
    form = AddApplicationManual(request.form)
    if form.validate():
        form.save()
    print form.errors
    new_num = int(app_id[-6:])+1
    new_id = app_id[0:len(app_id)-6] + "{0:06d}".format(new_num)
    new_apps = EsthenosOrgApplication.objects.filter(application_id = new_id)
    if len(new_apps) >0:
        return redirect("/admin/organisation/"+org_id+"/application/"+new_id+"/")
    else:
        return redirect("/admin/organisation/"+org_id+"/application/"+app_id+"/")


@admin_views.route('/admin/organisation/<org_id>/application/<app_id>/cashflow', methods=["GET"])
@login_required
def admin_application_cashflow(org_id,app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    try:
        applications = EsthenosOrgApplication.objects.filter(application_id = app_id)
    except Exception as e:
        print e.message
    if len(applications)==0:
        redirect("/admin/cbcheck")
    app_urls = list()
    application = applications[0]
    kwargs = locals()
    return render_template("admin_cf.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/application/<app_id>/cashflow', methods=["POST"])
@login_required
def cashflow_statusupdate(org_id,app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    try:
        application = EsthenosOrgApplication.objects.filter(application_id = app_id)
        if len(application) >= 0:
            application = application[0]
            status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=datetime.datetime.now())
            status.save()
            application.timeline.append(status)
            if request.form.get("status") == "true":
                application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=170)[0]
                application.current_status_updated  = datetime.datetime.now()
                application.status = 170
            else:
                application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=180)[0]
                application.current_status_updated  = datetime.datetime.now()
                application.status = 170
            new_num = int(app_id[-6:])+1
            new_id = app_id[0:len(app_id)-6] + "{0:06d}".format(new_num)
            new_apps = EsthenosOrgApplication.objects.filter(application_id = new_id)
            if len(new_apps) >0:
                return redirect("/admin/organisation/"+org_id+"/application/"+new_id+"/cashflow")
    except Exception as e:
        print e.message
    return redirect("/admin/organisation/"+org_id+"/application/"+app_id+"/cashflow")


@admin_views.route('/admin/read_pan/<object_id>', methods=["GET"])
@login_required
def read_pan(object_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    url = get_url_with_id(object_id)
    data = get_pan_details_url(url)
    print data
    kwargs = locals()
    return Response(response=data,
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/read_vid/<object_id>', methods=["GET"])
@login_required
def read_vid(object_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    url = get_url_with_id(object_id)
    data = get_vid_details_url(url)
    print data
    kwargs = locals()
    return Response(response=data,
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/read_aadhaar/<object_id>', methods=["GET"])
@login_required
def read_aadhaar(object_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    url = get_url_with_id(object_id)
    data = get_aadhaar_details_url(url)
    print data
    kwargs = locals()
    return Response(response=data,
        status=200,\
        mimetype="application/json")


@admin_views.route('/admin/organisation/<org_id>/application/<app_id>/track', methods=["GET"])
@login_required
def admin_application_id_track(org_id, app_id):
    if session['role'] != "ADMIN":
        abort(403)

    user = EsthenosUser.objects.get(id=current_user.id)
    organisation = EsthenosOrg.objects.get(id = org_id)
    application = EsthenosOrgApplication.objects.get(organisation=organisation,application_id=app_id)
    kwargs = locals()
    return render_template("admin_application_tracking.html", **kwargs)


@admin_views.route('/admin/cbcheck', methods=["GET"])
@login_required
def admin_cbcheck():
     if session['role'] != "ADMIN":
         abort(403)
     username = current_user.name
     c_user = current_user
     user = EsthenosUser.objects.get(id=c_user.id)
     kwargs = locals()
     return render_template("admin_cbcheck.html", **kwargs)


@admin_views.route('/admin/disbursement', methods=["GET"])
@login_required
def admin_disbursement():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_disbursement.html", **kwargs)


@admin_views.route('/admin/logout', methods=["GET"])
@login_required
def admin_logout():
    if session['role'] != "ADMIN":
        abort(403)
    logout_user()
    return redirect( "/admin/login")


@admin_views.route('/internal/pdf_if/<group_id>', methods=["GET"])
def admin_ipnpfr(group_id):
    group = EsthenosOrgGroup.objects.get(group_id=group_id)
    apps = EsthenosOrgApplication.objects.filter(group=group).filter(Q(status=272)or Q(status=276))
    disbursement_date = datetime.datetime.now()
    org_name = "Hindusthan Microfinance"
    kwargs = locals()
    body = render_template( "pdf_InsuranceFees.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message
    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'if'
    return response


@admin_views.route('/internal/pdf_pf/<group_id>', methods=["GET"])
def admin_processing_fees(group_id):
    group = EsthenosOrgGroup.objects.get(group_id=group_id)
    apps = EsthenosOrgApplication.objects.filter(group=group).filter(Q(status=272)or Q(status=276))
    disbursement_date = datetime.datetime.now()
    org_name = "Hindusthan Microfinance"
    kwargs = locals()
    body = render_template( "pdf_Processing_Fees.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message
    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'pf'
    return response


@admin_views.route('/admin/schedule', methods=["GET"])
def admin_schedule():
    kwargs = locals()
    return render_template( "pdf_SCHEDULE_A.html", **kwargs)


@admin_views.route('/admin/profile',methods=["GET"])
def admin_profile():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_profile.html",**kwargs)


@admin_views.route('/admin/pdf_dpn', methods=["GET"])
def admin_dpn():
    kwargs = locals()
    body = render_template( "pdf_DPN.html", **kwargs)
    try:
        pdfkit.from_string(body, 'dpn.pdf')
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'dpn'
    return response


@admin_views.route('/internal/pdf_sl/<grp_id>', methods=["GET"])
def admin_sanction(grp_id):
    group = EsthenosOrgGroup.objects.get(group_id=grp_id)
    apps = EsthenosOrgApplication.objects.filter(group=group).filter(Q(status=272)or Q(status=276))

    product = apps[0].product
    print product
    disbursement_date = datetime.datetime.now()
    org_name = "Hindusthan Microfinance"
    kwargs = locals()
    body = render_template( "pdf_Sanction_Letter_Hindusthan.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.25in',
            'margin-bottom': '0.35in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'sanction'
    return response


@admin_views.route('/admin/acknowledgement', methods=["GET"])
def admin_acknowledgement():
    kwargs = locals()
    return render_template( "pdf_HMPLACK.html", **kwargs)


@admin_views.route('/admin/acknowledgementother', methods=["GET"])
def admin_acknowledgementother():
    kwargs = locals()
    return render_template( "pdf_HMPL_ACK_OTH.html", **kwargs)


@admin_views.route('/admin/hmplcashflow', methods=["GET"])
def admin_hmplcashflow():
    kwargs = locals()
    return render_template( "pdf_HMPL_CASHFLOW.html", **kwargs)


@admin_views.route('/admin/hmplgrt', methods=["GET"])
def admin_hmplgrt():
    kwargs = locals()
    return render_template( "pdf_HMPL_GRT.html", **kwargs)


@admin_views.route('/internal/pdf_application/<app_id>', methods=["GET"])
def admin_pdf_application(app_id):
    app = EsthenosOrgApplication.objects.get(application_id=app_id)
    disbursement_date = datetime.datetime.now()
    interest_rate = 26.0
    kwargs = locals()
    body = render_template( "pdf_HApplication.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.50in',
            'margin-right': '0.50in',
            'margin-bottom': '0.50in',
            'margin-left': '0.50in',
            'encoding': "UTF-8",
            'orientation' : 'Portrait'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=application_%s.pdf' % app_id
    return response


@admin_views.route('/internal/pdf_hccs_reciept/<group_id>', methods=["GET"])
def adminpdf_hccs_reciept(group_id):
    group = EsthenosOrgGroup.objects.get(group_id=group_id)
    apps = EsthenosOrgApplication.objects.filter(group=group)
    disbursement_date = datetime.datetime.now()
    interest_rate = 26.0
    kwargs = locals()
    body = render_template( "pdf_HCCS_Receipt.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.50in',
            'margin-right': '0.50in',
            'margin-bottom': '0.50in',
            'margin-left': '0.50in',
            'encoding': "UTF-8",
            'orientation' : 'Portrait'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'RdReceipt'
    return response


@admin_views.route('/internal/pdf_dpn/<group_id>', methods=["GET"])
def admin_hmpdpn(group_id):
    group = EsthenosOrgGroup.objects.get(group_id=group_id)
    apps = EsthenosOrgApplication.objects.filter(group=group).filter(Q(status=272)or Q(status=276))
    disbursement_date = datetime.datetime.now()
    interest_rate = 26.0
    kwargs = locals()
    body = render_template( "pdf_HMPL_DPN_HINDI.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.50in',
            'margin-right': '0.50in',
            'margin-bottom': '0.50in',
            'margin-left': '0.50in',
            'encoding': "UTF-8",
            'orientation' : 'Portrait'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'dpn'
    return response


@admin_views.route('/internal/pdf_la/<group_id>/<dis_date_str>', methods=["GET"])
def admin_hmplloanagreement(group_id,dis_date_str):
    group = EsthenosOrgGroup.objects.get(group_id=group_id)
    apps = EsthenosOrgApplication.objects.filter(group=group).filter(Q(status=250) or Q(status=272)or Q(status=276))
    disbursement_date =    datetime.datetime.strptime(dis_date_str, "%d-%m-%Y").date()
    interest_rate = 26.0
    kwargs = locals()
    body = render_template( "pdf_HMPL_LA_New_Hindi.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.25in',
            'margin-bottom': '0.75in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Portrait'
        }
        pdfkit.from_string(body, 'dpn.pdf',options=options)
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'la'
    return response


@admin_views.route('/admin/hmplloancard', methods=["GET"])
def admin_hmplloancard():
    kwargs = locals()
    return render_template( "pdf_HMPL_Loancard.html", **kwargs)


@admin_views.route('/admin/hmplppl', methods=["GET"])
def admin_hmplppl():
    kwargs = locals()
    return render_template( "pdf_HMPL_PPL.html", **kwargs)


@admin_views.route('/admin/hmplsanction', methods=["GET"])
def admin_hmplsanction():
    kwargs = locals()
    return render_template( "pdf_HMPL_Sanction_Jlg.html", **kwargs)


@admin_views.route('/admin/cgt_grt_pdf', methods=["GET"])
@login_required
def admin_disbursement_pdf():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)

    kwargs = locals()
    return render_template( "pdf_disbursement.html", **kwargs)


@admin_views.route('/admin/ljlga', methods=["GET"])
@login_required
def admin_ljlga():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_LJLGAgreement.html", **kwargs)


@admin_views.route('/admin/lrpassbook', methods=["GET"])
@login_required
def admin_lrpassbook():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    org_name = "Hindusthan Microfinance"
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    body = render_template( "pdf_LRPassbook.html", **kwargs)
    try:
        pdfkit.from_string(body, 'pass.pdf')
    except Exception as e:
        print e.message

    raw_bytes = ""
    with open('pass.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'Passbook'
    return response

ordinals= ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th',
 '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st',
 '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']


@admin_views.route('/internal/pdf_hp/<application_id>/<dis_date_str>/<loan_amount>/<emi>/<first_collection_after_indays>', methods=["GET"])
def admin_hindustanpassbook(application_id,dis_date_str,loan_amount,emi,first_collection_after_indays):
    app = EsthenosOrgApplication.objects.get(application_id=application_id)
    disbursement_date =    datetime.datetime.strptime(dis_date_str, "%d-%m-%Y").date()
    second_collection_after_indays = 30
    first_emi = float(emi)
    rate_of_interest= .260/12.0
    current_principal = float(loan_amount)
    passbook_rows = list()
    for i in range(1,25):
        row= dict()
        interest = 0.0
        if(i==1):
            interest = float(first_collection_after_indays)/30.0 * rate_of_interest  * current_principal
        else:
            interest = second_collection_after_indays/30.0 * rate_of_interest * current_principal
        date_after_month = disbursement_date.today()+ relativedelta(months=i)

        collection_date = disbursement_date.today()+ relativedelta(days=int(first_collection_after_indays))
        collection_day = ordinals[int(collection_date.day)]
        import math
        interest = math.ceil(interest * 1000)/1000.0
        frac, whole = math.modf(interest)
        if frac>0.5:
            interest = whole+1
        else:
            interest = whole

        row["date"] = str(disbursement_date.day)+"/"+date_after_month.strftime("%b")+"/"+str(date_after_month.year)
        row["interest"] = interest
        row["prev_os"] = current_principal
        current_principal = current_principal-(first_emi - interest)
        row["principal"] = (first_emi - interest)

        if i==24:
            row["emi"] = first_emi+current_principal
            current_principal= 0
        else:
            row["emi"] = first_emi
        row["next_os"] = current_principal

        passbook_rows.append(row)

    org_name = "Hindusthan Microfinance"
    kwargs = locals()

    body = render_template( "pdf_HindustanPassbook.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.15in',
            'margin-right': '0.0in',
            'margin-bottom': '0.15in',
            'margin-left': '0.0in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        pdfkit.from_string(body, 'tmp.pdf',options=options)
    except Exception as e:
        print "in exception"
        print e.message

    raw_bytes = ""
    with open('tmp.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line
    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] =\
    'inline; filename=%s.pdf' % 'hp'
    return response


@admin_views.route('/admin/signup', methods=["GET", "POST"])
def admin_signup():
    if request.method == "POST":
        reg_form = RegistrationFormAdmin( request.form)
        form = reg_form
        if form.validate():
            user = form.save()
            userobj = EsthenosUser.objects.get(id=user.get_id())
            userobj.roles= list()
            userobj.roles.append("ADMIN")
            userobj.active = True
            userobj.save()
            user = EsthenosUser.objects.get( email=form.email.data)

            if (form.type.data == "ADMIN" ):
                login_user(user)
                session['type'] = "ADMIN"
                return redirect( '/admin/login')

        else:
            flash_errors(reg_form)
            kwargs = {"login_form": reg_form}
            return render_template( "auth/login_admin.html", **kwargs)

    else:
        reg_form = RegistrationFormAdmin()

    kwargs = locals()
    return render_template("admin_signup.html", **kwargs)


@admin_views.route('/admin/login', methods=["GET", "POST"])
def login_admin():
    next_url = request.form.get( "next", None) or request.args.get( "next", None) or session.get("next_url", None)

    if request.method == "GET" and not next_url and request.referrer:
        urldata = urlparse.urlparse( request.referrer)
        if urldata.path.find("/admin/login") != 0:
            host = request.headers.get("HOST", "")
            if host and urldata.netloc.find(host) > -1:
                next_url = request.referrer

    if not next_url:
      next_url = "/admin/dashboard"

    session["next_url"] = next_url

    if request.method == "POST":
        login_form = LoginForm( request.form)
        form = login_form
        if form.validate():
            user = EsthenosUser.objects.get( email=form.email.data)
            login_user(user)
            confirm_login()
            if form.role.data == "ADMIN":
                session['type'] = "ADMIN"
                return redirect(next_url)

        else:
            flash_errors(login_form)
            kwargs = {"login_form": login_form}
            return render_template( "auth/login_admin.html", **kwargs)
    else:
        login_form = LoginForm()

    kwargs = locals()
    return render_template("auth/login_admin.html", **kwargs)


@admin_views.route('/admin/update_settings',methods=['POST'])
@login_required
def update_settings():
    employees=EsthenosUser.objects.filter(roles__in=["EMP_EXECUTIVE"])
    for emp in employees:
        permissions=dict()
        permissions['data_entry']=request.form.get("ex_data_entry")
        permissions['cash_flow']=request.form.get("ex_cash_flow_analysis")
        permissions['view_reports']=request.form.get("ex_view_reports")
        emp.update(in__permissions = permissions)

    employees=EsthenosUser.objects.filter(roles__in=["EMP_MANAGER"])
    for emp in employees:
        permissions=dict()
        permissions['data_entry']=request.form.get("manager_data_entry")
        permissions['cash_flow']=request.form.get("manager_cash_flow_analysis")
        permissions['view_reports']=request.form.get("manager_view_reports")
        emp.permissions=permissions
        emp.update(in__permissions = permissions)

    employees=EsthenosUser.objects.filter(roles__in=["EMP_VP"])
    for emp in employees:
        permissions=dict()
        permissions['data_entry']=request.form.get("vp_data_entry")
        permissions['cash_flow']=request.form.get("vp_cash_flow_analysis")
        permissions['view_reports']=request.form.get("vp_view_reports")
        emp.permissions=permissions
        emp.update(in__permissions = permissions)

    return redirect("/admin/settings")
