import os
import sys, traceback
import json, psutil, urlparse

import boto, pdfkit
from mongoengine import Q
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

from flask.ext import excel
from flask import Blueprint, redirect, url_for, flash, current_app
from flask import render_template, session, request, Response, jsonify, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required, confirm_login
from flask_sauth.forms import LoginForm
from flask_sauth.views import flash_errors

from e_admin.forms import *
from e_tokens.utils import login_or_key_required, feature_enable
from e_reports.views import get_application_headers, get_application_rowdata
from e_pixuate.pixuate import *
from e_organisation.forms import *
from e_organisation.models import *

from blinker import signal
from esthenos import mainapp


signal_user_registered = signal('user-registered')

admin_views = Blueprint('admin_views', __name__, template_folder='templates')

ordinals= ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th',
           '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st',
           '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']


@admin_views.route('/admin/organisations', methods=["GET", "POST"])
@login_required
@feature_enable("features_admin")
def admin_organisations():
    user = EsthenosUser.objects.get(id=current_user.id)
    organisations = EsthenosOrg.objects.all()

    if request.method == "POST":
        org_form = AddOrganisationForm( request.form)
        form = org_form

        if form.validate():
            org = form.save()
            settings = EsthenosSettings.objects.all()[0]
            settings.update(inc__organisations_count=1)
            return redirect("/admin/organisation/%s/dashboard" % org.id)

        else:
            flash_errors(org_form)
            kwargs = {"login_form": org_form}
            return render_template("admin_organisation.html", **kwargs)

    if request.method == "GET":
        kwargs = locals()
        return render_template("admin_organisation.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/update', methods=["GET"] )
@login_required
@feature_enable("features_admin")
def admin_organisation_details(org_id):
    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)
    areas = EsthenosOrgArea.objects.filter(organisation=org)
    states = EsthenosOrgState.objects.filter(organisation=org)
    regions = EsthenosOrgRegion.objects.filter(organisation=org)
    branches = EsthenosOrgBranch.objects.filter(organisation=org)

    kwargs = locals()
    return render_template("admin_add_org_details.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/states', methods=["POST"])
@login_required
@feature_enable("features_admin")
def admin_org_states_update(org_id, state_id=None):
    org = EsthenosOrg.objects.get(id=org_id)

    if request.method == "POST":
        states = request.form.getlist('org_states')
        for state in states:
            state, status = EsthenosOrgState.create(name=state, organisation=org)
        return redirect(url_for("admin_views.admin_organisation_details", org_id=org_id))


@admin_views.route('/admin/organisation/<org_id>/states', methods=["GET"])
@login_required
@feature_enable("features_geo_api")
def admin_org_states_list(org_id):
    org = EsthenosOrg.objects.get(id=org_id)
    state_id = request.args.get('state_id')
    print state_id
    if request.method == "GET" and (state_id is not None):
        state = EsthenosOrgState.objects.get(organisation=org_id, id=state_id)
        return jsonify(state.children)

    if request.method == "GET":
        states = EsthenosOrgState.objects.filter(organisation=org_id)
        states = [state.json for state in states]
        return jsonify(children=states, count=len(states))


@admin_views.route('/admin/organisation/<org_id>/regions', methods=["GET"])
@login_required
@feature_enable("features_geo_api")
def admin_org_regions_list(org_id):
    region_id = request.args.get('region_id')
    org = EsthenosOrg.objects.get(id=org_id)
    region = EsthenosOrgRegion.objects.get(organisation=org, id=region_id)
    return jsonify(region.children)


@admin_views.route('/admin/organisation/<org_id>/regions', methods=["POST"])
@login_required
@feature_enable("features_admin")
def admin_org_regions_update(org_id, region_id=None):
    org = EsthenosOrg.objects.get(id=org_id)

    if request.method == "POST":
        state = EsthenosOrgState.objects.get(id=request.form.get('org_state'))
        for region in request.form.get('org_regions').split(","):
            region, status = EsthenosOrgRegion.create(name=region, parent=state)
        return redirect(url_for("admin_views.admin_organisation_details", org_id=org_id))


@admin_views.route('/admin/organisation/<org_id>/areas', methods=["GET"])
@login_required
@feature_enable("features_geo_api")
def admin_org_areas_list(org_id):
    area_id = request.args.get('area_id')
    org = EsthenosOrg.objects.get(id=org_id)
    area = EsthenosOrgArea.objects.get(organisation=org, id=area_id)
    return jsonify(area.children)


@admin_views.route('/admin/organisation/<org_id>/areas', methods=["POST"])
@login_required
@feature_enable("features_admin")
def admin_org_areas_update(org_id, area_id=None):
    org = EsthenosOrg.objects.get(id=org_id)
    region = EsthenosOrgRegion.objects.get(id=request.form.get('org_region'))
    for area in request.form.get('org_areas').split(","):
        area, status = EsthenosOrgArea.create(name=area, parent=region)
    return redirect(url_for("admin_views.admin_organisation_details", org_id=org_id))


@admin_views.route('/admin/organisation/<org_id>/branches', methods=["GET"])
@login_required
@feature_enable("features_geo_api")
def admin_org_branches_list(org_id):
    branch_id = request.args.get('branch_id')
    org = EsthenosOrg.objects.get(id=org_id)
    branch = EsthenosOrgBranch.objects.get(organisation=org_id, id=branch_id)
    return jsonify(branch.children)


@admin_views.route('/admin/organisation/<org_id>/branches', methods=["POST"] )
@login_required
@feature_enable("features_admin")
def admin_org_branches_update(org_id, branch_id=None):
    org = EsthenosOrg.objects.get(id=org_id)

    if request.method == "POST":
        area = EsthenosOrgArea.objects.get(id=request.form.get('org_area'))
        for branch in request.form.get('org_branch_data').split(","):
            branch, status = EsthenosOrgBranch.create(name=branch, parent=area)
        return redirect(url_for("admin_views.admin_organisation_details", org_id=org_id))


@admin_views.route('/admin/organisation/<org_id>/dashboard', methods=["GET"])
@login_required
@feature_enable("features_admin")
def admin_organisation_dashboard(org_id):
    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)

    kwargs = locals()
    return render_template("admin_organisation_dashboard.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/settings', methods=["GET", "POST"])
@login_required
@feature_enable("features_admin")
def admin_organisation_settings(org_id):
    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation

    features = mainapp.config["FEATURES"]
    features = sorted(features.items(), key=lambda x: x[1]['title'])

    hierarchy = EsthenosOrgHierarchy.objects.filter(organisation=user.organisation, level__gt=0).order_by('+level')
    settings, status = EsthenosOrgSettings.objects.get_or_create(organisation=user.organisation)

    if request.method == "POST":
        settings = {}
        for designation in hierarchy:
            settings[str(designation.id)] = []

        for key, value in request.form.items():
            designation, feature = key.split("|")
            settings[designation].append(feature)

        for designation in hierarchy:
            setting = settings[str(designation.id)]
            designation.update(set__features=setting)

        return redirect(url_for("admin_views.admin_organisation_settings", org_id=org_id))

    kwargs = locals()
    return render_template("admin_org_settings.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/guidelines', methods=["POST"])
@login_required
@feature_enable("features_admin")
def admin_organisation_guidelines_rbi(org_id):
    organisation = EsthenosOrg.objects.get(id=org_id)
    settings, status = EsthenosOrgSettings.objects.get_or_create(organisation=organisation)

    if request.method == "POST":
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

        return redirect(url_for("admin_views.admin_organisation_settings", org_id=org_id))


@admin_views.route('/admin/organisation/<org_id>/targets', methods=["GET", "POST"])
@login_required
@feature_enable("features_performance_target")
def admin_organisation_targets(org_id):
    user = EsthenosUser.objects.get(id=current_user.id)
    org = user.organisation

    if request.method == "GET":
        states = EsthenosOrgState.objects.filter(organisation = user.organisation)
        regions = EsthenosOrgRegion.objects.filter(organisation = user.organisation)
        areas = EsthenosOrgArea.objects.filter(organisation = user.organisation)
        branches = EsthenosOrgBranch.objects.filter(organisation = user.organisation)

        hierarchy = EsthenosOrgHierarchy.objects.filter(organisation = user.organisation)
        targets = EsthenosOrgUserPerformanceTarget.objects.filter(organisation = user.organisation)

        kwargs = locals()
        return render_template("admin_org_targets.html", **kwargs)


    if request.method == "POST":
        branches = request.form.getlist('org_states')
        end_date = request.form.get("end_date")
        start_date = request.form.get("start_date")

        loan_target = request.form.get("loan_name")

        group_name = request.form.get("group_name")
        center_name = request.form.get("center_name")
        business_name = request.form.get("business_name")

        from datetime import datetime

        target, status = EsthenosOrgUserPerformanceTarget.objects.get_or_create(
            owner = user,
            organisation = user.organisation,

            name = request.form.get("target_name"),

            role = EsthenosOrgHierarchy.objects.get(
                id=request.form.get("target_role")
            ),

            end_date = datetime.strptime(
                request.form.get("end_date"), '%m/%d/%Y'
            ),
            start_date = datetime.strptime(
                request.form.get("start_date"), '%m/%d/%Y'
            ),

            loan_target = request.form.get("loan_target"),
            group_target = request.form.get("group_target"),
            center_target = request.form.get("center_target"),

            business_target = request.form.get("business_target"),
            applications_target = request.form.get("applications_target")
        )
        return redirect(url_for("admin_views.admin_organisation_targets", org_id=org_id))


@admin_views.route('/admin/organisation/<org_id>/employees', methods=["GET", "POST"])
@login_required
@feature_enable("features_admin")
def admin_organisation_add_emp(org_id):
    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)
    employees = EsthenosUser.objects.filter(organisation=org)

    if request.method == "POST":
        form = AddOrganizationEmployeeForm(request.form)

        if form.validate():
            form.save(org_id)
            return redirect(url_for("admin_views.admin_organisation_add_emp", org_id=org_id))

        else:
            flash_errors(form)
            kwargs = locals()
            return render_template("admin_org_emp_add.html", **kwargs)

    if request.method == "GET":
        states = EsthenosOrgState.objects.filter(organisation=org)
        hierarchy = EsthenosOrgHierarchy.objects.filter(organisation=org, level__gt=0).order_by('+level')
        kwargs = locals()
        return render_template("admin_org_emp_add.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/employees/<emp_id>', methods=["GET", "POST"])
@login_required
@feature_enable("features_admin")
def admin_organisation_add_emp_details(org_id, emp_id):
    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)
    employee = EsthenosUser.objects.get(organisation=org, id=emp_id)

    if request.method == "POST":
        form = AddOrganizationEmployeeForm(request.form)
        employee, errors = form.update(employee)
        for error, value in errors.iteritems():
            flash(value, error)
        return redirect(url_for("admin_views.admin_organisation_add_emp_details", org_id=org_id, emp_id=emp_id))

    if request.method == "GET":
        states = EsthenosOrgState.objects.filter(organisation=org)
        hierarchy = EsthenosOrgHierarchy.objects.filter(organisation=org, level__gt=0).order_by('+level')
        kwargs = locals()
        return render_template("admin_org_emp_details.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/psychometric_questions',methods=['GET','POST'])
@login_required
@feature_enable("features_psychometric_questions")
def psychometric_questions(org_id):
    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)
    questions = EsthenosOrgPsychometricTemplateQuestion.objects.filter(organisation=org)

    if request.method == "GET":
        kwargs = locals()
        return render_template("admin_organisation_psychometric_questions.html", **kwargs)

    if request.method == "POST":
        question = AddOrgPsychometricTemplateQuestionsForm(request.form)

        if question.validate():
            question.save()
            kwargs = locals()
            return redirect("/admin/organisation/%s/psychometric_questions" % org_id)

        else:
            flash_errors(question)
            kwargs = locals()
            return render_template("admin_organisation_psychometric_questions.html", **kwargs)

@admin_views.route('/admin/organisation/<org_id>/employees/<emp_id>/password', methods=["GET", "POST"])
@login_required
@feature_enable("features_admin")
def admin_organisation_emp_password(org_id, emp_id):
    org = EsthenosOrg.objects.get(id=org_id)
    user = EsthenosUser.objects.get(id=current_user.id)
    employee = EsthenosUser.objects.get(organisation=org, id=emp_id)

    if request.method == "GET":
        kwargs = locals()
        return render_template('admin_org_emp_password.html', **kwargs)

    if request.method == "POST":
        password = request.form.get('password')
        employee.set_password(password)
        employee.save()
        return redirect(url_for("admin_views.admin_organisation_add_emp", org_id=org_id))

@admin_views.route('/admin/organisation/<org_id>/psychometric_questions/<question_id>/delete',methods=['POST'])
@login_required
@feature_enable("features_psychometric_questions")
def psychometric_questions_delete(org_id, question_id):
    question = EsthenosOrgPsychometricTemplateQuestion.objects.filter(id=question_id)
    question.delete()
    return redirect("/admin/organisation/%s/psychometric_questions" % org_id)


@admin_views.route('/internal/pdf_sl/<applicant_id>', methods=["GET"])
def admin_sanction(applicant_id):
    apps = EsthenosOrgApplication.objects.filter(application_id=applicant_id).filter(status__gte=240)

    disbursement_date = datetime.datetime.now()
    org_name = ""

    kwargs = locals()
    body = render_template("pdf_Sanction_Letter_Hindusthan.html", **kwargs)
    options = {
        'page-size': 'A4',
        'margin-top': '0.35in',
        'margin-right': '0.25in',
        'margin-bottom': '0.35in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'orientation' : 'Landscape'
    }
    pdfkit.from_string(body, 'pdf_sanction_letter.pdf',options=options)

    raw_bytes = ""
    with open('pdf_sanction_letter.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'sanction'
    return response


@admin_views.route('/internal/pdf_if/<applicant_id>', methods=["GET"])
def admin_ipnpfr(applicant_id):
    apps = EsthenosOrgApplication.objects.filter(application_id=applicant_id).filter(status__gte=240)

    disbursement_date = datetime.datetime.now()
    org_name = ""

    kwargs = locals()
    body = render_template( "pdf_InsuranceFees.html", **kwargs)

    options = {
        'page-size': 'A4',
        'margin-top': '0.35in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'orientation' : 'Landscape'
    }
    pdfkit.from_string(body, 'pdf_insurance_fees.pdf', options=options)

    raw_bytes = ""
    with open('pdf_insurance_fees.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'if'
    return response


@admin_views.route('/internal/pdf_pf/<applicant_id>', methods=["GET"])
def admin_processing_fees(applicant_id):
    apps = EsthenosOrgApplication.objects.filter(application_id=applicant_id).filter(status__gte=240)

    disbursement_date = datetime.datetime.now()
    org_name = ""

    kwargs = locals()
    body = render_template("pdf_Processing_Fees.html", **kwargs)

    options = {
        'page-size': 'A4',
        'margin-top': '0.35in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'orientation' : 'Landscape'
    }
    pdfkit.from_string(body, 'pdf_processing_fees.pdf', options=options)

    raw_bytes = ""
    with open('pdf_processing_fees.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'pf'
    return response


@admin_views.route('/internal/pdf_dpn/<applicant_id>', methods=["GET"])
def admin_hmpdpn(applicant_id):
    app = EsthenosOrgApplication.objects.get(application_id=applicant_id)
    disbursement_date = datetime.datetime.now()
    interest_rate = 26.0

    kwargs = locals()
    body = render_template( "pdf_HMPL_DPN_HINDI.html", **kwargs)

    options = {
        'page-size': 'A4',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': "UTF-8",
        'orientation' : 'Portrait'
    }
    pdfkit.from_string(body, 'dpn.pdf', options=options)

    raw_bytes = ""
    with open('dpn.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'dpn'
    return response


@admin_views.route('/internal/pdf_application/<app_id>', methods=["GET"])
def admin_pdf_application(app_id):
    app = EsthenosOrgApplication.objects.get(application_id=app_id)
    disbursement_date = datetime.datetime.now()
    interest_rate = 26.0

    kwargs = locals()
    body = render_template("pdf_HApplication.html", **kwargs)

    options = {
        'page-size': 'A4',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': "UTF-8",
        'orientation' : 'Portrait'
    }
    pdfkit.from_string(body, 'pdf_loan_application.pdf', options=options)

    raw_bytes = ""
    with open('pdf_loan_application.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=application_%s.pdf' % app_id
    return response


@admin_views.route('/internal/pdf_hccs_reciept/<applicant_id>', methods=["GET"])
def admin_pdf_hccs_reciept(applicant_id):
    apps = EsthenosOrgApplication.objects.filter(application_id=applicant_id)
    disbursement_date = datetime.datetime.now()
    interest_rate = 26.0

    kwargs = locals()
    body = render_template( "pdf_HCCS_Receipt.html", **kwargs)

    options = {
        'page-size': 'A4',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': "UTF-8",
        'orientation' : 'Portrait'
    }
    pdfkit.from_string(body, 'reciept.pdf', options=options)

    raw_bytes = ""
    with open('reciept.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'RdReceipt'
    return response


@admin_views.route('/internal/pdf_la/<applicant_id>/<dis_date_str>', methods=["GET"])
def admin_hmplloanagreement(applicant_id,dis_date_str):
    apps = EsthenosOrgApplication.objects.filter(application_id=applicant_id).filter(status__gte=240)
    disbursement_date = datetime.datetime.strptime(dis_date_str, "%d-%m-%Y").date()
    interest_rate = 26.0

    kwargs = locals()
    body = render_template("pdf_HMPL_LA_New_Hindi.html", **kwargs)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.25in',
        'margin-bottom': '0.75in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'orientation' : 'Portrait'
    }
    pdfkit.from_string(body, 'pdf_grt_agreement.pdf', options=options)

    raw_bytes = ""
    with open('pdf_grt_agreement.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'la'
    return response


@admin_views.route('/internal/pdf_hp/<application_id>/<dis_date_str>/<loan_amount>/<emi>/<first_collection_after_indays>', methods=["GET"])
def admin_hindustanpassbook(application_id,dis_date_str,loan_amount,emi,first_collection_after_indays):
    app = EsthenosOrgApplication.objects.get(application_id=application_id)
    disbursement_date = datetime.datetime.strptime(dis_date_str, "%d-%m-%Y").date()
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
    options = {
        'page-size': 'A4',
        'margin-top': '0.15in',
        'margin-right': '0.0in',
        'margin-bottom': '0.15in',
        'margin-left': '0.0in',
        'encoding': "UTF-8",
        'orientation' : 'Landscape'
    }
    pdfkit.from_string(body, 'pdf_passbook.pdf', options=options)

    raw_bytes = ""
    with open('pdf_passbook.pdf', 'rb') as r:
        for line in r:
            raw_bytes = raw_bytes + line

    response = make_response(raw_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'hp'
    return response
