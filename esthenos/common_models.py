__author__ = 'prathvi'
from esthenos  import db
import datetime

from p_user.models import PUser
class Metadata(db.Document):
    user = db.ReferenceField(PUser)
    data = db.StringField(max_length=2048,default='{}')
    date_modified = db.DateTimeField(default=datetime.datetime.now)