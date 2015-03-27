from e_organisation.forms import AddApplicationMobile

__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template,session,request,Response, jsonify
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required,confirm_login
import json
from e_admin.models import *
from esthenos.mongo_encoder import encode_model
from  werkzeug.exceptions import abort
from flask import  Blueprint
import psutil
import os
from e_admin.models import EsthenosUser
from e_organisation.models import  EsthenosOrg, EsthenosOrgApplication,EsthenosOrgProduct
import urlparse
from flask_sauth.models import authenticate,User
from e_admin.forms import AddOrganisationForm,RegistrationFormAdmin, AddEmployeeForm, AddOrganizationEmployeeForm, AddOrganisationProductForm
from flask_sauth.views import flash_errors
from flask_sauth.forms import LoginForm
import urlparse
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required
from e_tokens.models import EsthenosOrgUserToken
#from flask.ext.sendmail import Message
from blinker import signal
from esthenos import mainapp
import sys,traceback
import boto
conn = boto.connect_ses(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))

signal_user_registered = signal('user-registered')

admin_views = Blueprint('admin_views', __name__,
                        template_folder='templates')




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

# @admin_views.route('/admin/organisation/products', methods=["GET"])
# @login_required
# def admin_org_add_product():
#     if session['role'] != "ADMIN":
#         abort(403)
#     username = current_user.name
#     c_user = current_user
#     user = EsthenosUser.objects.get(id=c_user.id)
#     settings = EsthenosSettings.objects.all()[0]
#     kwargs = locals()
#     return render_template("admin_org_add_product.html", **kwargs)

@admin_views.route('/admin/add_org', methods=["GET","POST"] )
@login_required
def admin_add_org():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    if request.method == "POST":
        print request.form
        org_form = AddOrganisationForm( request.form)
        form = org_form
        if(form.validate()):
            form.save()
            settings = EsthenosSettings.objects.all()[0]
            settings.update(inc__organisations_count=1)
            print "success"
            return redirect("/admin/organisations")
        else:
            print "here error"
            flash_errors(org_form)
            print org_form.errors
            kwargs = {"login_form": org_form}
            return render_template("admin_add_org.html", **kwargs)

    else:
        kwargs = locals()
        return render_template("admin_add_org.html", **kwargs)


@admin_views.route('/admin/add_emp', methods=["GET","POST"])
@login_required
def admin_add_emp():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    if request.method == "POST":
        print "hello"
        org_form = AddEmployeeForm( request.form )

        form = org_form
        if(form.validate()):
            form.save()
            print "success"
            return redirect("/admin/employees")
        else:
            print "here error"
            flash_errors(org_form)
            print org_form.errors
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
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    employees=EsthenosUser.objects.filter(roles__in=["EMP_EXECUTIVE","EMP_MANAGER","EMP_VP"])
    kwargs = locals()
    return render_template("admin_employees.html", **kwargs)


