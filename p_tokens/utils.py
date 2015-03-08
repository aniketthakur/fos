__author__ = 'prathvi'
from functools import wraps
from flask import request, abort
from p_user.models import EsthenosUser
from esthenos import mainapp as app
from models import EsthenosOrgUserToken
from flask_login import  current_user,current_app
from flask_login import current_user, login_user
from mongoengine.queryset import DoesNotExist
# The actual decorator function
def login_or_key_required(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('instance_token'):
            print request.args.get('instance_token')
            user = verify_auth_token(request.args.get('instance_token'))
            if user is not None and current_user.is_authenticated():
                #see if you want to add something more here
                return view_function(*args, **kwargs)
            else:
                abort(401)
        elif request.headers.has_key('InstanceToken'):
            user = verify_auth_token(token=request.headers['InstanceToken'])
            if user is not None and current_user.is_authenticated():
                #see if you want to add something more here
                return view_function(*args, **kwargs)
            else:
                abort(401)

        elif not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        else:
            return view_function(*args, **kwargs)
    return decorated_function

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature

def generate_auth_token(current_user, expiration = 3600):
    print app.config['SECRET_KEY']
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    return s.dumps({ 'id': str(current_user.unique_id) })

def verify_dev_request_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        tokenobj = DevRequestToken.objects.get(token = token)
        print tokenobj.full_token
        data = s.loads(tokenobj.full_token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user = PUser.objects.get(unique_id=data['id'])
    return user

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    tokenobj = None
    data = dict()
    try:
        tokenobj = InstanceToken.objects.get(token = token)
        print tokenobj.full_token
        data = s.loads(tokenobj.full_token)
        print "valid token"
    except SignatureExpired:
        if tokenobj.expires_in is -1 :
            full_token = generate_auth_token(tokenobj.user,360000)
            token  = full_token.split(".")[2]
            tokenobj.full_token= full_token
            tokenobj.token = token
            tokenobj.save()
            data = s.loads(tokenobj.full_token)
            print "token expired- regenerated"
        else:
            print "token expired"
            return None
    except BadSignature:
        print "bad sig"
        return None # invalid token

    except DoesNotExist:
        print "does bot exists"
        return None

    print data

    user = PUser.objects.get(unique_id=data['id'])
    login_user(user)
    return user