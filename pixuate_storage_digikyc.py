#!/usr/bin/python

import sys
import requests
import json

store_url='http://console.digikyc.com/api/bucket/55378215207ffc40a5e06e68/object'
#8d4bc6b37028a4e8bb8b61bb6244d545_o.jpg
object_url='http://console.digikyc.com/api/bucket_id/55378215207ffc40a5e06e68/object/'
headers={'InstanceToken' : 'zvgkH-L1eJ1CucZacS6jsb7Fwx0NEGl-40ZM2vvpW0k','Accept':'application/json'}

def upload_images(path,filename):
    files = {'file': open(path, 'rb')}
    data = {'name':filename}
    response = requests.post(store_url, files=files,data=data,headers=headers)
    print response.content
    return response.content



def get_url_with_id(object_id):
    obj = None
    from e_organisation.models import PixuateObjectUrlMap
    try:
        obj = PixuateObjectUrlMap.objects.get(pixuate_id=object_id)
    except Exception as e:
        print e.message
    if obj !=None:
        return obj.pixuate_url
    else:
        url =  object_url + object_id
        print url
        response = requests.get(url,headers=headers)
        object = PixuateObjectUrlMap()
        object.pixuate_id = object_id
        print response.content
        resp = json.loads(response.content)
        object.pixuate_url = 'http://console.digikyc.com/objects/'+resp["url_resized"]
        object.pixuate_original_url = 'http://console.digikyc.com/objects/'+resp["url_original"]
        object.save()
        print response.content
        return object.pixuate_url


if __name__ == "__main__":
    #upload_images("pancard1.jpg")
    get_url_with_id("55069e1c2a762045610533a1")