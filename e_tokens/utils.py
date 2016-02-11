from functools import wraps

from flask import request, abort
from models import EsthenosOrgUserToken
from esthenos import mainapp as app
from e_organisation.models import EsthenosUser

from mongoengine.queryset import DoesNotExist
from flask_login import current_user, current_app, login_user
from itsdangerous import SignatureExpired, BadSignature, JSONWebSignatureSerializer as Serializer


@app.context_processor
def feature_processor():
  def feature_show(feature):
      enabled = app.config["FEATURES"][feature]["enabled"]
      allowed = current_user.is_allowed(feature)
      is_admin = current_user.is_admin()
      return (enabled and allowed) or (enabled and is_admin)
  return dict(feature_show=feature_show)


def feature_enable(feature):
    def decorator(view_function):
        @wraps(view_function)
        def decorated(*args, **kwargs):
            app.logger.debug("FEATUERS")
            app.logger.debug("FEATUERS %s " % (feature))
            app.logger.debug(" %s " % (app.config["FEATURES"]))
            app.logger.debug("%s" % (app.config["FEATURES"][feature]))
            app.logger.debug("%s " % (app.config["FEATURES"][feature]["enabled"]))
            enabled = app.config["FEATURES"][feature]["enabled"]
            allowed = current_user.is_allowed(feature)
            is_admin = current_user.is_admin()

            if (enabled and allowed) or (enabled and is_admin):
                return view_function(*args, **kwargs)

            else:
                abort(403)

        return decorated
    return decorator


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
