__author__ = 'prathvi'
from flask import   request,Response
from flask_login import current_user, login_required
from flask import  Blueprint
import  json
from e_admin.models import EsthenosUser
import utils,models
from esthenos.mongo_encoder import encode_model
token_views = Blueprint('token_views', __name__,template_folder='templates')

@token_views.route('/api/app_token/generate', methods=["POST"])
@login_required
def generate_token_view():
    c_user = current_user
    kwargs = locals()
    expires = int(request.json.get('token_duration'))
    if expires < 0:
        expires = -1
    else:
        expires = expires *60
    b_name = request.json.get('bucket_names')
    buckets = []
    if b_name != None and b_name != "":
        b_names = b_name.split(",")
        for name in b_names:
            buck = PTrainedBucket.objects.get(name= name)
            buckets.append(buck)
    services = request.json.get("services")
    management_perms = request.json.get("management_perms")
    user = PUser.objects.get(id= c_user.id)
    if expires is -1:
        full_token = utils.generate_auth_token(c_user,expiration=360000)
    else:
        full_token = utils.generate_auth_token(c_user,expiration=expires)
    print expires
    token  = full_token.split(".")[2]
    token_obj = models.InstanceToken(full_token= full_token,token = token,trained_buckets = buckets,\
                 services=services.split(","),management_perms=management_perms.split(","),user = user,expires_in=expires)
    token_obj.save()

    print utils.verify_auth_token(token)
    return Response(json.dumps({'message':'token generated'}), content_type="application/json", mimetype='application/json')

@token_views.route('/api/app_token/<token>', methods=["DELETE"])
@login_required
def delete_token(token):
    c_user = current_user
    kwargs = locals()
    tokenobj = models.InstanceToken.objects.get(token=token)
    if str(tokenobj.user.id) == str(c_user.id):
        tokenobj.delete()
        return Response(json.dumps({"message":"successfully deleted"}), content_type="application/json", mimetype='application/json')
    return Response(json.dumps({"tokens":"unauthorised"}), content_type="application/json", mimetype='application/json')

@token_views.route('/api/app_token', methods=["GET"])
@login_required
def get_tokens():
    c_user = current_user
    kwargs = locals()
    all_tokens = models.InstanceToken.objects(user=c_user.id)
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