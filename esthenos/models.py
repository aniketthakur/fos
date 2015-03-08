__author__ = 'prathvi'

from esthenos  import db

from flask.ext.mongorest.authentication import AuthenticationBase
from flask_login import current_user


class SessionAuthentication(AuthenticationBase):
    def authorized(self):
        return current_user.is_authenticated()



class AdminSessionAuthentication(AuthenticationBase):
    def authorized(self):
        return current_user.is_authenticated() and current_user.has_role("ADMIN")

"""
Models below are to be reviewed
"""


class PAppUser(db.EmbeddedDocument):
    """
    PERM_GET("READ"),
    PERM_PUT("MODIFY"),
    PERM_ALL("ALL"),
    """
    unique_user_id = db.StringField(max_length=255, required=True)
    owner_id = db.StringField(max_length=255, required=True)
    perms = db.ListField(db.StringField(max_length=255))


class PAppToken(db.Document):
    auth_token = db.StringField(max_length=255, required=True)
    client_id = db.StringField(max_length=255, required=True)
    expires_in = db.IntField(default=0)
    unique_user_id = db.StringField(max_length=255, required=True)
    client_name = db.StringField(max_length=255, required=True)
    api_version = db.StringField(max_length=255, required=True)

    def __unicode__(self):
        return self.auth_token +" "+self.client_name

    @property
    def post_type(self):
        return self.__class__.__name__
