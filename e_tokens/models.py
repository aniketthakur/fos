__author__ = 'prathvi'

import datetime
from esthenos.mongo_encoder import encode_model
from e_admin.models import EsthenosUser
from esthenos import db

class EsthenosOrgUserToken(db.Document):
    token = db.StringField(max_length=255, required=True)
    full_token = db.StringField(max_length=512, required=True)
    expires_in = db.IntField(default=-1)
    user = db.ReferenceField(EsthenosUser,required=False)
    date_created = db.DateTimeField(default=datetime.datetime.now)

    def to_dbref(self):
        return encode_model(self)

    def __unicode__(self):
        return self.token +" "+str(self.expires_in)

