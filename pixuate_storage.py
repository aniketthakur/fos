#!/usr/bin/python

import sys
import requests
import json

storage_url='http://api.pixuate.com/rest/v1/bucket/55041de92a76201b0bf03602/object'
headers={'InstanceToken' : 'YCb3sHjX0Bteg-0zrqynDf7Zp_ldhvVhDhq94XOoW78','Accept':'application/json'}

def upload_images(path):
    files = {'file': open(path, 'rb')}
    data = {'name':'pancard'}
    response = requests.post(storage_url, files=files,data=data,headers=headers)
    print response.content
    return response.content


if __name__ == "__main__":
    upload_images("pancard1.jpg")