__author__ = 'prathvi'
from esthenos import db
import datetime
from esthenos.mongo_encoder import encode_model

class PServer(db.Document):
    name = db.StringField(max_length=128,required=True)
    description = db.StringField(max_length=1024, required=False)
    ip_address = db.StringField(max_length=128,required=True)
    s_type = db.StringField(max_length=128,required=True) # amazon /digitalocean /ssd non ssd
    cpu = db.StringField(max_length=10,required=True)
    ram = db.StringField(max_length=10,required=True)
    port = db.IntField(required=True)
    last_accessed = db.DateTimeField(default=datetime.datetime.now)
    added_on = db.DateTimeField(default=datetime.datetime.now)
    instances = db.ListField(db.StringField(max_length=128))
    is_running = db.BooleanField()

    def to_dbref(self):
        return encode_model(self)

    def serialize(self,obj):
        return encode_model(obj)


