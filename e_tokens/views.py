from flask import jsonify
from flask import Blueprint, request, session

from flask_sauth.forms import LoginForm
from utils import generate_auth_token
from models import EsthenosOrgUserToken
from esthenos import mainapp as app
from esthenos.settings import AWS_SETTINGS
from e_organisation.models import EsthenosUser

token_views = Blueprint('token_views', __name__)


@token_views.route('/api/token/<feature>', methods=["POST"])
def generate_token_view(feature):
    form = LoginForm(request.form)
    feature = "features_mobile_%s" % feature
    enabled = app.config["FEATURES"][feature]["enabled"]

    if form.validate():
        user = EsthenosUser.objects.get(email=form.email.data)

        if not enabled:
            return jsonify({
              'message':'the feature has been disabled.'
            })

        if not user.active:
            return jsonify({
              'message':'your account has been deactivated'
            })

        if not user.is_allowed(feature):
            return jsonify({
              'message':'you do not have permissions for the feature'
            })

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
