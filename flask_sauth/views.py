import urlparse

from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, ResetPasswordForm, NewPasswordForm, ChangePasswordForm
from flask.ext.sauth.models import User
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

auth_views = Blueprint('auth_views', __name__,
                        template_folder='templates')




@auth_views.route('/accounts/login', methods=["GET", "POST"])
def login():
    next_url = request.form.get( "next", None) or request.args.get( "next", None) or session.get("next_url", None)

    if( request.method == "GET" and not next_url and request.referrer):
        urldata = urlparse.urlparse( request.referrer)
        if( urldata.path.find("/accounts") != 0):
            host = request.headers.get("HOST", "")
            if( host and urldata.netloc.find(host) > -1):
                next_url = request.referrer

    if( not next_url): next_url = "/"

    session["next_url"] = next_url

    def do_redirect():
        #del( session["next_url"])
        return redirect( next_url)

    if( current_user.is_authenticated()):
        return do_redirect()

    if request.method == "POST":
        login_form = LoginForm( request.form)
        form = login_form
        if(form.validate()):

            login_user( form.user_cache,True)
            is_fresh  = request.form.get( "fresh", None)
            if is_fresh is not None and  is_fresh == "true":
                from flask.ext.login import confirm_login
                confirm_login()

            user = User.objects.get( email=form.email.data)
            if user.active == False:
                flash(u'Your account has been deactivated', 'error')
                kwargs = {"login_form": login_form}
                return render_template( "auth/login.html", **kwargs)
            print "In login : "+form.role.data
            if (form.role.data == "ADMIN"):
                session['role'] = "ADMIN"
                return redirect("/admin/servers")
            if (form.role.data == "ORG_CM"):
                session['role'] = "ORG_CM"
                return redirect("/")
            token =  request.args.get('token',None)
            if token is not None:
                req_token = DevRequestToken.objects.get(token=token)
                req_token.delete()
            return do_redirect()
        else:
            flash_errors(login_form)
            kwargs = {"login_form": login_form}
            return render_template( "auth/login.html", **kwargs)
    else:
        login_form = LoginForm()

    kwargs = locals()
    return render_template("auth/login.html", **kwargs)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print error
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

from p_admin.models import EsthenosUser
from esthenos.utils import random_with_N_digits

@auth_views.route("/accounts/logout")
def logout():
    session.clear()
    logout_user()
    return redirect( "/")

@auth_views.route("/accounts/password/reset", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        form = ResetPasswordForm( request.form)
        if( form.validate()):
            user = User.objects.get( email=form.email.data)
            password_reset_token = user.generate_password_reset_token()

            host = request.headers["HOST"]
            link = "http://%s/accounts/password/reset/%s" % (host, password_reset_token)

            msg = "Hi %s,\n\nSomeone (probably you) requested for a password reset at %s. Please visit the following link if you wish to reset your password:\n\n%s\n\nHave a good day!" % (user.name, host, link)
            conn.send_email(current_app.config["SERVER_EMAIL"], "[%s] Reset Password" % host, msg, [user.email])
            flash( "Sent you a mail to reset the password. Do remember to check your spam folder as well.", "success")
    else:
        form = ResetPasswordForm()
    return render_template( "auth/reset_password.html", **locals())

@auth_views.route("/accounts/password/reset/<password_reset_token>", methods=["GET", "POST"])
def do_reset_password( password_reset_token):
    user = User.objects( password_reset_token=password_reset_token).first()
    if( not user):
        flash( "Invalid request parameters. Please try resetting again.", "error")
        return redirect( "/accounts/password/reset")

    if request.method == "POST":
        form = NewPasswordForm( request.form)
        if( form.validate()):
            user.set_password( form.password1.data)
            flash( "Your password was changed successfully.", "success")
            return redirect( "/accounts/login")

    form = NewPasswordForm()
    return render_template( "auth/new_password.html", **locals())

@auth_views.route("/accounts/password/change", methods=["GET", "POST"])
@login_required
def change_password():
    c_user = current_user
    if( request.method == "POST"):
        form = ChangePasswordForm( request.form)
        if( form.validate()):
            current_user.set_password( form.password1.data)
            flash( "Your password was changed successfully.", "success")
            return redirect( "/")
    else:
        form = ChangePasswordForm()
    return render_template( "auth/change_password.html", **locals())
