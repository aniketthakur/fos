__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template,session,request,Response
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required,confirm_login
import json
from p_admin.models import *
from esthenos.mongo_encoder import encode_model
from  werkzeug.exceptions import abort
from flask import  Blueprint
import psutil
import os
from p_admin.models import EsthenosUser
from p_organisation.models import  EsthenosOrg
import urlparse
from flask_sauth.models import authenticate,User
from p_admin.forms import AddOrganisationForm,RegistrationFormAdmin, AddEmployeeForm, AddOrganizationEmployeeForm
from flask_sauth.views import flash_errors
from flask_sauth.forms import LoginForm
import urlparse
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required
from p_tokens.models import EsthenosOrgUserToken
#from flask.ext.sendmail import Message
from blinker import signal
from esthenos import mainapp
import sys,traceback
import boto
from p_tokens.utils import verify_dev_request_token
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
        user = EsthenosUser.objects.get(id=c_user.id)
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

    kwargs = locals()
    return render_template("admin_organisation_dashboard.html", **kwargs)

@admin_views.route('/admin/organisation/<org_id>/add_emp', methods=["GET","POST"])
@login_required
def admin_organisation_add_emp(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    print "reached here"
    if request.method == "POST":
        org_emp  = AddOrganizationEmployeeForm(request.form)
        form=org_emp
        print org_id
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
        user = EsthenosUser.objects.get(id=c_user.id)
        org = EsthenosOrg.objects.get(id=org_id)
        kwargs = locals()
        return render_template("admin_org_add_emp.html", **kwargs)

@admin_views.route('/admin/applications', methods=["GET"])
@login_required
def admin_application():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_applications.html", **kwargs)


@admin_views.route('/admin/application/<app_id>', methods=["GET"])
@login_required
def admin_application_id(app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_application_manual_DE.html", **kwargs)

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

@admin_views.route('/admin/application/<app_id>/track_final', methods=["GET"])
@login_required
def admin_application_id_trackfinal(app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    user = EsthenosUser.objects.get(id=c_user.id)
    kwargs = locals()
    return render_template("admin_application_tracking_final.html", **kwargs)

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

@admin_views.route('/admin/employee/signup', methods=["POST"])
def developer_signup():
    if request.method == "POST":
        register_form = RegistrationForm( request.form)
        form = register_form

        if(form.validate()):
            user = form.save()
            signal_user_registered.send("flask-satuh", user=user,plan_name = form.plan.data)
            user = EsthenosUser.objects.get(id=user.get_id())
            user.roles= list()
            user.roles.append("EMPLOYEE")
            user.p_user_type = form.user_type.data # "ACCOUNT_OWNER"
            #new_user.p_user_type = "ACCOUNT_USER"
            if form.owner_id.data is not None and form.owner_id.data != "":
                owner = None
                try:
                    owner = EsthenosUser.objects.get(id = form.owner_id.data)
                except Exception,e:
                    print e.message
                    type_, value_, traceback_ = sys.exc_info()
                    print traceback.format_exception(type_, value_, traceback_)
                user.owner = owner
                user.billing_enabled = True
            user.active = True
            user.save()
            from pitaya.utils import subscribe
            subscribe(user.name,user.email)
            html_data = render_template("email_welcome.html",user = user.name)
            conn.send_email(current_app.config["SERVER_EMAIL"], "Welcome To Pixuate",None,[user.email],format="html" ,html_body=html_data)
            return redirect( next_url)
        else:
            flash_errors(register_form)
            kwargs = {"register_form": register_form}
            return render_template( "auth/signup.html", **kwargs)



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