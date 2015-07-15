#!/usr/bin/python

import sys
import json
import requests
from e_organisation.models import PixuateObjectUrlMap

pan_url='http://console.digikyc.com/api/services/read_pan'
vid_url='http://console.digikyc.com/api/services/read_voters_id'
addhaar_url='http://console.digikyc.com/api/services/read_aadhaar_id'

store_url='http://console.digikyc.com/api/bucket/55378215207ffc40a5e06e68/object'
object_url='http://console.digikyc.com/api/bucket_id/55378215207ffc40a5e06e68/object/'

headers={'InstanceToken' : 'zvgkH-L1eJ1CucZacS6jsb7Fwx0NEGl-40ZM2vvpW0k','Accept':'application/json'}


def get_pan_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(pan_url, files=files,headers=headers)
    return json.loads(json.dumps(response.content))

def get_pan_details_url(path):
    data = {'query_url': path}
    response = requests.post(pan_url, data=data,headers=headers)
    return json.loads(json.dumps(response.content))

def get_vid_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(vid_url, files=files,headers=headers)
    return json.loads(json.dumps(response.content))

def get_vid_details_url(path):
    data = {'query_url': path}
    response = requests.post(vid_url, data=data,headers=headers)
    return json.loads(json.dumps(response.content))

def get_aadhaar_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(addhaar_url, files=files,headers=headers)
    return json.loads(json.dumps(response.content))

def get_aadhaar_details_url(path):
    data = {'query_url': path}
    response = requests.post(addhaar_url, data=data,headers=headers)
    return json.loads(json.dumps(response.content))


def upload_images(path,filename):
    files = {'file': open(path, 'rb')}
    data = {'name':filename}
    response = requests.post(store_url, files=files,data=data,headers=headers)
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
        object.pixuate_url = 'http://console.digikyc.com/objects/' + resp["url_resized"]
        object.pixuate_original_url = 'http://console.digikyc.com/objects/' + resp["url_original"]
        object.save()
        return object.pixuate_url

    
if  __name__== "__main__":
    details_url = "http://api.pixuate.com/objects/55041d942a76201b0bf035ff/693c07c22f8d96204f194152d38d641a_o.jpg"
    get_aadhaar_details_url(details_url)

    #upload_images("pancard1.jpg")
    get_url_with_id("55069e1c2a762045610533a1")
