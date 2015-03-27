__author__ = 'prathvi'
from esthenos  import db
import datetime

from e_admin.models import EsthenosUser
class Metadata(db.Document):
    user = db.ReferenceField(EsthenosUser)
    data = db.StringField(max_length=2048,default='{}')
    date_modified = db.DateTimeField(default=datetime.datetime.now)