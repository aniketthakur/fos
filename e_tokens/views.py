__author__ = 'prathvi'
from flask import   request,Response
from flask_login import current_user, login_required,login_user
from flask import  Blueprint
import  json
from e_admin.models import EsthenosUser
import utils,models
from esthenos.mongo_encoder import encode_model
from flask_sauth.forms import RegistrationForm, LoginForm
token_views = Blueprint('token_views', __name__,template_folder='templates')

@token_views.route('/api/app_token/generate', methods=["POST"])
def generate_token_view():
    c_user = current_user
    kwargs = locals()
    expires = -1
    login_form = LoginForm( request.form)
    print login_form
    form = login_form
    if(form.validate()):
        user = EsthenosUser.objects.get( email=form.email.data)
        if expires is -1:
            full_token = utils.generate_auth_token(user,expiration=360000)
        else:
            full_token = utils.generate_auth_token(user,expiration=expires)
        print expires
        print full_token
        token  = full_token.split(".")[2]
        token_obj,status = models.EsthenosOrgUserToken.objects.get_or_create(full_token= full_token,token = token,user = user,expires_in=expires)
        print utils.verify_auth_token(token)
        return Response(json.dumps({'message':'token generated','token':token}), content_type="application/json", mimetype='application/json')
    return Response(json.dumps({'message':'token generation failed'}), content_type="application/json", mimetype='application/json')

@token_views.route('/api/app_token/<token>', methods=["DELETE"])
@login_required
def delete_token(token):
    c_user = current_user
    kwargs = locals()
    tokenobj = models.EsthenosOrgUserToken.objects.get(token=token)
    if str(tokenobj.user.id) == str(c_user.id):
        tokenobj.delete()
        return Response(json.dumps({"message":"successfully deleted"}), content_type="application/json", mimetype='application/json')
    return Response(json.dumps({"tokens":"unauthorised"}), content_type="application/json", mimetype='application/json')

@token_views.route('/api/app_token', methods=["GET"])
@utils.login_or_key_required
def get_tokens():
    c_user = current_user
    kwargs = locals()
    all_tokens = models.EsthenosOrgUserToken.objects(user=c_user.id)
    tokens = list()
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