@admin_views.route('/admin/organisations', methods=["GET"])
@login_required
def admin_organisations():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisations = EsthenosOrg.objects.all()
    kwargs = locals()
    return render_template("admin_organisation.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>', methods=["GET"])
@login_required
def admin_organisation_dashboard(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    org = EsthenosOrg.objects.get(id=org_id)
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    organisation = EsthenosOrg.objects.get(id=org_id)
    print org_id
    employees = []
    try:
        employees = EsthenosUser.objects.filter(organisation=organisation)
    except Exception as e:
        print e.message

    products = []
    try:
        products = EsthenosOrgProduct.objects.filter(organisation=organisation)
    except Exception as e:
        print e.message
    kwargs = locals()
    return render_template("admin_organisation_dashboard.html", **kwargs)

@admin_views.route('/admin/organisation/<org_id>/add_emp', methods=["GET","POST"])
@login_required
def admin_organisation_add_emp(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    print "reached here"
    if request.method == "POST":
        print request.form
        org_emp  = AddOrganizationEmployeeForm(request.form)
        form=org_emp
        print org_id
        form.save(org_id)
        if (form.validate()):
            form.save(org_id)
            print "formValidated"
            return redirect("/admin/organisation/"+org_id)
        else:
            print "some Error"
            flash_errors(form)
            print form.errors
            org = EsthenosOrg.objects.get(id=org_id)
            kwargs = locals()
            return render_template("admin_org_add_emp.html", **kwargs)
    else:

        org = EsthenosOrg.objects.get(id=org_id)
        kwargs = locals()
        return render_template("admin_org_add_emp.html", **kwargs)


@admin_views.route('/admin/organisation/<org_id>/add_product',methods=['GET','POST'])
@login_required
def admin_organisation_product(org_id):
    if session['role']=='ADMIN':
        username=current_user.name
        user=current_user
        org=EsthenosOrg.objects.get(id=org_id)
        kwargs = locals()
        if request.method=="GET":
            return render_template("admin_org_add_product.html", **kwargs)
        else:
            product=AddOrganisationProductForm(request.form)
            org_product=product
            print request.form
#            org_product.save(org_id)
            if(org_product.validate()):
                print "Product Details Validated,Saving the form"
                org_product.save(org_id)
                org = EsthenosOrg.objects.get(id=org_id)
                c_user = current_user
                user = EsthenosUser.objects.get(id=c_user.id)
                organisation = EsthenosOrg.objects.get(id=org_id)
                kwargs = locals()
                return redirect("/admin/organisation/"+org_id)
            else:
                print "Validation Error"
                print flash_errors(org_product)
                kwargs = locals()
                return redirect("/admin/organisation/"+org_id+"/add_product")
    else:
        return abort(403)
# Added by Deepak
@admin_views.route('/admin/cbcheck', methods=["GET"])
@login_required
def admin_cbcheck():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    tagged_applications = EsthenosOrgApplication.objects.all()
    kwargs = locals()
    return render_template("admin_cbcheck.html", **kwargs)
# Added by Deepak
@admin_views.route('/admin/disbursement', methods=["GET"])
@login_required
def admin_disbursement():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    tagged_applications = EsthenosOrgApplication.objects.all()
    kwargs = locals()
    return render_template("admin_disbursement.html", **kwargs)
@admin_views.route('/admin/applications', methods=["GET"])
@login_required
def admin_application():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    tagged_applications = EsthenosOrgApplication.objects.all()
    kwargs = locals()
    return render_template("admin_applications.html", **kwargs)

from datetime import date, timedelta
from pixuate_storage import  *
@admin_views.route('/admin/organisation/<org_id>/application/<app_id>', methods=["GET"])
@login_required
def admin_application_id(org_id,app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    app_urls = list()
    application = EsthenosOrgApplication.objects.filter(application_id = app_id)[0]
    for app_id in application.tag.app_file_pixuate_id:
        app_urls.append(get_url_with_id(app_id))

    kyc_urls = list()
    kyc_ids = application.tag.kyc_file_pixuate_id
    for kyc_id in application.tag.kyc_file_pixuate_id:
        kyc_urls.append(get_url_with_id(kyc_id))

    gkyc_urls = list()
    gkyc_ids = application.tag.gkyc_file_pixuate_id
    for gkyc_id in application.tag.gkyc_file_pixuate_id:
        gkyc_urls.append(get_url_with_id(gkyc_id))
    today= datetime.datetime.today()
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

    print request.form

    return redirect("/admin/organisation/5512da35e77989097c031a66/application/SA0000007/")


@admin_views.route('/admin/organisation/<org_id>/application/<app_id>/cashflow', methods=["GET"])
@login_required
def admin_application_cashflow(org_id,app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    app_urls = list()
    application = EsthenosOrgApplication.objects.filter(application_id = app_id)[0]
    kwargs = locals()
    return render_template("admin_cf.html", **kwargs)

from pixuate_storage import  *
from pixuate import  *
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

@admin_views.route('/admin/application/<app_id>/track', methods=["GET"])
@login_required
def admin_application_id_track(app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_application_tracking.html", **kwargs)


# @admin_views.route('/admin/cbcheck', methods=["GET"])
# @login_required
# def admin_cbcheck():
#     if session['role'] != "ADMIN":
#         abort(403)
#     username = current_user.name
#     c_user = current_user
#     user = EsthenosUser.objects.get(id=c_user.id)
#     kwargs = locals()
#     return render_template("admin_cbcheck.html", **kwargs)


# @admin_views.route('/admin/disbursement', methods=["GET"])
# @login_required
# def admin_disbursement():
#     if session['role'] != "ADMIN":
#         abort(403)
#     username = current_user.name
#     c_user = current_user
#     user = EsthenosUser.objects.get(id=c_user.id)
#     kwargs = locals()
#     return render_template("admin_disbursement.html", **kwargs)



@admin_views.route('/admin/logout', methods=["GET"])
@login_required
def admin_logout():
    if session['role'] != "ADMIN":
        abort(403)
    logout_user()
    return redirect( "/admin/login")

@admin_views.route('/admin/ipnpfr', methods=["GET"])
@login_required
def admin_ipnpfr():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_IPNPFR.html", **kwargs)

#Added By Deepak

@admin_views.route('/admin/ipnpfrtwo', methods=["GET"])
@login_required
def admin_ipnpfrtwo():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_IPNPFR_two.html", **kwargs)

#Added By Deepak
@admin_views.route('/admin/schedule', methods=["GET"])
@login_required
def admin_schedule():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_SCHEDULE_A.html", **kwargs)
#Added By Deepak
@admin_views.route('/admin/dpn', methods=["GET"])
@login_required
def admin_dpn():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_DPN.html", **kwargs)
#Added By Deepak

@admin_views.route('/admin/sanction', methods=["GET"])
@login_required
def admin_sanction():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_Sanction_Letter.html", **kwargs)




@admin_views.route('/admin/disbursement_pdf', methods=["GET"])
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
    usr = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template( "pdf_LRPassbook.html", **kwargs)



@admin_views.route('/admin/signup', methods=["GET", "POST"])
#@login_required
def admin_signup():
    if request.method == "POST":

        reg_form = RegistrationFormAdmin( request.form)
        form = reg_form
        if(form.validate()):
            user = form.save()
            userobj = EsthenosUser.objects.get(id=user.get_id())
            userobj.roles= list()
            userobj.roles.append("ADMIN")
            userobj.active = True
            userobj.save()
            print "here entered"
            user = EsthenosUser.objects.get( email=form.email.data)
            print form.type.data
            if (form.type.data == "ADMIN" ):
                login_user(user)
                session['type'] = "ADMIN"
                print "success"
                return redirect( '/admin/login')

        else:
            print "here error"
            flash_errors(reg_form)
            print reg_form.errors
            kwargs = {"login_form": reg_form}
            return render_template( "auth/login_admin.html", **kwargs)
    else:
        reg_form = RegistrationFormAdmin()
    kwargs = locals()
    return render_template("admin_signup.html", **kwargs)

@admin_views.route('/admin/login', methods=["GET", "POST"])
def login_admin():
    next_url = request.form.get( "next", None) or request.args.get( "next", None) or session.get("next_url", None)

    if( request.method == "GET" and not next_url and request.referrer):
        urldata = urlparse.urlparse( request.referrer)
        if( urldata.path.find("/admin/login") != 0):
            host = request.headers.get("HOST", "")
            if( host and urldata.netloc.find(host) > -1):
                next_url = request.referrer

    if( not next_url): next_url = "/admin/dashboard"

    session["next_url"] = next_url
    def do_redirect():
        #del( session["next_url"])
        return redirect( next_url)

    if request.method == "POST":
        login_form = LoginForm( request.form)
        form = login_form
        if(form.validate()):

            user = EsthenosUser.objects.get( email=form.email.data)
            login_user(user)
            confirm_login()
            print form.role.data
            if (form.role.data == "ADMIN" ):
                session['type'] = "ADMIN"
                print "success"
                return do_redirect()

        else:
            print "here error"
            flash_errors(login_form)
            print login_form.errors
            kwargs = {"login_form": login_form}
            return render_template( "auth/login_admin.html", **kwargs)
    else:
        login_form = LoginForm()

    kwargs = locals()
    return render_template("auth/login_admin.html", **kwargs)


@admin_views.route('/admin/mobile/application',methods=['POST'])
def mobile_application():
    jsonlist= request.form
    print jsonlist
    request.files
    app_form=AddApplicationMobile(jsonlist)
    if(app_form.validate()):
        print "Form Validated"
        print "Saving Form"
        app_form.save()
    else:
        flash_errors(app_form)
        print "Could Not validate"
    kwargs = locals()
    return render_template("auth/login_admin.html", **kwargs)



