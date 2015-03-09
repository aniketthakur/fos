__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template,session,request,Response
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required
import json
from p_admin.models import *
from esthenos.mongo_encoder import encode_model
from  werkzeug.exceptions import abort
from flask import  Blueprint
import psutil
import os
from p_user.models import EsthenosUser
import urlparse
from flask_sauth.models import authenticate,User
from flask_sauth.views import flash_errors
from flask_sauth.forms import LoginForm,RegistrationFormAdmin
server_views = Blueprint('server_views', __name__,
                        template_folder='templates')




@server_views.route('/admin/dashboard', methods=["GET"])
@login_required
def admin_dashboard():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_dashboard.html", **kwargs)

@server_views.route('/admin/add_org', methods=["GET","POST"] )
@login_required
def admin_add_org():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    if request.method == "POST":
        pass
    else:
        kwargs = locals()
        return render_template("admin_add_org.html", **kwargs)


@server_views.route('/admin/add_emp', methods=["GET"])
@login_required
def admin_add_emp():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_add_emp.html", **kwargs)

@server_views.route('/admin/employees', methods=["GET"])
@login_required
def admin_employees():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_employees.html", **kwargs)


@server_views.route('/admin/organisations', methods=["GET"])
@login_required
def admin_organisations():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_organisation.html", **kwargs)


@server_views.route('/admin/organisation/<org_id>', methods=["GET"])
@login_required
def admin_organisation_dashboard(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_organisation_dashboard.html", **kwargs)

@server_views.route('/admin/organisation/<org_id>/add_emp', methods=["GET"])
@login_required
def admin_organisation_add_emp(org_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_org_add_emp.html", **kwargs)

@server_views.route('/admin/applications', methods=["GET"])
@login_required
def admin_application():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_applications.html", **kwargs)


@server_views.route('/admin/application/<app_id>', methods=["GET"])
@login_required
def admin_application_id(app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_application_manual_DE.html", **kwargs)

@server_views.route('/admin/application/<app_id>/track', methods=["GET"])
@login_required
def admin_application_id_track(app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_application_tracking.html", **kwargs)

@server_views.route('/admin/application/<app_id>/track_final', methods=["GET"])
@login_required
def admin_application_id_trackfinal(app_id):
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_application_tracking_final.html", **kwargs)

@server_views.route('/admin/cbcheck', methods=["GET"])
@login_required
def admin_cbcheck():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_cbcheck.html", **kwargs)


@server_views.route('/admin/disbursement', methods=["GET"])
@login_required
def admin_disbursement():
    if session['role'] != "ADMIN":
        abort(403)
    username = current_user.name
    c_user = current_user
    kwargs = locals()
    return render_template("admin_disbursement.html", **kwargs)


@server_views.route('/admin/signup', methods=["GET", "POST"])
#@login_required
def admin_signup():
    if request.method == "POST":

        reg_form = RegistrationFormAdmin( request.form)
        form = reg_form
        if(form.validate()):
            form.save()
            print "here entered"
            user = EsthenosUser.objects.get( email=form.email.data)
            print form.type.data
            if (form.type.data == "ADMIN" ):
                login_user(user)
                session['type'] = "ADMIN"
                print "success"
                return do_redirect()

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

@server_views.route('/admin/login', methods=["GET", "POST"])
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
            user_data = authenticate(form.email.data, form.password.data)
            login_user(user_data)
            user = EsthenosUser.objects.get( email=form.email.data)
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