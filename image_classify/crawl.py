import requests
import json
import base64
import cv2
import pdb
import sys
import time
import os

#to delete the index and start from scratch
os.system('curl -XDELETE https://elasticsearch.leenet.link/images')

url = "https://deepdetectgpu.leenet.link/services/ilsvrc_googlenet"
params = {
 "description": "image classification service",
 "model": {
  "repository": "/opt/models/ilsvrc_googlenet",
  "init": "https://deepdetect.com/models/init/desktop/images/classification/ilsvrc_googlenet.tar.gz",
  "create_repository": True
 },
 "mllib": "caffe",
 "type": "supervised",
 "parameters": {
  "input": {
   "connector": "image"
  }
 }
}
my_json_data = json.dumps(params)
req = requests.post(url,data=my_json_data)
response = req.json()
print(response)
# traverse root directory, and list directories as dirs and files as files
import os
for root, dirs, files in os.walk("/home/alice/share/"):
    try:
        for file in files:
            try:
                if file.endswith(".jpg"):
                    uri = os.path.join(root, file)
                    virtual = uri.replace("/home/alice/share/","")
                    print(uri)
                    imgs = []
                    try:
                        img1 = cv2.imread(uri)
                        retval, buf = cv2.imencode('.jpg',img1)
                        img_base64 = base64.b64encode(buf).decode('utf-8')
                        imgs.append(img_base64)
                    except:
                        print("could not open ", uri)
                        continue
                    url = "https://deepdetectgpu.leenet.link/predict"
                    params = {"service":"ilsvrc_googlenet",
                        "parameters":
                            {
                                "mllib":{
                                    "gpu":True
                                },
                                "input":{"width":224,"height":224},
                                "output":{
                                    "best":3,
                                    "template":"{ {{#body}}{{#predictions}} \"path\":{ \"virtual\":\"" + virtual + "\", \"real\":\"" + uri + "\"},\"categories\": [ {{#classes}} { \"category\":\"{{cat}}\",\"score\":{{prob}} } {{^last}},{{/last}}{{/classes}} ] {{/predictions}}{{/body}} }",
                                    "network":{
                                        "url":"https://elasticsearch.leenet.link/images/img",
                                        "http_method":"POST"
                                    }
                                }
                            },
                        "data":imgs}
                    my_json_data = json.dumps(params)
                    req = requests.post(url,data=my_json_data)
                    response = req.json()
                    print(response)
            except KeyboardInterrupt:
                print("loop exiting via Ctrl+c")
                sys.exit(1) # break or raise
    except KeyboardInterrupt:
        print("loop exiting via Ctrl+c")
        sys.exit(1) # break or raise
        