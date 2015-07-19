from functools import wraps

from flask import request, abort
from e_admin.models import EsthenosUser

from models import EsthenosOrgUserToken
from esthenos import mainapp as app

from mongoengine.queryset import DoesNotExist
from flask_login import current_user, current_app, login_user
from itsdangerous import SignatureExpired, BadSignature, JSONWebSignatureSerializer as Serializer


# The actual decorator function
def login_or_key_required(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('instance_token'):
            user = verify_auth_token(request.args.get('instance_token'))
            if user is not None and current_user.is_authenticated():
                return view_function(*args, **kwargs)
            else:
                abort(401)

        elif request.headers.has_key('EsthenosOrgUserToken'):
            user = verify_auth_token(token=request.headers['EsthenosOrgUserToken'])
            if user is not None and current_user.is_authenticated():
                return view_function(*args, **kwargs)
            else:
                abort(401)

        elif not current_user.is_authenticated():
            return current_app.login_manager.unauthorized()

        else:
            return view_function(*args, **kwargs)

    return decorated_function


def generate_auth_token(current_user, expiration = 3600):
    s = Serializer(app.config['SECRET_KEY'])
    return s.dumps({ 'id': str(current_user.id) })


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        tokenobj = EsthenosOrgUserToken.objects.filter(token = token)[0]
        data = s.loads(tokenobj.full_token)

    except SignatureExpired as e:
            print "token expired", e
            return None

    except BadSignature as e:
        print "bad signature", e
        return None

    except DoesNotExist as e:
        print "does not exists", e
        return None

    user = EsthenosUser.objects.filter(id=data['id'])[0]
    login_user(user)
    return user