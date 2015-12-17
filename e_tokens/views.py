import json

from flask import Response, jsonify
from flask import Blueprint, request, session, flash

from flask_sauth.forms import LoginForm
from utils import generate_auth_token
from models import EsthenosOrgUserToken
from esthenos.settings import AWS_SETTINGS
from e_organisation.models import EsthenosUser

token_views = Blueprint('token_views', __name__,template_folder='templates')


@token_views.route('/api/app_token/generate', methods=["POST"])
def generate_token_view():
    login_form = LoginForm(request.form)
    form = login_form

    if form.validate():
        user = EsthenosUser.objects.get(email=form.email.data)

        if not user.active:
            return jsonify({'message':'your account has been deactivated'})

        session['role'] = user.hierarchy.role
        full_token = generate_auth_token(user, expiration=360000)

        token = full_token.split(".")[2]
        token_obj, status = EsthenosOrgUserToken.objects.get_or_create(full_token=full_token, token=token, user=user)

        response = {
          'id': str(user.id),
          'email': user.email,
          'role' : user.hierarchy.role,
          'token' : token,
          'bucket' : AWS_SETTINGS['AWS_S3_BUCKET'],
          'poolId' : AWS_SETTINGS['AWS_COGNITO_ID'],
          'message': 'token generated'
        }
        return jsonify(response)

    return jsonify({'message':'authentication failed'})
