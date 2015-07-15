#!/usr/bin/python

import sys
import json
import requests
from e_organisation.models import PixuateObjectUrlMap

storage_url='http://api.pixuate.com/rest/v1/bucket/552e9c2e2a762065ac21cc31/object'
object_url='http://api.pixuate.com/rest/v1/bucket_name/EsthenosCustomerEnrollmentForms/object/'
headers={'InstanceToken' : 'YCb3sHjX0Bteg-0zrqynDf7Zp_ldhvVhDhq94XOoW78','Accept':'application/json'}

def upload_images(path,filename):
    files = {'file': open(path, 'rb')}
    data = {'name':filename}
    response = requests.post(storage_url, files=files,data=data,headers=headers)
    return response.content

def get_url_with_id(object_id):
    obj = None
    try:
        obj = PixuateObjectUrlMap.objects.get(pixuate_id=object_id)
    except Exception as e:
        print e.message

    if obj !=None:
        return obj.pixuate_url
    else:
        url =  object_url + object_id
        response = requests.get(url,headers=headers)
        object = PixuateObjectUrlMap()
        object.pixuate_id = object_id

        resp = json.loads(response.content)
        object.pixuate_url = 'http://api.pixuate.com/objects/'+resp["url_resized"]
        object.pixuate_original_url = 'http://api.pixuate.com/objects/'+resp["url_original"]
        object.save()
        return object.pixuate_url

if __name__ == "__main__":
    #upload_images("pancard1.jpg")
    get_url_with_id("55069e1c2a762045610533a1")
