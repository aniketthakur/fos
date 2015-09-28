import json
from flask import request, Response
from flask_login import current_user, login_required,login_user
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from flask_sauth.forms import RegistrationForm, LoginForm

from utils import generate_auth_token, login_or_key_required
from models import EsthenosOrgUserToken

from e_admin.models import EsthenosUser
from esthenos.mongo_encoder import encode_model
from esthenos.settings import AWS_SETTINGS

token_views = Blueprint('token_views', __name__,template_folder='templates')

@token_views.route('/api/app_token/generate', methods=["POST"])
def generate_token_view():
    c_user = current_user
    kwargs = locals()
    expires = -1
    login_form = LoginForm( request.form)
    form = login_form

    if form.validate():
        user = EsthenosUser.objects.get(email=form.email.data)
        if not user.active:
            flash(u'Your account has been deactivated', 'error')
            kwargs = {"login_form": login_form}

        if form.role.data == "ADMIN":
            session['role'] = "ADMIN"

        if form.role.data == "ORG_CM":
            session['role'] = "ORG_CM"

        if form.role.data == "EMP_EXECUTIVE":
            session['role'] = "EMP_EXECUTIVE"

        if expires is -1:
            full_token = generate_auth_token(user,expiration=360000)

        else:
            full_token = generate_auth_token(user,expiration=expires)

        token = full_token.split(".")[2]
        token_obj, status = EsthenosOrgUserToken.objects.get_or_create(full_token=full_token, token=token, user=user, expires_in=expires)

        response = {
          'token' : token,
          'bucket' : AWS_SETTINGS['AWS_S3_BUCKET'],
          'poolId' : AWS_SETTINGS['AWS_COGNITO_ID'],
          'message': 'token generated'
        }
        return Response(json.dumps(response), content_type="application/json", mimetype='application/json')

    return Response(json.dumps({'message':'token generation failed'}), content_type="application/json", mimetype='application/json')


@token_views.route('/api/app_token/<token>', methods=["DELETE"])
@login_required
def delete_token(token):
    c_user = current_user
    kwargs = locals()
    tokenobj = EsthenosOrgUserToken.objects.get(token=token)
    if str(tokenobj.user.id) == str(c_user.id):
        tokenobj.delete()
        return Response(json.dumps({"message":"successfully deleted"}), content_type="application/json", mimetype='application/json')
    return Response(json.dumps({"tokens":"unauthorised"}), content_type="application/json", mimetype='application/json')


@token_views.route('/api/app_token', methods=["GET"])
@login_or_key_required
def get_tokens():
    c_user = current_user
    tokens = list()
    kwargs = locals()
    all_tokens = EsthenosOrgUserToken.objects(user=c_user.id)

    for token in all_tokens:
        tok = dict()
        tok['token'] = token.token
        tok['expires_in'] = token.expires_in
        tok['date_created'] = token.date_created
        buc_names = []
        for buk in token.trained_buckets:
            buc_names.append(buk.name)
        tok['instance_buckets'] = buc_names
        tok['perms'] = token.management_perms
        tok['services'] = token.services
        tokens.append(tok)

    return Response(json.dumps({"tokens":tokens},default=encode_model), content_type="application/json", mimetype='application/json')